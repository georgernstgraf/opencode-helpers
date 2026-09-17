#!/bin/bash
# SearXNG Web Search - prioritized engine chain with a token-gated Brave API fallback.
#
# The default general search walks a strict chain, stopping at the first tier
# that returns results:
#   1. brave             (free HTML scraper) -- the ONLY default result engine
#   2. google            (free HTML scraper)
#   3. mwmbl,searchmysite (free, small indices)
#   4. braveapi          (paid API) -- queried ONLY when tiers 1-2 failed AND
#                        the tier-3 free result is weak (< FALLBACK_MIN_RESULTS).
# Tiers 2-4 are fallback-only: they run only when the preceding tier is empty,
# so google deliberately never appears in normal results (only via the fallback
# chain, or an explicit `engines=google`). The `< 3` gate protects the Brave API
# token. When braveapi runs, its results are merged ahead of the free tier-3
# results (URL-deduplicated). An explicit `engines=` argument bypasses the chain.
# Profiles: SEARXNG_CHAIN=gregor walks google -> brave -> braveapi with no
# free tier (school instance). Instances and per-instance auth come from
# SEARXNG_PRIMARY[/_AUTH]/SEARXNG_FALLBACK[/_AUTH] (see env.sample).

set -e

# Instance chain - public primary, then public fallbacks.
# No localhost entry: the skill runs on multiple hosts; only the SearXNG
# host itself would resolve localhost:8888.
#
# Env overrides (see env.sample): SEARXNG_PRIMARY replaces the whole list;
# SEARXNG_FALLBACK appends a second instance. Each instance has its own
# auth (SEARXNG_PRIMARY_AUTH / SEARXNG_FALLBACK_AUTH as "user:password",
# or SEARXNG_PRIMARY_CRED_FILE / SEARXNG_FALLBACK_CRED_FILE pointing at a
# file with that format); empty means the shared default below.
INSTANCES=(
    "https://searxng.claw.graf.priv.at"
    "https://etsi.me"
    "https://baresearch.org"
)

TIMEOUT=20
FOLLOWUP_TIMEOUT=12
MAX_RESULTS=10
USER_AGENT="opencode-searxng/1.4"

# Optional shared-secret auth for the public instance (HTTP Basic, enforced at
# nginx). Read from $SEARXNG_AUTH or ~/.config/opencode/searxng.cred as
# "user:password"; when absent, requests are sent unauthenticated.
# This is the DEFAULT used for every instance without a per-instance override.
AUTH="${SEARXNG_AUTH:-}"
if [[ -z "$AUTH" && -r "${HOME}/.config/opencode/searxng.cred" ]]; then
    AUTH="$(head -n1 "${HOME}/.config/opencode/searxng.cred")"
fi
CURL_AUTH=()
if [[ -n "$AUTH" ]]; then
    CURL_AUTH=(--user "$AUTH")
fi

# Resolve one per-instance auth value. Set-but-empty direct value means
# "no auth for this instance"; unset direct/file values mean "use the
# shared CURL_AUTH default" (sentinel __SHARED__).
resolve_instance_auth() {
    local dref="$1" fref="$2"
    if [[ -v $dref ]]; then
        printf '%s' "${!dref}"
    elif [[ -v $fref && -n "${!fref}" && -r "${!fref}" ]]; then
        head -n1 "${!fref}"
    else
        printf '__SHARED__'
    fi
}

INSTANCE_AUTHS=()
if [[ -n "${SEARXNG_PRIMARY:-}" ]]; then
    INSTANCES=("$SEARXNG_PRIMARY")
    INSTANCE_AUTHS=(
        "$(resolve_instance_auth SEARXNG_PRIMARY_AUTH SEARXNG_PRIMARY_CRED_FILE)"
    )
    if [[ -n "${SEARXNG_FALLBACK:-}" ]]; then
        INSTANCES+=("$SEARXNG_FALLBACK")
        INSTANCE_AUTHS+=(
            "$(resolve_instance_auth SEARXNG_FALLBACK_AUTH SEARXNG_FALLBACK_CRED_FILE)"
        )
    fi
fi

# Curl auth args for instance $1 (index into INSTANCES): the per-instance
# value when set, no auth when explicitly emptied, otherwise the shared
# default. Result in $AUTH_ARGS.
auth_args_for() {
    # No colon in ${..-..}: an explicitly emptied entry means "no auth",
    # only a missing entry falls back to the shared default.
    local idx="$1" per="${INSTANCE_AUTHS[$idx]-__SHARED__}"
    AUTH_ARGS=()
    if [[ "$per" == "__SHARED__" ]]; then
        if [[ "${#CURL_AUTH[@]}" -gt 0 ]]; then
            AUTH_ARGS=("${CURL_AUTH[@]}")
        fi
    elif [[ -n "$per" ]]; then
        AUTH_ARGS=(--user "$per")
    fi
}

