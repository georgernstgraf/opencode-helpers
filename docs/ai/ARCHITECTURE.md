# Architecture

Living structural map of the system as of 2026-10-25.
Overwritten when structural changes occur during a session.

## Overview

opencode-helpers is a template repository providing standardized skills,
agents, commands, scripts, and knowledge persistence patterns for AI-assisted
development workflows in opencode. Skills in `skills/` contain all workflow
logic (and, for the search skills, their own MCP servers); the thin command layer in
`commands/` delegates to skills. Global agents live in `agents/` as flat
`<name>.md` files (linked via `~/.config/opencode/agents`). Utility scripts
live in `scripts/` (retired ones in `scripts/archive/`). Executable code is
covered by a hermetic `unittest` suite in `tests/`. Session context is
persisted to a structured set of knowledge files in `docs/ai/`.

## Agents (`agents/`)

| Agent | Purpose | Model |
|-------|---------|-------|
| `lehrplan-annotator` | Authors the Erläuterungs-Ebene (KM-Überblicke, Lernziel- und Lehrstoff-Erläuterungen as blockquote annotations) for HTL curriculum extracts per the `lehrplan` skill's quality criteria; law text stays untouched | `opencode-go/glm-5.3` (non-flash — explanation authoring needs the strongest language model) |

## Commands (`commands/`)

| Command | Purpose | Delegates to |
|---------|---------|-------------|
| `/improve` | Planning-only analysis of commands/skills for inconsistencies | none |
| `/knowledge-assess` | Assess student knowledge-check submissions | `knowledge-assessment` |
| `/knowledge-exam` | Generate a German mini-exam from Git history | `knowledge-exam` |
| `/knowledge-persist` | Persist session context into docs/ai/ files | `knowledge-persistence` |
| `/nextprompt` | Run `aitranscribe -q` and treat output as next instruction | none (external tool) |
| `/tmpissue` | Create a GitHub issue from /tmp/issue.md, then delete it | none (`gh` CLI) |

## Scripts

| Script | Purpose |
|--------|---------|
| `skills/deepseek-search/scripts/opencode-deepseek-search` | MCP server (Python 3, stdlib only) providing the `deepseek_search` tool: DeepSeek Search API primary, SearXNG chain as fallback; routes SearXNG-only parameters (category/engines/pageno/safesearch) straight to the fallback |
| `skills/searxng/scripts/opencode-searxng` | MCP server (Python 3, stdlib only) providing the `searxng_search` tool with category/engine/time-range/safesearch filtering — still the tool on hosts that run SearXNG only (school) |
| `skills/searxng/searxng-search.sh` | Canonical SearXNG search logic (also the fallback backend of `deepseek-search`): prioritized engine chain against the SearXNG instance chain (`brave` → `google` → `mwmbl,searchmysite` → token-gated `braveapi`), returns JSON on stdout |
| `skills/full-sync/scripts/full-sync.sh` | Multi-repo sync: fetch every remote, fast-forward/rebase clean checkouts onto their upstream, prune dead secondary remotes, `svn up`; never commits or pushes. `--host-steps` refreshes the host: apt update/upgrade, restart of the configured user services, reboot when pending — gated on a clean sync report |
| `skills/full-sync/scripts/test-full-sync.sh` | Shell self-test for `full-sync.sh` against throwaway bare remotes/clones (23 checks; no real repository touched) |
| `scripts/archive/` | Retired scripts (`opencode-searxng` legacy requests server, `opencode-ollama-sync`) — kept unregistered for reference |

## Tests (`tests/`)

Hermetic, stdlib-only `unittest` suite for the repo's executable code. Run with
`python3 -m unittest discover -s tests -v` — no network, no live instance.
Skills whose logic is stateful also ship a standalone shell self-test next to
the script (precedent: `skills/full-sync/scripts/test-full-sync.sh`).

| File | Purpose |
|------|---------|
| `tests/searxng_mock.py` | In-process mock of the SearXNG JSON API plus a helper that points a temp copy of `searxng-search.sh` at it |
| `tests/deepseek_search_mock.py` | In-process mock of the DeepSeek Search API (`POST /v1/tools/search`), scriptable per request (status/body/queue) |
| `tests/test_deepseek_search_mcp.py` | Provider chain end to end: DeepSeek success, missing key, every fallback trigger (402/408/429/5xx/network/empty), fatal 4xx, SearXNG-only routing, operator/`time_range` mapping, query truncation, envelope keys |
| `tests/test_skill_frontmatter.py` | Visibility guard: hidden skills carry `metadata.opencode/autoinvoke: false`, no inert `slash:` field, exactly one advertised search skill |
| `tests/test_full_sync.py` | `full-sync.sh`: report keys, fetch/ff/rebase pull decisions, dead-remote pruning, credential redaction in report *and* log, exit codes, `max_depth`, svn status without committing, `--host-steps` gate |
| `tests/test_searxng_search.py` | `searxng-search.sh` behavior: chain tiers (`brave`/`google`/free), the `< 3` token gate + merge/dedupe, explicit-engine/category bypass, preserved params, instance chain, first-responsive-instance reuse |
| `tests/test_opencode_searxng.py` | MCP protocol (`initialize`/`tools/list`) and hermetic `tools/call` integration in a temp skill layout |
| `tests/test_skill_links.py` | Every `](./…)` link in a `skills/*/SKILL.md` resolves to an existing sibling file |

