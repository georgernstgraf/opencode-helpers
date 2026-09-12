# Pitfalls

Things that do not work, subtle bugs, and non-obvious constraints.
Read this file carefully before making changes in affected areas.

## General

- Always read existing files before editing - OpenCode requires this.
- Never assume a library is available - check imports/package files first.
- OpenCode may show linked skills as `None` when `SKILL.md` files are missing required YAML frontmatter.
- Do not move runtime-critical skill instructions into adjacent helper Markdown files unless skill loading is known to include them.
- Do not allow issue workflow commits without a GitHub issue number in the commit message.
- Never close an issue that has open sub-issues. Always list sub-issues and verify all are closed before closing.
- When passing Markdown with backticks to `gh issue create` or `gh issue comment` through the shell, quote it safely or the shell may try to execute the backticked fragments before posting the content.
- OpenCode has no built-in throttling for parallel sub-agent execution - use dynamic concurrency with a maximum limit and ~3 second delays between agent starts to avoid overwhelming API rate limits.
- When removing or renaming a skill, update every dependent command, agent, README entry, and knowledge file in the same change or stale workflow references remain behind.
- `~/.config/opencode/skills` is a symlink to the repo's `skills/` directory; editing one location updates both automatically. Full chain: `~/.config/opencode/skills` → `~/repos/georgernstgraf/opencode-helpers/skills`.
- `~/.config/opencode/agents` is a symlink to the repo's `agents/` directory (same pattern as skills). opencode's agent loader scans `{agent,agents}/**/*.md` recursively with `symlink: true` — **every** `.md` in that tree becomes an agent, so never add README or auxiliary Markdown files to `agents/`.
- Host-local endpoints in shared skills break off-host: `localhost:8888` only resolves on the SearXNG host (claw). The searxng skill therefore uses `https://searxng.claw.graf.priv.at` as primary instance — never add localhost entries to shared tooling.
- When refactoring shared content into `grading-shared`, keep grading-specific logic (date filtering, homework weighting) in the consuming skill — only truly shared protocols belong in `grading-shared`.
- The `repograde` skill now handles both full-history and date-filtered grading; there is no separate `repogradesince` skill or command.
- Reference/illustrative material may live in sibling `*.md` files next to a `SKILL.md` (loaded on demand; the skill loader reads only `SKILL.md`). Runtime-critical instructions must stay in `SKILL.md`; sibling content must be linked as `[X.md](./X.md)`. `tests/test_skill_links.py` validates every `](./…)` link in `skills/*/SKILL.md` only — illustrative `./src/...` links inside sibling format templates are intentionally not checked.
- When extracting a section that contains a fenced code block with Markdown headings, promote heading levels fence-aware (track the ` ``` ` toggles) — a blanket `###`→`##` replace corrupts headings inside the template code block.

## SearXNG Backend

- SearXNG egress goes through a tinyproxy on host gregor (school IP). If **all** engines return 0 results, suspect the proxy/VPN first — not the skill or MCP server. Egress check: `curl --proxy http://10.8.0.16:1080 https://api.ipify.org` must return `192.189.51.211`.
- tinyproxy: use `Listen 10.8.0.16` (listening socket), **never** `Bind` — `Bind` forces the outgoing source IP and would push egress into the VPN tunnel. The user directive is `User`; `UserName` is invalid syntax.
- In this SearXNG instance, `disabled: true` excludes an engine from default queries but keeps it explicitly selectable (`engines=<name>` or `!<bang>`); `inactive: true` removes it entirely. `disabled: true` alone does **not** remove an engine (it stays reachable via explicit `engines=`) — to remove, drop it from `keep_only` **and** delete its custom block.
- SearXNG has **no native conditional fallback**: `weight` only re-ranks the merged results and all engines of a category run in parallel. The Brave fallback is therefore implemented in `skills/searxng/searxng-search.sh` (phase 2), not in the instance.
- SearXNG **ignores `engines=` when `categories=` is also present** (the category wins). Always send `engines` without a category. This silently broke explicit engine selection in the wrapper until the two parameters were split.
- `braveapi` is `disabled: true` in `settings.yml` so ordinary searches skip it (no quota burn); the wrapper selects it per request via `engines=braveapi`. Verified 2026-09-12: a disabled engine is still selectable this way. Plan B if that ever changes: prefix the query with the `!braveapi` bang.
- SearXNG's default `disabled: true` for `google` must be overridden with explicit `disabled: false` in `settings.yml` for the engine to work.
- `bing` web and `yahoo` were removed 2026-09-12: `bing` web returned random or spam results non-deterministically, `yahoo` produced an lxml ParserError (no parseable HTML). Do not re-enable without testing.
- Brave Search API billing: new activations are **prepaid-only**; existing postpaid plans are grandfathered (unchanged) but **cannot be reactivated after cancellation** — cancelling means only prepaid is available afterwards. **Switching a plan means the old API key stops working; a new key must be generated** and put into `settings.yml`.
- Brave gives **$5 in free credits per plan, per month** — not per billing model. Running postpaid + prepaid versions of the same plan does **not** yield double $5; the credit moves to the prepaid plan.
- Prepaid pauses at $0 balance; postpaid keeps billing pay-as-you-go beyond the included credits (set a usage limit if kept).
- Diagnosing `braveapi` suspensions: `unresponsive: braveapi → "Suspended: access denied"` means **key/auth** (wrong/old key). HTTP 402 `code: CREDIT_EXHAUSTED` with `current_balance_units < min_request_cost_units` means **insufficient credit**. After a top-up the engine revives automatically on the next query — **no `docker restart` needed**, because the key in `settings.yml` is unchanged.

## Database

- Class lookup in `uploadthing.db` is case-sensitive; `klasse` column stores uppercase (e.g., "2AHWII") but `grading-shared` config uses lowercase ("2ahwii"); always use `UPPER(klasse)` comparison.

## Grading Workflow

- Never assume grading runs from within a Git repository - it operates from a local folder (CWD).
- `projectgrade` is the exception: it MUST run from within a Git repository (the project being evaluated).
- `git branch -a` only shows existing branches; `projectgrade` must also recover contributions from deleted branches via merge commit history and GitHub PR API.
- `Hausübungen.md` (legacy) is always in the CWD, never inside a student repository.
- `Hausübungen.md` (legacy) may be a symbolic link; follow symlinks when reading.
- Per-lesson `Hausübung.md` files live inside `<date>_<topic>` directories; grading skills must discover both formats.
- Student repositories must already exist locally; never attempt to clone them.
- If any student repository has uncommitted changes, grading must stop immediately.
- All grading skills use `<name>_grading.md` pattern; `INDIVIDUAL.md` is deprecated.
- `knowledge-assessment` outputs `GRADINGS.md` and `CLASS.md` (both mandatory) plus per-student `<name>_grading.md` files.
- Email bodies must be plain ASCII text — no Markdown headers, bold, tables, or lists in email JSON bodies; only code blocks with backtick fences are allowed.
- The `repograde` skill is invoked directly (no command wrapper); it handles full-history and date-filtered grading in one skill.
- The `projectgrade` skill is invoked directly (no command wrapper); it uses holistic descriptive grading, not numeric weights.
- **Agents frequently attempt to write Python or bash scripts to automate student evaluation.** This produces machine-like, impersonal grades that fail to capture the unique nuances of individual student submissions. Grading must always be done through direct AI reasoning — never through scripts, test runners, linters, or automated checkers. The agent itself is the evaluator.

## Project Configuration

- OpenClaw-specific configuration (agent binding, Telegram groups, memory settings) belongs in OpenClaw's channel config, not in `AGENTS.md` or other project files.
- Project `AGENTS.md` should contain only project-relevant instructions and conventions.
- Searching for "latest" technologies or software versions (e.g., "Gemma 4") without a `time_range` or exact quoting (`"Gemma 4"`) often returns irrelevant legacy documentation due to higher domain authority of old sites (e.g., Firefox 4, MDN). Always check if a time filter is needed for brand-new topics.
