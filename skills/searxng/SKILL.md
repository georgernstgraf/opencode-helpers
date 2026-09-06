---
name: searxng
description: "Search the web using local SearXNG instance. Use when: user asks to search the web, find information, or look something up. Self-hosted at searxng.claw.graf.priv.at."
metadata: { "openclaw": { "emoji": "🔍" } }
---

# SearXNG Web Search Skill

Search the web using self-hosted SearXNG at `searxng.claw.graf.priv.at`.

## Architecture

Three layers, bottom-up:

1. **SearXNG instance** — self-hosted at `https://searxng.claw.graf.priv.at/search` (nginx → `localhost:8888` on the SearXNG host). JSON API: `?q=QUERY&format=json`.
2. **`searxng-search.sh`** — canonical search logic. Plain bash script that `curl`s the JSON API with fallback across instances (`searxng.claw.graf.priv.at` → `etsi.me` → `baresearch.org`; the public URL is primary so the script works on every host — only the SearXNG host itself would resolve `localhost:8888`), returns JSON on stdout. Usable standalone: `./searxng-search.sh "query" [lang] [page] [category] [engines] [time_range] [safesearch]`.
3. **`skills/searxng/scripts/opencode-searxng`** — thin MCP stdio server (Python 3, stdlib only). Speaks JSON-RPC 2.0 over stdin/stdout, exposes one tool `search`, and shells out to `searxng-search.sh`. Registered in `~/.config/opencode/opencode.json` under `mcp.searxng`, so OpenCode exposes it as the **`searxng_search`** tool.

## MCP Tool: `searxng_search`

Exposed by the `skills/searxng/scripts/opencode-searxng` stdio server. Prompt with e.g. `use the searxng_search tool`.

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `query` | string | yes | Search query (quotes for exact versions) |
| `category` | string | no | `general`, `images`, `news`, `it`, `science`; default `general` |
| `engines` | string | no | Comma-separated engine list (e.g. `wikipedia,github`); overrides `category` |
| `time_range` | string | no | `day`, `week`, `month`, `year` — use for recent topics |
| `language` | string | no | Language code (`en`, `de`, `auto`); default `en` |
| `pageno` | integer | no | Results page (1-indexed); default `1` |
| `safesearch` | integer | no | `0` (off), `1` (moderate), `2` (strict) |

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

> These commands run on the **SearXNG host** (where nginx proxies to `localhost:8888`), not necessarily the machine running OpenCode.

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