## Skills (`skills/`)

| Skill | Purpose | Invocation |
|-------|---------|------------|
| `code-review` | Review changes since a fixed point along standards and spec axes via parallel sub-agents | Direct ("review since X") |
| `codebase-audit` | One-shot whole-repo audit across four axes (security in depth, structure/layers, coupling/entanglement, architecture) via parallel sub-agents, ending in an epic with formally linked sub-issues | Natural language ("audit the codebase") |
| `domain-modeling` | Build and sharpen a project's domain model (CONTEXT.md, ADRs) | Direct invocation |
| `fork-policy` | Enforce clean-main branch policy on forked repositories | On-demand invocation |
| `grading-shared` | Shared protocols: address style, email formulas, DB lookup, homework discovery, bulk concurrency, German/UTF-8 rules, email body format, praise guidelines, reporting | Referenced by `repograde`, `knowledge-assessment`, `projectgrade` |
| `grill-me` | Relentless interview to sharpen a plan or design | Natural language ("grill me") |
| `grill-with-docs` | Grilling plus ADR/glossary docs created along the way | Natural language ("grill") |
| `grilling` | Relentless interview to stress-test a plan, decision, or idea | Natural language ("grill") |
| `homework` | Generate per-lesson `Hausübung.md` files from Git history | Direct invocation from class folder |
| `issue-workflow` | Continuous issue awareness (always work under an issue), proactive issue-linked commit/push (green commits only), completion/auto-close criteria; `start`/`commit`/`finish` remain as manual override modes. Mandatory **Duplicate-Check gate** before every issue creation (repo-local issue + PR search, decision matrix, `Duplicate check (YYYY-MM-DD): …` trace line). Treats the knowledge-persistence commit as part of the flow (no empty commit after it) and expects a post-close knowledge follow-up commit | Continuous + natural language override triggers (no slash command) |
| `knowledge-assessment` | Assess student knowledge-check submissions, produce grading reports and email payloads | `/knowledge-assess` |
| `knowledge-exam` | Generate German knowledge-check exams and solution files | `/knowledge-exam` |
| `knowledge-persistence` | Persist session context into structured docs/ai/ knowledge files; **always ends with its own commit + push** of the knowledge files (issue-referenced; `svn ci` in SVN), never closes issues | `/knowledge-persist` or natural language triggers ("persist knowledge") |
| `orchestration` | Scope-gated coordination for large work: decompose into sub-issues, delegate implementation to sub-agents, verify behind a hard test gate | Natural language ("large", multi-session work) |
| `projectgrade` | Grade student project repositories holistically based on Git commits, GitHub Issues, Pull Requests, and further measurable contributions | Direct skill invocation |
| `repograde` | Grade student repositories (full or date-filtered) in single-repo or bulk mode with plan presentation | Direct skill invocation |
| `deepseek-search` | Web search via the DeepSeek Search API with the SearXNG engine chain as fallback; without a key the chain is SearXNG only. Owns the `deepseek_search` MCP server | MCP tool (the only advertised search skill) |
| `searxng` | Backend manual of the SearXNG chain (instance/credential contract, engine tiers, envelope diagnostics); owns `searxng-search.sh` and the `searxng_search` MCP server for SearXNG-only hosts | Hidden (`metadata.opencode/autoinvoke: false`), loadable via `@searxng`; its MCP tool stays registered where hosts run SearXNG only |
| `sync-upstream-skills` | Re-transplant owned skills from the mattpocock upstream after a git pull; checks duplicate names and dangling references | Natural language ("sync skills") |
| `teach` | Teach the user a new skill or concept | Direct invocation |
| `lehrplan` | Austrian HTL teaching repos: Gegenstand identification incl. conformity check, RIS sync with Novellen-Check (NOR-Kopf method), year-wise curriculum extraction into `lehrplan/` | Natural language ("Unterricht", "RIS sync", "Lehrplan extrahieren") |

