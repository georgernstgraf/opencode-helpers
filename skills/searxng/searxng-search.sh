#!/bin/bash
# SearXNG Web Search - Local First with Public Fallback
# Primary: localhost:8888 (self-hosted)
# Fallback: Public SearXNG instances

set -e

# Configuration - Local instance first, then public fallbacks
INSTANCES=(
    "https://searxng.claw.graf.priv.at"
    "https://etsi.me"
    "https://baresearch.org"
)

TIMEOUT=20
MAX_RESULTS=10
USER_AGENT="OpenClaw Search/1.0"

# Parse arguments
QUERY="${1:-}"
LANG="${2:-en}"
PAGE="${3:-1}"

if [[ -z "$QUERY" ]]; then
    echo '{"success": false, "error": "No query provided"}'
    exit 1
fi

# URL encode query
ENCODED_QUERY=$(printf '%s' "$QUERY" | jq -sRr @uri)

# Try each instance
for INSTANCE in "${INSTANCES[@]}"; do
    URL="${INSTANCE}/search?q=${ENCODED_QUERY}&format=json&language=${LANG}&pageno=${PAGE}"
    
    # Try JSON API
    RESPONSE=$(curl -s --max-time "$TIMEOUT" \
        -H "User-Agent: $USER_AGENT" \
        -H "Accept: application/json" \
        "$URL" 2>/dev/null) || continue
    
    # Check if we got valid JSON with results
    if echo "$RESPONSE" | jq -e '.results | length > 0' >/dev/null 2>&1; then
        # Format results
        echo "$RESPONSE" | jq --arg instance "$INSTANCE" --arg query "$QUERY" --argjson max "$MAX_RESULTS" '
            {
                success: true,
                instance: $instance,
                query: $query,
                total_results: (.number_of_results // 0),
                results: [.results[:($max)] | .[] | {
                    title: (.title // "No title"),
                    url: .url,
                    engine: (.engine // "unknown"),
                    engines: (.engines // []),
                    snippet: ((.content // "") | .[0:300])
                }]
            }
        '
        exit 0
    fi
done

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