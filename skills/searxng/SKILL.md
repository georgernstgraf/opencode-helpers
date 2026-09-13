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

## Prioritized Engine Chain with a Token Gate

`searxng-search.sh` walks a strict chain for **general** searches and stops at
the first tier that returns results:

1. `brave` — free HTML scraper
2. `google` — free HTML scraper
3. `mwmbl,searchmysite` — free, small-index last resort
4. `braveapi` — paid API, queried **only** when tiers 1–2 failed *and* the
   tier-3 free result has fewer than `FALLBACK_MIN_RESULTS` (3) hits

A tier "fails" when the engine is suspended (`unresponsive_engines`) or returns
0 results. When `braveapi` runs, its results are merged **ahead of** the free
tier-3 results, deduplicated by URL.

> **`brave` is the only engine that serves normal results.** `google`,
> `mwmbl,searchmysite` and `braveapi` are *fallback-only*: each runs only when
> the preceding tier comes back empty. `google` therefore deliberately never
> appears in an ordinary result set — it is reached solely inside the fallback
> chain, or when a caller passes `engines=google` explicitly. Its absence from
> default results is by design, not a fault.

- The answer carries `engine_used` (`brave`/`google`/`braveapi`/`mwmbl`/
  `searchmysite`/`none`), `fallback_used` (`engine_used != "brave"`), `tried`
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
| `engines` | string | no | Comma-separated engine list (e.g. `wikipedia,github`); overrides `category` and disables the engine chain |
| `time_range` | string | no | `day`, `week`, `month`, `year` — use for recent topics |
| `language` | string | no | Language code (`en`, `de`, `auto`); default `en` |
| `pageno` | integer | no | Results page (1-indexed); default `1` |
| `safesearch` | integer | no | `0` (off), `1` (moderate), `2` (strict) |

## Available Engines

Engines enabled on the instance (`keep_only` in `/opt/searxng/searxng/settings.yml`).
Last verified 2026-09-12.

### General Web Search
Chain order for general searches: `brave` → `google` → `mwmbl,searchmysite` →
(`braveapi`, gated on < 3 free hits).
- `brave` — **primary general engine** (HTML scraper). Occasionally rate-limit
  suspended; revives automatically.
- `google` — **fallback tier 2 only** (HTML scraper; works via the backend's
  school-IP egress; see above). Never a default result engine: reached only when
  `brave` returns nothing, or via explicit `engines=google`. Can be
  CAPTCHA-suspended.
- `mwmbl` — Mwmbl (small index). Free last-resort before spending Brave quota:
  short/common queries give relevant results, long-tail queries often return 0.
- `searchmysite` — Indie websites. Same free last-resort tier as `mwmbl`.
- `braveapi` — Brave Search API (independent index, paid). **Token-gated**: excluded
  from normal instance searches and queried automatically only when `brave` and
  `google` both fail *and* the free tier-3 result is weak (< 3 hits), or
  explicitly via `engines=braveapi`. Suspended when its quota is exhausted;
  revives automatically after top-up.

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

## Access Control (shared secret)

The public instance is **not open**: nginx enforces HTTP Basic Auth on the whole
vhost (UI and API), and SearXNG's port `8888` is bound to `127.0.0.1` only, so the
instance cannot be reached except through nginx. Intended clients are claw,
think and dell.

- `searxng-search.sh` reads the credential from `$SEARXNG_AUTH` or
  `~/.config/opencode/searxng.cred` (format `user:password`, mode `600`) and
  sends it as Basic auth. Without a credential the request is unauthenticated
  and nginx answers `401`.
- Deploy the credential file (mode `600`) on each client host; never commit it.
- The credential is served by the `searxng` htpasswd file at
  `/etc/nginx/searxng.htpasswd` on the instance host. Rate limiting
  (`limit_req`) is also enforced there.
- The vhost logs to its **own** files — `/var/log/nginx/searxng.access.log`
  (custom `searxng` format with `rt=$request_time`) and
  `/var/log/nginx/searxng.error.log` — so Basic-Auth rejections (`401`) and
  rate-limit hits (`429`) are measurable and the shared `access.log` stays free
  of SearXNG traffic. Rotation is covered by the existing
  `/etc/logrotate.d/nginx` glob. Config: `/etc/nginx/sites-available/searxng.claw.graf.priv.at`.

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