Long reference material lives in sibling files next to a skill's `SKILL.md`, linked as `[X.md](./X.md)` and loaded only on demand: `codebase-audit/{AXES,TOOLS}.md`, `grading-shared/EMAIL-EXAMPLES.md`, `knowledge-persistence/FILE-TEMPLATES.md`, `lehrplan/{KLASSEN-ZUORDNUNG,SPENGERGASSE-KLASSEN,RIS-PRAXIS,ERLAEUTERUNGS-QUALITAET}.md`, `repograde/REPORT-FORMAT.md`, `projectgrade/REPORT-FORMAT.md`. The links are guarded by `tests/test_skill_links.py`.

## Knowledge Files (`docs/ai/`)

| File | Purpose | Update mode |
|------|---------|------------|
| HANDOFF.md | Open tasks for next session | Overwrite |
| DECISIONS.md | Active decisions still in force | Append; prune superseded → HISTORY.md |
| ARCHITECTURE.md | Living structural map of the current system | Overwrite |
| CONVENTIONS.md | Ongoing coding rules, patterns, and style agreements | Append |
| PITFALLS.md | Hard-won failure knowledge and non-obvious constraints | Append |
| DOMAIN.md | Business/teaching-domain rules | Append |
| STATE.md | Current project status snapshot | Overwrite |
| HISTORY.md | Chronological archive of superseded decisions and pruned entries | Append-only |

## Data Flows

