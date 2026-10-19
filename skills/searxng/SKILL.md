---
name: searxng
description: "Search the web using a configured self-hosted SearXNG instance. Use when: user asks to search the web, find information, or look something up."
metadata: { "openclaw": { "emoji": "🔍" } }
---

# SearXNG Web Search Skill

Search the web using self-hosted SearXNG instances. **This skill is
instance-neutral**: it ships no endpoints and no credentials. Which instance(s)
it queries is decided entirely by the host's environment overlay (see
`env.sample` and the "Environment contract" section below). Deployment
specifics of any concrete instance (host, network path, auth setup, engine
matrix) are documented in that host's own repository — not here.

## Architecture

Three layers, bottom-up:

1. **SearXNG instance(s)** — self-hosted, host-specific. The JSON API is
   `GET <instance>/search?q=QUERY&format=json`.
2. **`searxng-search.sh`** — canonical search logic. Plain bash script that
   `curl`s the JSON API, returns JSON on stdout. Usable standalone:
   `SEARXNG_PRIMARY=... ./searxng-search.sh "query" [lang] [page] [category] [engines] [time_range] [safesearch]`.
3. **`skills/searxng/scripts/opencode-searxng`** — thin MCP stdio server (Python 3, stdlib only). Speaks JSON-RPC 2.0 over stdin/stdout, exposes one tool `search`, and shells out to `searxng-search.sh`. Registered in the host's `~/.config/opencode/opencode.json` under `mcp.searxng`, so OpenCode exposes it as the **`searxng_search`** tool.

## Environment contract (instance selection and auth)

| Variable | Meaning |
|---|---|
| `SEARXNG_PRIMARY` | **Required.** Base URL of the primary instance. Without it the script reports a configuration error instead of querying anything. |
| `SEARXNG_FALLBACK` | Optional second instance, tried in order when the primary yields nothing usable. |
| `SEARXNG_PRIMARY_AUTH` / `SEARXNG_FALLBACK_AUTH` | HTTP Basic credentials for that instance as `user:password`. Set-but-empty means "no auth for this instance". |
| `SEARXNG_PRIMARY_CRED_FILE` / `SEARXNG_FALLBACK_CRED_FILE` | Path to a file whose first line holds `user:password` (mode `600`). |
| `SEARXNG_CHAIN` | Engine-chain profile: `default` or `strict` (see below). |

Rules:

- There is **no shared default credential** and no built-in instance list.
  An instance without `_AUTH`/`_CRED_FILE` is queried unauthenticated.
- Real credentials live in host-local overlays only — never in this repo.
  Copy `skills/searxng/env.sample` as the starting point.
- The `run_query` loop walks the instance chain (primary first) and accepts
  the first instance that returns a usable answer; `instance` in the result
  envelope names the instance that actually served the query.

## Prioritized Engine Chain with a Token Gate

`searxng-search.sh` walks a strict chain for **general** searches and stops at
the first tier that returns results (default profile):

1. `bing` — free HTML scraper
2. `yahoo` — free HTML scraper
3. `mwmbl,searchmysite` — free, small-index last resort
4. `braveapi` — paid API, queried **only** when tiers 1–2 failed *and* the
   tier-3 free result has fewer than `FALLBACK_MIN_RESULTS` (3) hits

### Chain profile `strict` (env.sample)

`SEARXNG_CHAIN=strict` skips the free last-resort tier:
`bing` → `yahoo` → `braveapi` (tier 3 is the API, ungated). The legacy
profile value `gregor` is accepted as a deprecated alias only until every
host overlay is migrated, then it will be removed.

> **Why not `brave`/`google`?** As of 2026-10-08 both are upstream-broken,
> independent of the egress IP: `brave` answers `429` and the `google` engine
> still calls the retired `/wml/search` endpoint (`HTTP 403`, searxng#5867).
> `bing` and `yahoo` were the only general engines that worked on every tested
> egress IP (VPS, school, residential). `brave`/`google` stay enabled
> server-side for a future upstream fix, but are no longer in the chain.

A tier "fails" when the engine is suspended (`unresponsive_engines`) or returns
0 results. When `braveapi` runs, its results are merged **ahead of** the free
tier-3 results, deduplicated by URL.

> **`bing` is the only engine that serves normal results.** `yahoo`,
> `mwmbl,searchmysite` and `braveapi` are *fallback-only*: each runs only when
> the preceding tier comes back empty. `yahoo` therefore deliberately never
> appears in an ordinary result set — it is reached solely inside the fallback
> chain, or when a caller passes `engines=yahoo` explicitly. Its absence from
> default results is by design, not a fault.

- The answer carries `engine_used` (`bing`/`yahoo`/`braveapi`/`mwmbl`/
  `searchmysite`/`none`), `fallback_used` (`engine_used != "bing"`), `tried`
  (engines actually attempted) and `unresponsive_engines` (union, for diagnosis).
- An explicit `engines=` list **disables** the chain (caller intent wins), and
  the chain applies to general searches only — not to
  `news`/`it`/`science`/`images`.
- The `< 3` gate and the free tier-3 buffer exist to **protect the Brave API
  token (paid quota)**: the chain only spends a Brave request when both free
  scrapers are blocked and the free indices are too thin.
- `braveapi` is excluded from normal instance searches, so ordinary searches do
  not consume Brave quota.

## Backend Egress (deployment detail)

Search quality and which engines are usable depend on the SearXNG instance's
outgoing traffic, not on this skill. If **every** engine returns 0 results,
the instance's egress path is the likely cause — not the skill or the MCP
server. A single engine failing (e.g. `google` 403) is an engine/upstream
issue, not egress. Egress topology, engine matrices and failure modes are
operational and host-specific: they live in the instance host's repository,
not here — this skill is portable across hosts.

## MCP Tool: `searxng_search`

Exposed by the `skills/searxng/scripts/opencode-searxng` stdio server. Prompt with e.g. `use the searxng_search tool`.

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `query` | string | yes | Search query (quotes for exact versions) |
| `category` | string | no | `general`, `images`, `news`, `it`, `science`; default `general` |
| `engines` | string | no | Comma-separated engine list (e.g. `wikipedia,github`); overrides `category` and disables the engine chain |
| `time_range` | string | no | `day`, `week`, `month`, `year` — use for recent topics |
| `language` | string | no | Language code (`en`, `de`, `fr`, `auto`); default `en` |
| `pageno` | integer | no | Results page (1-indexed); default `1` |
| `safesearch` | integer | no | `0` (off), `1` (moderate), `2` (strict) |

## SearXNG Instance (generic)

- **Web UI:** `<instance-base-url>/`
- **API:** `<instance-base-url>/search?q=QUERY&format=json`

Concrete instance URLs, access-control setups (Basic Auth, rate limiting,
noindex policy) and Docker management commands are host-specific deployment
knowledge — see the instance host's repository documentation.

## Memory Usage

- SearXNG container: ~200-400MB RAM
- Redis (Valkey): ~50-100MB RAM
- Total: ~250-500MB RAM

Check usage:
```bash
docker stats --no-stream
```
