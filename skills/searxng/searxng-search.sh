#!/bin/bash
# SearXNG Web Search - instance chain with a quality-gated fallback engine.
#
# Phase 1 queries the instance chain (self-hosted primary, then public
# fallbacks). If a general search yields no *reasonable* results, phase 2
# retries once with the fallback engine (Brave Search API) and merges the
# results. Explicit `engines` always bypasses the fallback.

set -e

# Instance chain - public primary, then public fallbacks.
# No localhost entry: the skill runs on multiple hosts; only the SearXNG
# host itself would resolve localhost:8888.
INSTANCES=(
    "https://searxng.claw.graf.priv.at"
    "https://etsi.me"
    "https://baresearch.org"
)

TIMEOUT=20
MAX_RESULTS=10
USER_AGENT="opencode-searxng/1.3"

# Quality gate for the fallback engine. The engine is queried only when the
# primary search returns no reasonable results:
#   - zero results, or
#   - no Google result and fewer than FALLBACK_MIN_RESULTS results.
# The fallback runs for general searches only (not for explicit engines).
FALLBACK_ENGINE="braveapi"
FALLBACK_MIN_RESULTS=3

# Parse arguments
QUERY="${1:-}"
LANG="${2:-en}"
PAGE="${3:-1}"
CATEGORY="${4:-}"
ENGINES="${5:-}"
TIME_RANGE="${6:-}"
SAFESEARCH="${7:-}"

if [[ -z "$QUERY" ]]; then
    echo '{"success": false, "error": "No query provided"}'
    exit 1
fi

# URL encode query
ENCODED_QUERY=$(printf '%s' "$QUERY" | jq -sRr @uri)

# Optional search parameters (empty = server defaults).
# Explicit `engines` overrides `categories`: SearXNG ignores the engines filter
# when a category is present, so the two are never combined.
CATEGORY_PARAM=""
if [[ -n "$CATEGORY" && -z "$ENGINES" ]]; then
    CATEGORY_PARAM="&categories=$(printf '%s' "$CATEGORY" | jq -sRr @uri)"
fi
ENGINES_PARAM=""
if [[ -n "$ENGINES" ]]; then
    ENGINES_PARAM="&engines=$(printf '%s' "$ENGINES" | jq -sRr @uri)"
fi
TIME_PARAM=""
if [[ -n "$TIME_RANGE" ]]; then
    TIME_PARAM="&time_range=$(printf '%s' "$TIME_RANGE" | jq -sRr @uri)"
fi
SAFE_PARAM=""
if [[ -n "$SAFESEARCH" ]]; then
    SAFE_PARAM="&safesearch=${SAFESEARCH}"
fi

EXTRA_PARAMS="${CATEGORY_PARAM}${ENGINES_PARAM}${TIME_PARAM}${SAFE_PARAM}"

# Run one query across the instance chain.
# $1 = extra URL params (with leading &), $2 = "1" to require >0 results,
# $3 = optional single instance to use (defaults to the whole chain).
# Sets R_JSON / R_INSTANCE to the accepted (or last valid) response.
run_query() {
    local extra="$1"
    local require_results="$2"
    local only_instance="${3:-}"
    local instance url response
    local instances=("${INSTANCES[@]}")
    if [[ -n "$only_instance" ]]; then
        instances=("$only_instance")
    fi
    R_JSON=""
    R_INSTANCE=""
    for instance in "${instances[@]}"; do
        url="${instance}/search?q=${ENCODED_QUERY}&format=json&language=${LANG}&pageno=${PAGE}${extra}"
        response=$(curl -s --max-time "$TIMEOUT" \
            -H "User-Agent: $USER_AGENT" \
            -H "Accept: application/json" \
            "$url" 2>/dev/null) || continue

        echo "$response" | jq -e 'type == "object" and has("results")' >/dev/null 2>&1 || continue

        R_JSON="$response"
        R_INSTANCE="$instance"

        if [[ "$require_results" == "1" ]]; then
            if echo "$response" | jq -e '(.results | length) > 0' >/dev/null 2>&1; then
                return 0
            fi
        else
            # Accept when there are results, or when the instance is healthy
            # (empty + no unresponsive engines = genuine empty answer).
            if echo "$response" | jq -e \
                '(.results | length) > 0 or (.unresponsive_engines // [] | length) == 0' \
                >/dev/null 2>&1; then
                return 0
            fi
        fi
        # Empty results but engines failed on this instance: try the next one.
    done
    return 0
}