- `commands/*.md` → `skills/<name>/SKILL.md`: Commands pass user arguments and constraints into skills for execution.
- `grading-shared` → `repograde`/`knowledge-assessment`/`projectgrade`: Shared protocols injected via skill reference at runtime.
- `skills/*` → `docs/ai/*`: Knowledge-persistence skill writes session context into knowledge files, then commits + pushes them (issue-referenced) — the run is only complete once they are on the trunk.
- `docs/ai/*` → agent bootstrap: AGENTS.md instructs agents to read knowledge files before starting any task.
- `repograde` bulk mode: fan-out to concurrent subagents → per-repo artifact files → fan-in aggregation into shared EMAIL.json.
- `skills/deepseek-search/scripts/opencode-deepseek-search` (MCP) → OpenCode: exposes the `deepseek_search` tool. It calls the DeepSeek Search API (`POST <DEEPSEEK_SEARCH_API_BASE or https://api.deepseek.com>/v1/tools/search`) and, when no key is configured or the call fails (402/408/429/5xx/network/empty), shells out to `skills/searxng/searxng-search.sh`. The envelope reports `provider`, `fallback_used`/`fallback_reason`, `providers_tried`/`providers_unavailable`; on the SearXNG path the engine-level flag is `engine_fallback_used`.
- `skills/searxng/scripts/opencode-searxng` (MCP) → OpenCode: exposes the `searxng_search` tool to all agents via JSON-RPC; the server shells out to `skills/searxng/searxng-search.sh` per call, which queries the instances configured in the **host overlay** (`SEARXNG_PRIMARY`/`SEARXNG_FALLBACK` in `mcp.searxng.environment`) — the skill itself ships no endpoints (#112).
- `skills/searxng/searxng-search.sh` prioritized chain: for general searches it stops at the first tier that returns results — `bing`, then `yahoo`, then the free `mwmbl,searchmysite`, and finally `engines=braveapi` **only** when `bing` and `yahoo` both failed and the free tier yielded fewer than 3 hits. `bing` is the **only** engine that serves normal results; `yahoo`, the free tier and `braveapi` are **fallback-only**. `braveapi` results are merged ahead of the free results (URL-deduplicated); the answer carries `engine_used`/`fallback_used`/`tried`/`unresponsive_engines`. An explicit `engines=` argument bypasses the chain; the profile `SEARXNG_CHAIN=strict` skips the free tier. (`brave`/`google` were the chain until 2026-10-08; both went upstream-broken: `google`'s engine calls the retired `/wml/search` endpoint → 403, searxng#5867; `brave` → 429.)
- SearXNG access control: the public vhost requires **HTTP Basic Auth** (shared secret in `/etc/nginx/searxng.htpasswd`) for both UI and API, and nginx applies `limit_req`/`limit_conn`. The container port `8888` is published only on `127.0.0.1`, so the instance is reachable solely through nginx. `/robots.txt` is served **without** auth (`location = /robots.txt`, `Disallow: /`) and every response carries `X-Robots-Tag: noindex, nofollow, noarchive` (the backend's own `X-Robots-Tag` is hidden with `proxy_hide_header`). The vhost logs to dedicated files (`/var/log/nginx/searxng.access.log`, custom `searxng` format incl. `rt=`, and `searxng.error.log`) rather than the shared `access.log`. Clients authenticate by reading `~/.config/opencode/searxng.cred` (or `$SEARXNG_AUTH`) in `searxng-search.sh`. Intended clients: claw, think, dell.
- Search deployment on **think** (2026-10-25): the host registers `mcp.deepseek.environment` with `DEEPSEEK_SEARCH_API_KEY_FILE` (key file mode `600`) and no `mcp.searxng` block any more; the tool is `deepseek_search`. The repo `opencode.json` deliberately carries **no** `mcp` block — MCP registration is host-local, so a project-level config cannot shadow the host overlay; the template is `skills/deepseek-search/env.sample`. Historic reference (#74, superseded 2026-10-25): the `mcp.searxng` overlay used `SEARXNG_PRIMARY=http://10.8.0.16` (Gregor school instance — VPN `tun0`, port 80, no auth) with `SEARXNG_CHAIN=strict` (profile name `gregor` until 2026-10-08, when the chain became `bing` → `yahoo` → `braveapi`), plus `SEARXNG_FALLBACK=https://searx.graf.priv.at` (until 2026-10-25 `searxng.claw.graf.priv.at`) authenticated via `SEARXNG_FALLBACK_CRED_FILE` (`~/.config/opencode/searxng.cred`). Purpose/rollout: Gregor is the school's **agentic** search instance — think live, dell replication next, then student agents (see DECISIONS.md 2026-09-17); no browser-UI role for student use.

## Host Services: OpenCode Server & Telegram Bot

Every host runs OpenCode V2 as a **user** systemd unit (templates:
`dotfiles/systemd/user/`, install notes next to them):

- `opencode.service` → `opencode serve --service` (`ExecStartPre` auto-upgrade,
  `Restart=on-failure`, `UMask=0077`). The server binds **`127.0.0.1` only** and
  is password-protected (HTTP Basic Auth, user `opencode`, password in
  `~/.config/opencode/service.json`; `opencode service get password`). Port:
  host-pinned via `opencode service set port` or the V2 default `49374`.
- `oc-tg-bot-<host>.service` → one Telegram bot per host
  (`npx @grinev/opencode-telegram-bot@latest`), app home
  `OPENCODE_TELEGRAM_HOME=~/.config/oc-tg-bot-<host>` (`.env` mode 600,
  `settings.json`, `logs/`), `Restart=always`. Access is gated by
  `TELEGRAM_ALLOWED_USER_ID`; voice prompts are transcribed via Groq
  (`STT_MODEL=whisper-large-v3`, quality-first — see DECISIONS.md 2026-10-17).

`sudo loginctl enable-linger "$USER"` is **mandatory** on every host, otherwise
the units never start after a reboot or without an open login. The shared shell
layer (`dotfiles/bash_functions.sh`) addresses exactly these unit names
(`oc-restart`, `su-*`), and the `full-sync` host steps restart
`opencode.service` plus the `oc-tg-bot-*` units (both upgrade themselves on
restart: `opencode upgrade` in `ExecStartPre`, `npx …@latest` for the bot).

| Host | Server | Bot | Notes |
|------|--------|-----|-------|
| gregor | `127.0.0.1:4096` (pinned) | `oc-tg-bot-gregor` | reference setup |
| kik | `127.0.0.1:49374` (V2 default) | `oc-tg-bot-kik` (`@schurlix_kik_bot`) | installed 2026-10-17 (#111) |

## SearXNG Egress

Outgoing search-engine traffic from the self-hosted SearXNG instance (claw)
does not leave via claw's datacenter IP. It is routed through the school
network:

```
SearXNG (claw) ──VPN (tun0)──> tinyproxy on gregor (10.8.0.16:1080) ──> internet
                                                                        (egress: 192.189.51.211)
```

- Egress IP `192.189.51.211` is the HTL Spengergasse school network.
- Configured globally in the instance's `settings.yml` under
  `outgoing.proxies` (`all://` → `http://10.8.0.16:1080`); every engine goes
  through it.
- **Reason:** claw's datacenter IP (`85.215.162.182`) is bot-blocked or served
  garbage by most engines; the school IP is treated like normal user traffic.
  `google` — the secondary scraper engine in the chain — only works via this egress.
- tinyproxy listens only on the VPN interface (`Listen 10.8.0.16`,
  `Allow 10.8.0.0/24`) with a systemd `Restart=always` drop-in.
- **Failure mode:** if tinyproxy/VPN is down, all engines return 0 results;
  recovery is automatic via systemd restart.
- Egress check: `curl --proxy http://10.8.0.16:1080 https://api.ipify.org`
  must return `192.189.51.211`.
- `braveapi` (Brave Search API, prepaid plan) is retained as the only
  non-scraper general engine — an independent-index, token-gated fallback
  immune to the HTML bot-blocking the scraper engines hit. It pauses when its
  monthly free credit is exhausted and revives automatically.

This is backend deployment knowledge. The portable `searxng` skill only notes
the 0-results failure mode; operational pitfalls live in `PITFALLS.md`.
