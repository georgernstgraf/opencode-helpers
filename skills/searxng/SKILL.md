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
2. **`searxng-search.sh`** — canonical search logic. Plain bash script that `curl`s the JSON API, returns JSON on stdout. Primary instance is the public URL `searxng.claw.graf.priv.at` (works on every host — only the SearXNG host itself would resolve `localhost:8888`); the historical public mirrors (`etsi.me`, `baresearch.org`) no longer serve `format=json` to anonymous clients (see below). Usable standalone: `./searxng-search.sh "query" [lang] [page] [category] [engines] [time_range] [safesearch]`.
3. **`skills/searxng/scripts/opencode-searxng`** — thin MCP stdio server (Python 3, stdlib only). Speaks JSON-RPC 2.0 over stdin/stdout, exposes one tool `search`, and shells out to `searxng-search.sh`. Registered in `~/.config/opencode/opencode.json` under `mcp.searxng`, so OpenCode exposes it as the **`searxng_search`** tool.

## Backend Egress (deployment detail)

Search quality and which engines are usable depend on the SearXNG instance's
outgoing traffic, not on this skill. The backend currently egresses via a
school IP; if **every** engine returns 0 results, the backend proxy/VPN is the
likely cause — not the skill or the MCP server.

Deployment specifics (proxy host, VPN topology, `settings.yml` proxy setup,
failure modes, egress verification) are operational and host-specific. They are
documented in `opencode-helpers` under `docs/ai/ARCHITECTURE.md` and
`docs/ai/PITFALLS.md`, not here — this skill is portable across hosts.

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
| `engines` | string | Comma-separated engine list | `"wikipedia,github"` |
| `language` | string | Language code | `"en"`, `"de"`, `"fr"`, `"auto"` |
| `pageno` | integer | Results page number | `1`, `2`, `3` |
| `safesearch` | integer | Safe search filter | `0` (off), `1` (moderate), `2` (strict) |

## Available Engines

Engines enabled on the instance (`keep_only` in `/opt/searxng/searxng/settings.yml`).
Last verified 2026-09-12.

### General Web Search
- `google` — **primary general engine** (works via the backend's school-IP
  egress; see above)
- `braveapi` — Brave Search API. May be suspended while the API quota is
  exhausted; revives automatically after top-up.
- `brave` — Brave HTML scraper. Occasionally rate-limit suspended; revives
  automatically.
- `mwmbl` — Mwmbl. Secondary/fallback. Small index: short/common queries
  give relevant results, long-tail queries often return 0 (honest empty).
- `searchmysite` — Indie websites

> **Removed engines:** `bing` web and `yahoo`. Do not re-add without
> re-testing — removal rationale is in `docs/ai/PITFALLS.md`.

### Knowledge / IT
- `wikipedia` — Wikipedia (with infobox)
- `arxiv` — Scientific papers
- `github`, `github code` — GitHub repos and code search
- `npm`, `lib.rs` — Package registries
- `docker hub`, `arch linux wiki`, `gentoo` — Tech resources

### News
- `bing news` — Bing News (separate scraper from the removed `bing` web engine)
- `duckduckgo news` — DuckDuckGo News
- `hackernews` — Hacker News

> **Blocked / not usable** (Captcha, 403, or connection resets):
> `mojeek`, `startpage`, `qwant`, `yep`, `ecosia`, `duckduckgo`.
> Public fallback instances (`etsi.me`, `baresearch.org`) no longer serve
> `format=json` to anonymous clients (429 / anti-bot challenge).
> `google news` is untested on the current backend — test before enabling.

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
