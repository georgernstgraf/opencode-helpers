---
name: searxng
description: "Search the web using local SearXNG instance. Use when: user asks to search the web, find information, or look something up. Self-hosted at searxng.claw.graf.priv.at."
metadata: { "openclaw": { "emoji": "🔍" } }
---

# SearXNG Web Search Skill

Search the web using self-hosted SearXNG at `searxng.claw.graf.priv.at`.

## Architecture

- **Primary:** `https://searxng.claw.graf.priv.at/search` (nginx → `localhost:8888`)
- **Wrapper:** `scripts/opencode-searxng` (MCP JSON-RPC server, invoked by OpenCode)

## API Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `query` | string (required) | Search query | `"Gemma 4"` |
| `category` | string | Search category | `general`, `images`, `news`, `it`, `science` |
| `time_range` | string | Age filter | `day`, `week`, `month`, `year` |
| `engines` | string | Comma-separated engine list | `"wikipedia,github,braveapi"` |
| `language` | string | Language code | `"en"`, `"de"`, `"fr"`, `"auto"` |
| `pageno` | integer | Results page number | `1`, `2`, `3` |
| `safesearch` | integer | Safe search filter | `0` (off), `1` (moderate), `2` (strict) |

## Available Engines

### General Web Search
- `braveapi` — Brave Search API (best quality)
- `presearch` — Presearch
- `yacy` — P2P YaCy network
- `ask` — Ask.com
- `quark` — Quark search
- `searchmysite` — Indie websites
- `marginalia` — Non-commercial content

### Knowledge
- `wikipedia` — Wikipedia (with infobox)
- `arxiv` — Scientific papers
- `github` — GitHub repositories
- `github code` — GitHub code search
- `npm`, `lib.rs` — Package registries
- `docker hub`, `arch linux wiki`, `gentoo` — Tech resources

### News
- `hackernews` — Hacker News

## SearXNG Instance

- **Web UI:** https://searxng.claw.graf.priv.at/
- **API:** https://searxng.claw.graf.priv.at/search?q=QUERY&format=json

## Docker Management

```bash
# Check status
docker ps

# View logs
docker logs searxng

# Restart
cd /opt/searxng && docker compose restart

# Stop / Start
cd /opt/searxng && docker compose down
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
