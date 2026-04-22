---
name: searxng
description: "Search the web using local SearXNG instance with automatic fallback to public instances. Use when: user asks to search the web, find information, or look something up. Self-hosted at localhost:8888."
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["curl", "jq"] } } }
---

# SearXNG Web Search Skill

Search the web using local SearXNG instance (self-hosted) with fallback to public instances.

## Architecture

**Primary:** localhost:8888 (self-hosted SearXNG)
**Fallback:** Public SearXNG instances

## Usage

### Basic Search

```bash
{baseDir}/searxng-search.sh "your search query"
```

### Search with Language

```bash
{baseDir}/searxng-search.sh "Wetter in Berlin" "de"
```

### Pagination

```bash
{baseDir}/searxng-search.sh "python async" "en" 2
```

## SearXNG Instance

Your self-hosted SearXNG is running at:

- **Web UI:** http://localhost:8888
- **API:** http://localhost:8888/search?q=QUERY&format=json

## Output Format

```json
{
  "success": true,
  "instance": "http://localhost:8888",
  "query": "search query",
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "engine": "brave",
      "snippet": "Description..."
    }
  ]
}
```

## Docker Management

```bash
# Check status
docker ps

# View logs
docker logs searxng

# Restart
cd /opt/searxng && docker compose restart

# Stop
cd /opt/searxng && docker compose down

# Start
cd /opt/searxng && docker compose up -d
```

## Memory Usage

- SearXNG container: ~200-400MB RAM
- Redis (Valkey): ~50-100MB RAM
- Total: ~250-500MB RAM

Check usage:
```bash
docker stats --no-stream
```