# Strict chain: free scrapers first, then the free last-resort tier, then the
# paid API gated on a weak free result.
CHAIN_PRIMARY="brave"
CHAIN_SECONDARY="google"
FREE_FALLBACK="mwmbl,searchmysite"
FALLBACK_ENGINE="braveapi"
FALLBACK_MIN_RESULTS=3
# Chain profile (see env.sample): "gregor" serves the Gregor school instance
# as google -> brave -> braveapi with no free last-resort tier.
if [[ "${SEARXNG_CHAIN:-default}" == "gregor" ]]; then
    CHAIN_PRIMARY="google"
    CHAIN_SECONDARY="brave"
    FREE_FALLBACK=""
fi
EMPTY_JSON='{"number_of_results":0,"results":[]}'

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
# $3 = optional single instance to use (defaults to the whole chain),
# $4 = per-request timeout (defaults to TIMEOUT).
# Sets R_JSON / R_INSTANCE to the accepted (or last valid) response.
run_query() {
    local extra="$1"
    local require_results="$2"
    local only_instance="${3:-}"
    local timeout="${4:-$TIMEOUT}"
    local first_json="" first_instance=""
    R_JSON=""
    R_INSTANCE=""
    local idx instance url response
    for idx in "${!INSTANCES[@]}"; do
        instance="${INSTANCES[$idx]}"
        if [[ -n "$only_instance" && "$instance" != "$only_instance" ]]; then
            continue
        fi
        url="${instance}/search?q=${ENCODED_QUERY}&format=json&language=${LANG}&pageno=${PAGE}${extra}"
        auth_args_for "$idx"
        response=$(curl -s --max-time "$timeout" \
            "${AUTH_ARGS[@]}" \
            -H "User-Agent: $USER_AGENT" \
            -H "Accept: application/json" \
            "$url" 2>/dev/null) || continue

        echo "$response" | jq -e 'type == "object" and has("results")' >/dev/null 2>&1 || continue

        # Remember the first responsive instance: if no instance yields results,
        # this is the one whose (empty) answer we report and build on.
        if [[ -z "$first_json" ]]; then
            first_json="$response"
            first_instance="$instance"
        fi

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
    if [[ -n "$first_json" ]]; then
        R_JSON="$first_json"
        R_INSTANCE="$first_instance"
    fi
    return 0
}