# Emit one response as the tool's JSON envelope.
# $1 = response JSON, $2 = instance, $3 = fallback used (true/false),
# $4 = fallback reason ("empty"/"weak"/"").
emit() {
    echo "$1" | jq --arg instance "$2" --arg query "$QUERY" --argjson max "$MAX_RESULTS" \
        --argjson used "$3" --arg reason "$4" '
        {
            success: true,
            instance: $instance,
            query: $query,
            fallback_used: $used,
            total_results: (.number_of_results // (.results | length)),
            results: [.results[:($max)] | .[] | {
                title: (.title // "No title"),
                url: .url,
                engine: (.engine // "unknown"),
                engines: (.engines // []),
                snippet: ((.content // "") | .[0:300]),
                img_src: .img_src,
                thumbnail: .thumbnail,
                publishedDate: .publishedDate
            } | with_entries(select(.value != null))]
        }
        + (if $used then {fallback_reason: $reason} else {} end)
    '
}

# --- Phase 1: primary search ---------------------------------------------
run_query "$EXTRA_PARAMS" 0
PRIMARY_JSON="$R_JSON"
PRIMARY_INSTANCE="$R_INSTANCE"

if [[ -z "$PRIMARY_JSON" ]]; then
    cat <<EOF
{
    "success": false,
    "error": "All SearXNG instances unavailable",
    "tried": $(printf '%s\n' "${INSTANCES[@]}" | jq -R . | jq -s .),
    "query": "$QUERY",
    "suggestion": "Check if Docker container is running: docker ps",
    "restart": "cd /opt/searxng && docker compose restart"
}
EOF
    exit 0
fi

# --- Decide whether the fallback engine is warranted ---------------------
FALLBACK_REASON=""
if [[ -z "$ENGINES" && ( -z "$CATEGORY" || "$CATEGORY" == "general" ) ]]; then
    COUNT=$(echo "$PRIMARY_JSON" | jq '.results | length')
    GOOGLE=$(echo "$PRIMARY_JSON" | jq '
        [.results[]
         | select((.engine == "google") or ((.engines // []) | index("google")))]
        | length')
    if [[ "$COUNT" -eq 0 ]]; then
        FALLBACK_REASON="empty"
    elif [[ "$GOOGLE" -eq 0 && "$COUNT" -lt "$FALLBACK_MIN_RESULTS" ]]; then
        FALLBACK_REASON="weak"
    fi
fi

# --- Phase 2: fallback search, merge on success --------------------------
if [[ -n "$FALLBACK_REASON" ]]; then
    FALLBACK_EXTRA="&engines=$(printf '%s' "$FALLBACK_ENGINE" | jq -sRr @uri)${TIME_PARAM}${SAFE_PARAM}"
    run_query "$FALLBACK_EXTRA" 1 "$PRIMARY_INSTANCE"

    if [[ -n "$R_JSON" ]] && echo "$R_JSON" | jq -e '(.results | length) > 0' >/dev/null 2>&1; then
        MERGED=$(jq -n --argjson primary "$PRIMARY_JSON" --argjson fallback "$R_JSON" '
            ($primary.results) as $p
            | ($fallback.results) as $f
            | reduce ($p + $f)[] as $r ([]; if any(.[]; (.url // "") == ($r.url // "")) then . else . + [$r] end)
            | { number_of_results: length, results: . }')
        emit "$MERGED" "$PRIMARY_INSTANCE" true "$FALLBACK_REASON"
        exit 0
    fi
fi

emit "$PRIMARY_JSON" "$PRIMARY_INSTANCE" false ""
exit 0
