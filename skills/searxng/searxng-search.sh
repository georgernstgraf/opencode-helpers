#!/bin/bash
# SearXNG Web Search - Local First with Public Fallback
# Primary: localhost:8888 (self-hosted)
# Fallback: Public SearXNG instances

set -e

# Configuration - Public primary, then public fallbacks.
# No localhost entry: the skill runs on multiple hosts; only the SearXNG
# host itself would resolve localhost:8888.
INSTANCES=(
    "https://searxng.claw.graf.priv.at"
    "https://etsi.me"
    "https://baresearch.org"
)

TIMEOUT=20
MAX_RESULTS=10
USER_AGENT="opencode-searxng/1.2"

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

# Optional search parameters (empty = server defaults)
EXTRA_PARAMS=""
if [[ -n "$CATEGORY" ]]; then
    EXTRA_PARAMS+="&categories=$(printf '%s' "$CATEGORY" | jq -sRr @uri)"
fi
if [[ -n "$ENGINES" ]]; then
    EXTRA_PARAMS+="&engines=$(printf '%s' "$ENGINES" | jq -sRr @uri)"
fi
if [[ -n "$TIME_RANGE" ]]; then
    EXTRA_PARAMS+="&time_range=$(printf '%s' "$TIME_RANGE" | jq -sRr @uri)"
fi
if [[ -n "$SAFESEARCH" ]]; then
    EXTRA_PARAMS+="&safesearch=${SAFESEARCH}"
fi

# Format one valid instance response
emit() {
    echo "$1" | jq --arg instance "$2" --arg query "$QUERY" --argjson max "$MAX_RESULTS" '
        {
            success: true,
            instance: $instance,
            query: $query,
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
    '
}

# Try each instance
LAST_VALID=""
LAST_INSTANCE=""
for INSTANCE in "${INSTANCES[@]}"; do
    URL="${INSTANCE}/search?q=${ENCODED_QUERY}&format=json&language=${LANG}&pageno=${PAGE}${EXTRA_PARAMS}"

    # Try JSON API
    RESPONSE=$(curl -s --max-time "$TIMEOUT" \
        -H "User-Agent: $USER_AGENT" \
        -H "Accept: application/json" \
        "$URL" 2>/dev/null) || continue

    # Check if we got valid JSON with a results array
    if echo "$RESPONSE" | jq -e 'type == "object" and has("results")' >/dev/null 2>&1; then
        LAST_VALID="$RESPONSE"
        LAST_INSTANCE="$INSTANCE"

        # Emit immediately if there are results, or if the instance is healthy
        # (empty + no unresponsive engines = genuine empty answer)
        if echo "$RESPONSE" | jq -e \
            '(.results | length) > 0 or (.unresponsive_engines // [] | length) == 0' \
            >/dev/null 2>&1; then
            emit "$RESPONSE" "$INSTANCE"
            exit 0
        fi
        # Empty results but engines failed on this instance: try the next one
    fi
done

# Every instance returned an empty answer with broken engines.
# Emit the last valid (but empty) response rather than reporting total failure.
if [[ -n "$LAST_VALID" ]]; then
    emit "$LAST_VALID" "$LAST_INSTANCE"
    exit 0
fi

# All instances failed
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