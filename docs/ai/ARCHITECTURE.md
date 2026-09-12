# Architecture

Living structural map of the system as of 2026-09-10.
Overwritten when structural changes occur during a session.

## Overview

opencode-helpers is a template repository providing standardized skills,
agents, commands, scripts, and knowledge persistence patterns for AI-assisted
development workflows in opencode. Skills in `skills/` contain all workflow
logic (and, for `searxng`, their own MCP server); the thin command layer in
`commands/` delegates to skills. Global agents live in `agents/` as flat
`<name>.md` files (linked via `~/.config/opencode/agents`). Utility scripts
live in `scripts/` (retired ones in `scripts/archive/`). Session context is
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
| `/security` | Generate a project security review report | none |
| `/tmpissue` | Create a GitHub issue from /tmp/issue.md, then delete it | none (`gh` CLI) |

## Scripts

| Script | Purpose |
|--------|---------|
| `skills/searxng/scripts/opencode-searxng` | MCP server (Python 3, stdlib only) providing the `searxng_search` tool with category/engine/time-range/safesearch filtering |
| `skills/searxng/searxng-search.sh` | Canonical search logic: curl against the SearXNG instance chain, returns JSON on stdout |
| `scripts/archive/` | Retired scripts (`opencode-searxng` legacy requests server, `opencode-ollama-sync`) — kept unregistered for reference |

## Skills (`skills/`)

| Skill | Purpose | Invocation |
|-------|---------|------------|
| `code-review` | Review changes since a fixed point along standards and spec axes via parallel sub-agents | Direct ("review since X") |
| `domain-modeling` | Build and sharpen a project's domain model (CONTEXT.md, ADRs) | Direct invocation |
| `fork-policy` | Enforce clean-main branch policy on forked repositories | On-demand invocation |
| `grading-shared` | Shared protocols: address style, email formulas, DB lookup, homework discovery, bulk concurrency, German/UTF-8 rules, email body format, praise guidelines, reporting | Referenced by `repograde`, `knowledge-assessment`, `projectgrade` |
| `grill-me` | Relentless interview to sharpen a plan or design | Natural language ("grill me") |
| `grill-with-docs` | Grilling plus ADR/glossary docs created along the way | Natural language ("grill") |
| `grilling` | Relentless interview to stress-test a plan, decision, or idea | Natural language ("grill") |
| `homework` | Generate per-lesson `Hausübung.md` files from Git history | Direct invocation from class folder |
| `issue-workflow` | Issue lifecycle management (start, checkpoint, finish) with mandatory issue-linked commits | Natural language triggers (no slash command) |
| `knowledge-assessment` | Assess student knowledge-check submissions, produce grading reports and email payloads | `/knowledge-assess` |
| `knowledge-exam` | Generate German knowledge-check exams and solution files | `/knowledge-exam` |
| `knowledge-persistence` | Persist session context into structured docs/ai/ knowledge files | `/knowledge-persist` or natural language triggers ("persist knowledge") |
| `orchestration` | Orchestrate sub-agents to decompose, delegate, and deliver work via issue-driven task decomposition | Direct invocation |
| `projectgrade` | Grade student project repositories holistically based on Git commits, GitHub Issues, Pull Requests, and further measurable contributions | Direct skill invocation |
| `repograde` | Grade student repositories (full or date-filtered) in single-repo or bulk mode with plan presentation | Direct skill invocation |
| `searxng` | Web search via the self-hosted SearXNG instance; owns the `searxng_search` MCP server and the standalone `searxng-search.sh` | MCP tool (automatic in all agents) plus direct invocation |
| `sync-upstream-skills` | Re-transplant owned skills from the mattpocock upstream after a git pull; checks duplicate names and dangling references | Natural language ("sync skills") |
| `teach` | Teach the user a new skill or concept | Direct invocation |
| `telegram-send` | Send files/documents/photos to the user's Telegram chat via the local Bot API, using the running bot's credentials from `~/.config/oc-tg-bot*/.env` | Natural language triggers ("schick mir X ins Telegram", "send file to Telegram") |
| `lehrplan` | Austrian HTL teaching repos: Gegenstand identification incl. conformity check, RIS sync with Novellen-Check (NOR-Kopf method), year-wise curriculum extraction into `lehrplan/` | Natural language ("Unterricht", "RIS sync", "Lehrplan extrahieren") |

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
- `skills/*` → `docs/ai/*`: Knowledge-persistence skill writes session context into knowledge files.
- `docs/ai/*` → agent bootstrap: AGENTS.md instructs agents to read knowledge files before starting any task.
- `repograde` bulk mode: fan-out to concurrent subagents → per-repo artifact files → fan-in aggregation into shared EMAIL.json.
- `skills/searxng/scripts/opencode-searxng` (MCP) → OpenCode: exposes the `searxng_search` tool to all agents via JSON-RPC; the server shells out to `skills/searxng/searxng-search.sh` per call, which queries the instance chain `https://searxng.claw.graf.priv.at` → `etsi.me` → `baresearch.org` (no localhost entry — the skill runs on multiple hosts).

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
  `google` — the primary general engine — only works via this egress.
- tinyproxy listens only on the VPN interface (`Listen 10.8.0.16`,
  `Allow 10.8.0.0/24`) with a systemd `Restart=always` drop-in.
- **Failure mode:** if tinyproxy/VPN is down, all engines return 0 results;
  recovery is automatic via systemd restart.
- Egress check: `curl --proxy http://10.8.0.16:1080 https://api.ipify.org`
  must return `192.189.51.211`.
- `braveapi` (Brave Search API, prepaid plan) is retained as the only
  non-scraper general engine — an independent-index fallback immune to the
  HTML bot-blocking the scraper engines hit. It pauses when its monthly free
  credit is exhausted and revives automatically.

This is backend deployment knowledge. The portable `searxng` skill only notes
the 0-results failure mode; operational pitfalls live in `PITFALLS.md`.