# Count results attributed to one engine (via .engine or the .engines list).
engine_hits() {
    local json="$1" engine="$2"
    if [[ -z "$json" ]]; then
        echo 0
        return 0
    fi
    echo "$json" | jq --arg e "$engine" '
        [.results[] | select((.engine == $e) or ((.engines // []) | index($e)))]
        | length' 2>/dev/null || echo 0
}

# Append an engine (or comma-separated engine group) to the TRIED array.
mark_tried() {
    local group="$1"
    local -a names
    IFS=',' read -r -a names <<<"$group"
    local name
    for name in "${names[@]}"; do
        TRIED=$(jq -cn --argjson a "$TRIED" --arg b "$name" '$a + [$b]')
    done
}

# Union the response's unresponsive engines into UNRESP (deduplicated).
collect_unresponsive() {
    local json="$1" add
    if [[ -z "$json" ]]; then
        return 0
    fi
    add=$(echo "$json" | jq -c '.unresponsive_engines // []' 2>/dev/null) || return 0
    UNRESP=$(jq -cn --argjson a "$UNRESP" --argjson b "$add" '$a + $b | unique')
}

# Emit one response as the tool's JSON envelope.
# $1 = response JSON, $2 = instance, $3 = deciding engine ("brave"/"google"/
#      "braveapi"/"mwmbl"/"searchmysite"/"none"), $4 = fallback used (true/false),
# $5 = tried engines (JSON array), $6 = unresponsive engines (JSON array).
emit() {
    echo "$1" | jq --arg instance "$2" --arg query "$QUERY" --arg engine_used "$3" \
        --argjson max "$MAX_RESULTS" --argjson used "$4" \
        --argjson tried "$5" --argjson unresp "$6" '
        {
            success: true,
            instance: $instance,
            query: $query,
            engine_used: $engine_used,
            fallback_used: $used,
            tried: $tried,
            unresponsive_engines: $unresp,
            total_results: (if (.number_of_results // 0) > 0 then .number_of_results else (.results | length) end),
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
    '
}

UNRESP="[]"
TRIED="[]"

# Params shared by every chain tier (never the category: SearXNG ignores
# `engines=` when `categories=` is present).
CHAIN_PARAMS="${TIME_PARAM}${SAFE_PARAM}"

# --- Explicit engines or non-general category: single request, no chain ------
if [[ -n "$ENGINES" || ( -n "$CATEGORY" && "$CATEGORY" != "general" ) ]]; then
    run_query "$EXTRA_PARAMS" 0
    if [[ -z "$R_JSON" ]]; then
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
    if [[ -n "$ENGINES" ]]; then
        mark_tried "$ENGINES"
    fi
    collect_unresponsive "$R_JSON"
    FIRST_ENGINE=$(echo "$R_JSON" | jq -r '.results[0].engine // "unknown"' 2>/dev/null || echo unknown)
    emit "$R_JSON" "$R_INSTANCE" "$FIRST_ENGINE" false "$TRIED" "$UNRESP"
    exit 0
fi

# --- Tier 1: brave (free scraper) -------------------------------------------
run_query "&engines=${CHAIN_PRIMARY}${CHAIN_PARAMS}" 1
PRIMARY_JSON="$R_JSON"
ACTIVE_INSTANCE="$R_INSTANCE"
mark_tried "$CHAIN_PRIMARY"
collect_unresponsive "$PRIMARY_JSON"

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

if [[ "$(engine_hits "$PRIMARY_JSON" "$CHAIN_PRIMARY")" -gt 0 ]]; then
    emit "$PRIMARY_JSON" "$ACTIVE_INSTANCE" "$CHAIN_PRIMARY" false "$TRIED" "$UNRESP"
    exit 0
fi

# --- Tier 2: google (free scraper) ------------------------------------------
run_query "&engines=${CHAIN_SECONDARY}${CHAIN_PARAMS}" 1 "$ACTIVE_INSTANCE" "$FOLLOWUP_TIMEOUT"
SECOND_JSON="$R_JSON"
if [[ -n "$R_INSTANCE" ]]; then ACTIVE_INSTANCE="$R_INSTANCE"; fi
mark_tried "$CHAIN_SECONDARY"
collect_unresponsive "$SECOND_JSON"

if [[ "$(engine_hits "$SECOND_JSON" "$CHAIN_SECONDARY")" -gt 0 ]]; then
    emit "$SECOND_JSON" "$ACTIVE_INSTANCE" "$CHAIN_SECONDARY" true "$TRIED" "$UNRESP"
    exit 0
fi

# --- Tier 3: free last resort (mwmbl + searchmysite) -------------------------
# Empty in profiles without a free tier (e.g. gregor): fall through to the
# API tier with an empty free result.
if [[ -n "$FREE_FALLBACK" ]]; then
    run_query "&engines=${FREE_FALLBACK}${CHAIN_PARAMS}" 0 "$ACTIVE_INSTANCE" "$FOLLOWUP_TIMEOUT"
    FREE_JSON="${R_JSON:-$EMPTY_JSON}"
    if [[ -n "$R_INSTANCE" ]]; then ACTIVE_INSTANCE="$R_INSTANCE"; fi
    mark_tried "$FREE_FALLBACK"
    collect_unresponsive "$R_JSON"
else
    FREE_JSON="$EMPTY_JSON"
fi

FREE_COUNT=$(echo "$FREE_JSON" | jq '.results | length' 2>/dev/null || echo 0)

# --- Tier 4: braveapi, gated on a weak free result (token conservation) ------
if [[ "$FREE_COUNT" -lt "$FALLBACK_MIN_RESULTS" ]]; then
    run_query "&engines=${FALLBACK_ENGINE}${CHAIN_PARAMS}" 1 "$ACTIVE_INSTANCE" "$FOLLOWUP_TIMEOUT"
    FALLBACK_JSON="$R_JSON"
    mark_tried "$FALLBACK_ENGINE"
    collect_unresponsive "$FALLBACK_JSON"

    if [[ "$(engine_hits "$FALLBACK_JSON" "$FALLBACK_ENGINE")" -gt 0 ]]; then
        MERGED=$(jq -n --argjson api "$FALLBACK_JSON" --argjson free "$FREE_JSON" '
            ($api.results) as $a
            | ($free.results) as $f
            | reduce ($a + $f)[] as $r ([]; if any(.[]; (.url // "") == ($r.url // "")) then . else . + [$r] end)
            | { number_of_results: length, results: . }')
        emit "$MERGED" "$ACTIVE_INSTANCE" "$FALLBACK_ENGINE" true "$TRIED" "$UNRESP"
        exit 0
    fi
fi

# --- No API (or it failed): emit the free result, even when weak/empty -------
if [[ "$FREE_COUNT" -gt 0 ]]; then
    FREE_ENGINE=$(echo "$FREE_JSON" | jq -r '.results[0].engine // "mwmbl"' 2>/dev/null || echo mwmbl)
    emit "$FREE_JSON" "$ACTIVE_INSTANCE" "$FREE_ENGINE" true "$TRIED" "$UNRESP"
else
    emit "$FREE_JSON" "$ACTIVE_INSTANCE" "none" true "$TRIED" "$UNRESP"
fi
exit 0
