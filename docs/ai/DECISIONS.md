# Architectural Decisions

Records architectural and technical decisions with rationale.
Each entry documents WHAT was decided and WHY.

## 2026-03-04: Use docs/ai/ for knowledge persistence
- **Choice**: Store knowledge files in `docs/ai/` directory
- **Reason**: Follows common docs structure, keeps AI context with other documentation
- **Considered**: `_agents/`, `.opencode/knowledge/`
- **Tradeoff**: Slightly longer path, but more discoverable

## 2026-03-06: Use OpenCode YAML frontmatter for skill discovery
- **Choice**: Add OpenCode skill metadata directly to each `skills/<name>/SKILL.md`
- **Reason**: OpenCode only exposes linked skills when `SKILL.md` starts with valid frontmatter containing `name` and `description`
- **Considered**: Separate metadata files, leaving linked skill directories without metadata
- **Tradeoff**: Skill docs must carry a small metadata header, but discovery works reliably

## 2026-03-10: Keep skills self-contained for runtime loading
- **Choice**: Avoid factoring runtime-critical skill instructions into adjacent shared Markdown helper files
- **Reason**: Skills are loaded via the `skill` tool from global OpenCode config, so standalone `SKILL.md` files are safer than sidecar references
- **Considered**: A shared `skills/_shared/` folder for cross-skill teaching context
- **Tradeoff**: Some content repetition remains, but runtime behavior is more reliable and portable

## 2026-03-14: Centralize issue commands behind a dedicated workflow skill
- **Choice**: Refactor `issue-start`, `issue-commit`, and `issue-finish` into thin command wrappers around a shared `issue-workflow` skill
- **Reason**: The issue lifecycle rules, GitHub interactions, and commit requirements should stay consistent across all issue-oriented commands
- **Considered**: Keeping separate embedded instructions in each command file
- **Tradeoff**: The skill becomes broader, but maintenance is simpler and behavior stays aligned

## 2026-03-18: Consolidate repo-report into repograde
- **Choice**: Absorb the former `repo-report` analysis workflow into `skills/repograde/SKILL.md`
- **Reason**: Repository grading should have one authoritative skill, while `/repograde` stays a thin command wrapper and both single-repo and bulk mode share the same logic
- **Considered**: Keeping a separate generic analysis skill, or preserving the older agent-plus-skill split
- **Tradeoff**: The repograde skill becomes broader, but the grading workflow is clearer and easier to maintain

## 2026-03-19: Repograde writes basename-derived artifact files only
- **Choice**: In `repograde`, generate only `<basename>_grading.md` and `<basename>_email.json` per repository, and reserve shared `EMAIL.json` for the bulk-mode master aggregation step
- **Reason**: Artifact-based outputs are clearer than mutating `INDIVIDUAL.md` or `CLASS.md`, and they make the subagent/master split explicit in bulk mode
- **Considered**: Continuing to write `INDIVIDUAL.md` or `CLASS.md`, or allowing subagents to append directly to shared `EMAIL.json`
- **Tradeoff**: Bulk mode needs an explicit fan-in aggregation step, but per-repository outputs are simpler and less error-prone

## 2026-03-18: Dynamic concurrency for RepoGrader sub-agents
- **Choice**: Execute RepoGrader agents with dynamic concurrency (default 4 concurrent), starting the next agent immediately after one completes (with ~3 second delay)
- **Reason**: Maintains maximum throughput while keeping concurrent agents at a safe limit; OpenCode has no built-in throttling
- **Considered**: Batched execution (wait for all to complete before next batch), fully parallel or fully sequential execution
- **Tradeoff**: More complex than simple batching, but maximizes throughput without overwhelming API limits

## 2026-03-18: Centralize grading configuration in grading-shared skill
- **Choice**: Create `skills/grading-shared/SKILL.md` as single source of truth for class-to-address-style mapping, email formulas, and database patterns
- **Reason**: Both `knowledge-assessment` and `repograde` were duplicating class lists, email greetings/closings, and database lookup patterns
- **Considered**: Keeping configuration duplicated in each skill, or using a JSON config file
- **Tradeoff**: One more skill file, but eliminates duplication and ensures consistency across grading workflows

## 2026-03-21: Require second-person address (Du/Sie) in all grading content
- **Choice**: All grading content (grading reports, INDIVIDUAL.md, email bodies) must address students directly in second person, matching the class-based email salutation style
- **Reason**: Third-person address ("the student has...") is inconsistent with email salutations and feels impersonal; students should be addressed directly
- **Considered**: Mixed third-person in reports with second-person in emails, or only second-person in emails
- **Tradeoff**: Requires careful grammar (Sie vs Du conjugation in German), but creates consistent student experience

## 2026-03-23: Replace INDIVIDUAL.md with per-student grading files
- **Choice**: All grading skills use `<name>_grading.md` pattern instead of a single `INDIVIDUAL.md` file
- **Reason**: Consistent output pattern across all grading skills (repograde, knowledge-assessment, projectgrade); per-student files are easier to manage and align with `<basename>_grading.md` convention
- **Considered**: Keeping `INDIVIDUAL.md` for knowledge-assessment only, or using a different naming scheme
- **Tradeoff**: More files to manage in knowledge-assessment, but consistency across all grading workflows
- **Affected skills**: `knowledge-assessment` (now outputs `<name>_grading.md` instead of `INDIVIDUAL.md`)
- **Retained outputs**: `GRADINGS.md` and `CLASS.md` remain mandatory for knowledge-assessment

## 2026-03-27: Add mandatory exam-date parameter to knowledge-exam skill
- **Choice**: Require teachers to specify the exam date when generating knowledge-check exams
- **Reason**: Exams are created ahead of time for a specific planned date; using today's date by default led to mismatches between filename dates and actual exam dates
- **Considered**: Keeping today's date as default, or making exam-date optional with a prompt
- **Tradeoff**: One more required parameter, but ensures exam files are correctly dated from the start
- **Accepted formats**: ISO date (YYYY-MM-DD), literal `today`, or literal `tomorrow`

## 2026-04-01: Separate issue lifecycle from knowledge-persistence
- **Choice**: Add an explicit Issue Safety constraint to `knowledge-persistence` prohibiting it from closing, reopening, or changing issue state; add a new "Comment on Active Issue" step for traceability without closure
- **Reason**: Standalone invocation of knowledge-persistence was closing active GitHub issues because the skill had no constraint against it and the purpose language implied finality
- **Considered**: Relying on agent judgment alone, or making knowledge-persistence completely silent on issues
- **Tradeoff**: Skill is slightly more complex, but issue lifecycle ownership is now unambiguous

## 2026-04-01: Unify homework skills into per-lesson homework generation
- **Choice**: Merge `/homework` and `/homework-improve` into a single `homework` skill with no command wrapper. The skill generates per-lesson `Hausübung.md` (singular) files inside `<YYYY-MM-DD>_<topic>` lesson directories, invoked directly from inside the class folder.
- **Reason**: Two commands with confusing names, different output modes (read-only vs file-writing), and similar but divergent logic were unintuitive. Per-lesson files give students a single focused document instead of a cumulative file.
- **Considered**: Keeping two commands with better names; making one smart command with a mode flag; keeping cumulative `Hausübungen.md` format
- **Tradeoff**: Legacy `Hausübungen.md` files continue to exist in older class folders; grading skills must now support both formats (dual-source discovery)
- **Removed**: `commands/homework.md`, `commands/homework-improve.md`, `skills/homework-improve/SKILL.md`
- **Affected skills**: `homework` (rewritten), `repograde` (dual-source homework), `repogradesince` (dual-source homework)

## 2026-04-02: Add /improve command for repository self-analysis
- **Choice**: Create a planning-only `/improve` command that scans all commands and skills for inconsistencies, redundancies, stale references, and structural issues. Display findings to user without editing files.
- **Reason**: Manual cross-file analysis is error-prone as the repository grows; a repeatable command ensures quality checks are on-demand
- **Considered**: A lint-style script, automated CI checks, or relying on manual review
- **Tradeoff**: Command depends on agent judgment rather than deterministic parsing, but catches semantic issues that scripts cannot

## 2026-04-02: Factor shared grading protocols into grading-shared
- **Choice**: Move repository analysis protocol, homework discovery protocol, bulk grading concurrency rules, German/UTF-8 constraints, and reporting examples from `repograde` and `repogradesince` into `grading-shared/SKILL.md`. Grading skills now reference `grading-shared` instead of duplicating ~120 lines each.
- **Reason**: The two grading skills contained near-identical blocks for homework discovery (~120 lines), repository analysis (~40 lines), email/database rules (~10 lines), second-person examples (~20 lines), and German/UTF-8 constraints. Changes to shared logic had to be applied in two places.
- **Considered**: Creating a separate `skills/homework-shared/` skill, or keeping duplication with clearer comments
- **Tradeoff**: `grading-shared` becomes larger, but maintenance is single-source and inconsistencies are prevented
- **Also fixed**: concurrency default standardized to 5 (was 4 vs 5), `repogradesince` duplicate Source 2 header renamed to Source 3, `knowledge-exam` command missing `exam-date` parameter, `/knowledge` usage examples corrected to `/knowledge-exam`

## 2026-04-10: Merge repograde and repogradesince into unified repograde skill
- **Choice**: Remove `/repograde` and `/repogradesince` commands and the `repogradesince` skill entirely. Merge all logic into a single `repograde` skill that handles both full-history and date-filtered grading. The skill parses the user's request to determine mode (single-repo/bulk, filtered/unfiltered) instead of relying on separate command wrappers.
- **Reason**: Two commands with similar but divergent logic, plus a separate skill duplicating ~80% of repograde, created maintenance burden. A single skill with clear mode dispatch is simpler and less error-prone.
- **Considered**: Keeping two skills with shared base; keeping commands as thin wrappers with unified skill
- **Tradeoff**: The `repograde` skill is now larger and handles more modes, but there is a single source of truth for repository grading
- **Removed**: `commands/repograde.md`, `commands/repogradesince.md`, `skills/repogradesince/SKILL.md`
- **Also added**: Plan presentation before grading starts (homework discovered, repos to grade, output files)
- **Also added**: Email body format rules in `grading-shared` — plain ASCII text with code blocks as only allowed Markdown; praise guidelines (subtle, understated); structured email templates for homework and knowledge-check emails

## 2026-04-12: Overhaul projectgrade with holistic grading, PR analysis, and deleted-branch recovery
- **Choice**: Remove `/projectgrade` command and absorb its content into the `projectgrade` skill. Replace rigid numeric weight tables with a holistic descriptive assessment. Add Pull Request analysis, deleted-branch recovery, and further-contributions detection (wiki, CI/CD, tests, docs, project management).
- **Reason**: The command was a thin wrapper delegating entirely to the skill (same pattern as repograde unification). Numeric weights were too rigid for collaborative projects where students contribute in different ways (code, issues, reviews, documentation). Deleted branches were being missed in branch analysis.
- **Considered**: Adding PR scoring as a separate numeric weight category; keeping rigid weights alongside new contributions; creating a separate PR-analysis skill
- **Tradeoff**: The holistic approach is more subjective but fairer and more transparent — the grading report lists all contributions factually to support individual student conversations
- **Removed**: `commands/projectgrade.md`
- **Added sections**: "Differences from repograde", "Deleted Branch Recovery", "Pull Request Analysis", "Further Contributions", "Holistic Grading Philosophy"
- **Replaced**: Numeric weight tables → qualitative descriptive assessment with diligence rating (high/medium/low)
- **Acknowledged limitations**: Pair programming, offline coordination are invisible to Git

## 2026-04-13: Secure configuration via variable substitution and internal store
- **Choice**: Remove API keys from `opencode.json` in the repository. Use internal provider store (`opencode providers add`) for provider keys and `{file:...}` substitution for custom tokens (like SearXNG).
- **Reason**: Prevents accidental leakage of secrets in the public repository while maintaining a shared configuration structure.
- **Considered**: Environment variables (vulnerable to process inspection), cleartext JSON (unsafe).
- **Tradeoff**: Requires one-time local setup of the internal store and a local secret file, but achieves a "secret-free" repository.

## 2026-04-13: Translate internal logic and documentation to English
- **Choice**: Translate all `docs/ai/`, `agents/`, `commands/`, and `skills/` files to English, while strictly preserving German for student-facing output.
- **Reason**: English reasoning improves LLM instruction following for complex logic. Preserving German for students ensures the localized educational experience remains unchanged.
- **Considered**: Remaining in German, full English (including students).
- **Tradeoff**: Requires explicit language safety anchors (`MANDATORY GERMAN`) in skills to prevent accidental English output to students.

## 2026-04-13: Enhance SearXNG with time filtering and explicit search conventions
- **Choice**: Add `time_range` parameter to `searxng_search` tool and update its MCP schema and description.
- **Reason**: Without time filtering, high-authority legacy documentation (like Firefox 4 or MDN articles) can drown out brand-new technology releases (like Gemma 4) in search results.
- **Considered**: Heuristic-based auto-filtering in the tool-wrapper.
- **Tradeoff**: Agent must now explicitly decide when to use a time filter, but the behavior is more predictable and less "magical" than a heuristic approach.
- **Also added**: Explicit "Search Strategy" section to `CONVENTIONS.md` to guide agents.

## 2026-04-16: Standardize repograde output structure
- **Choice**: Add a mandatory `repograde` grading-report template with fixed top-level sections, fixed section responsibilities, and tighter email structure guidance for homework grading outputs.
- **Reason**: Repograde subagents were producing noticeably inconsistent grading bodies, especially in assessment size and emphasis, which made outputs harder to compare across students.
- **Considered**: Keeping the current flexible reporting guidance, or moving the full template entirely into `grading-shared`.
- **Tradeoff**: The skill instructions are more prescriptive and longer, but bulk and single-repo grading outputs are now more consistent and auditable.

## 2026-04-24: Add fork-policy skill for clean-main enforcement on forks
- **Choice**: Create a standalone `skills/fork-policy/SKILL.md` that forbids commits to `main`/`master` on forked repositories, requiring feature branches with naming pattern `feat/issue-N-short-description`.
- **Reason**: Forked repositories need a clean main branch for upstream syncing and to support multiple concurrent feature branches. The policy is loaded on demand rather than enforced by default — projects opt in via AGENTS.md reference or skill invocation.
- **Considered**: Adding the rule to AGENTS.md (always enforced), extending the issue-workflow skill, creating a policy directory
- **Tradeoff**: The policy only applies when explicitly loaded, but this avoids imposing restrictions on non-fork projects
- **Fork detection**: A repository is treated as a fork if it has more than one remote (simple heuristic)

## 2026-05-21: Add automatic assessment disclaimer to all grading emails
- **Choice**: Insert an automatic assessment disclaimer paragraph directly below the email greeting in all grading workflows.
- **Reason**: Transparency for students that the assessment is generated automatically and may contain errors.
- **Wording**: Tailored to address style (Du vs Sie) and type of assessment (Leistungsfeststellung vs Knowledge-Check).
- **Tradeoff**: Adds minor boilerplate, but establishes proper expectations and handles potential auto-assessment mistakes gracefully.

## 2026-05-22: Replace issue slash commands with natural language triggers
- **Choice**: Remove `commands/issue-start.md`, `issue-commit.md`, `issue-finish.md` and trigger `issue-workflow` skill via natural language phrases ("issue start", "issue commit", "issue commit and push")
- **Reason**: The user prefers saying phrases like "issue commit and push" rather than remembering slash commands; NLW is more intuitive and the agent can parse intent reliably
- **Considered**: Keeping slash commands alongside NLW, training on slash commands only
- **Tradeoff**: No tab-completable commands, but the workflow is more accessible and matches user's natural communication style

## 2026-05-22: Create AGENTS.template.md for project onboarding
- **Choice**: Add `AGENTS.template.md` as a generic onboarding template with placeholders, Knowledge Bootstrap, and Skill Triggers blocks
- **Reason**: New projects need a ready-to-copy AGENTS.md that references knowledge-persistence and issue-workflow skills; the template reduces setup friction
- **Considered**: Documenting setup only in README, keeping AGENTS.md as the single source
- **Tradeoff**: Two AGENTS files to maintain (project-specific + template), but onboarding is self-service

## 2026-05-22: Bilingual README with DE priority
- **Choice**: Rewrite README.md with German section first, English section second; add SearXNG server documentation, symlink instructions, and NLW descriptions
- **Reason**: Primary audience is German-speaking teachers and students at HTL Spengergasse; English section serves international opencode community
- **Considered**: German-only README, English-only README, side-by-side translation
- **Tradeoff**: Longer README, but both audiences are served appropriately

## 2026-05-22: Adopt Trunk-Based Development on main
- **Choice**: Always commit and push directly to the `main` branch. Never create feature branches or Pull Requests for development in this repository.
- **Reason**: Simplifies development, reduces process overhead, and aligns with the repository's direct development style.
- **Tradeoff**: Bypasses PR code review, but ensures faster integration for this utility template repository.

## 2026-05-22: Orchestrate README improvements via sub-agents across 12 repos
- **Choice**: Used the `orchestration` skill pattern (epic + sub-issues + Task agents) to improve READMEs across 12 independent repos: zazentimer, opencode-helpers, aitranscribe, aitranscribe-android, GRG-SWP, GRG-WMC, GRG-CS, GRG-POSTHEORIE, GRG-INFI, GRG-JAVA, GRG-NVS, htl
- **Reason**: Each repo had an outdated or missing README; parallel Task agents improved efficiency while each agent independently analysed the source code for accurate, project-specific documentation
- **Considered**: Manual per-repo edits, a single scripted approach
- **Tradeoff**: 12 parallel agents consumed significant context, but all completed successfully with project-specific, non-template READMEs
- **Languages**: English for zazentimer, aitranscribe, aitranscribe-android; bilingual for opencode-helpers; German for all teaching repos

## 2026-09-12: Remove the `telegram-send` skill
- **Choice**: Deleted the `telegram-send` skill; file delivery now goes through the bot's built-in UI.
- **Reason**: The current bot version can attach more files directly through its interface, so the raw-Bot-API skill is redundant.
- **Considered**: Keeping the skill as a fallback; installing the `opencode-telegram-send-file` plugin.
- **Tradeoff**: Loses scripted/agent-initiated sending, acceptable because the bot UI covers the use case.

## 2026-09-12: Slim `orchestration` to a scope-gated coordination policy
- **Choice**: Reduced `skills/orchestration/SKILL.md` from 367 lines of generic decomposition/delegation guidance to a short, scope-gated policy (coordinate only for multi-session/multi-sub-issue work; hard test gate), with pointers to `issue-workflow`, `knowledge-persistence`, and `code-review`.
- **Reason**: Current models already decompose and delegate to sub-agents natively; the generic bulk was no-op, and the skill duplicated the bootstrap protocol (with a phantom `docs/ai/ONBOARDING.md` reference and a numbering bug).
- **Considered**: Retiring the skill outright; keeping and refactoring it in place.
- **Tradeoff**: The "pure orchestrator, never writes code" mode now applies only to large work instead of being an unconditional default.

## 2026-09-12: Consolidate shared grading/search facts into single sources (P2)
- **Choice**: Three identical German-language blocks (`knowledge-assessment`, `projectgrade`, `repograde`) now reference `grading-shared`; the address-style table was removed from `projectgrade` and the class list from `knowledge-exam`; per-question point totals now live only in `knowledge-exam`; `searxng`'s duplicate API-parameter table was removed. A "Single Source of Truth" rule was added to `docs/ai/CONVENTIONS.md`.
- **Reason**: The same facts were maintained in up to four places, so a change in one could silently diverge from the others (the P1 email conflict was one such instance).
- **Considered**: A neutral shared language-rule document; keeping tailored copies in `homework`/`knowledge-exam`.
- **Tradeoff**: `homework` and `knowledge-exam` keep their tailored German statements (they name their own artifact and are loaded standalone); only the verbatim duplicates were collapsed.

## 2026-09-12: Progressive disclosure for long reference material (P3a)
- **Choice**: Moved illustrative and format reference out of six skills into sibling files loaded on demand: `grading-shared/EMAIL-EXAMPLES.md`, `knowledge-persistence/FILE-TEMPLATES.md`, `lehrplan/{KLASSEN-ZUORDNUNG,SPENGERGASSE-KLASSEN,RIS-PRAXIS,ERLAEUTERUNGS-QUALITAET}.md`, `repograde/REPORT-FORMAT.md`, `projectgrade/REPORT-FORMAT.md`. Normative rules stayed inline. Added `tests/test_skill_links.py` as a link guard.
- **Reason**: Six SKILL.md files were 460-1026 lines; examples, templates and branch-specific domain detail are not needed on every run, and burying them dilutes attention (per the `writing-for-agents` information hierarchy).
- **Considered**: Extracting normative protocols too (P3b); a neutral shared doc.
- **Tradeoff**: Normative content (missing-email, methodology, scoring, output language, Repo-Konventionen, Ausbildungszweig-Konzept) stays inline to avoid a pointer behind a pointer, so files shrink less than possible. `KLASSEN-ZUORDNUNG.md` is now the user-editable table.

## 2026-05-22: Restructure GitHub profile README with current projects
- **Choice**: Rewrote `georgernstgraf/georgernstgraf/README.md` to show current projects (zazentimer, opencode-helpers, aitranscribe) prominently, teaching repos in a table, and past projects condensed
- **Reason**: The profile was outdated and didn't reflect the three actively developed projects
- **Considered**: Keeping the old flat list, creating a personal website
- **Tradeoff**: Profile is now longer but gives a complete picture of active work

## 2026-05-21: Enforce pure AI evaluation, prohibit grading scripts
- **Choice**: Mandate pure AI reasoning for all student grading. Explicitly forbid agents from writing or invoking scripts, programs, test runners, linters, or automated checkers to assess student work.
- **Reason**: Agents were writing evaluation scripts that produced machine-like, impersonal grades that failed to account for the unique individuality of each student's submission. Direct AI reasoning produces higher-quality, more nuanced assessments.
- **Considered**: Allowing scripts for partial automation, or relying on agent judgment alone.
- **Tradeoff**: Pure AI evaluation is slower per-student but produces more thoughtful, individualized results. Sub-agents are used for parallelism instead of scripts.

## 2026-09-10: Repo-managed global agents via `agents/` directory
- **Choice**: Add a top-level `agents/` directory as the single global agent source, linked via `~/.config/opencode/agents` (mirror of the skills symlink pattern). Agent definitions are flat `agents/<name>.md` files; the filename becomes the agent name. First agent: `lehrplan-annotator` (ported from WI-Fachgruppe-Informatik's `.opencode/agent/`, where the repo-local copy was removed afterwards).
- **Reason**: Keep `~/.config/opencode` portable — agents are versioned in this repo exactly like skills, available on all hosts, and trunk-based. Explanation authoring (Erläuterungs-Ebene) deliberately uses the non-flash model `opencode-go/glm-5.3`.
- **Considered**: Global agents directly in `~/.config/opencode/agent/` (not portable), per-agent subdirectories like `skills/<name>/SKILL.md` (unnecessary — loader scans `**/*.md`)
- **Tradeoff**: Every `.md` in the `agents/` tree becomes an agent (loader glob `{agent,agents}/**/*.md`, `symlink: true`), so no auxiliary Markdown files are allowed inside `agents/`.

## 2026-09-06: Single-source SearXNG stack with public service URL
- **Choice**: The stdlib-only MCP server in `skills/searxng/scripts/opencode-searxng` is the single search implementation; the legacy requests-based server moved to `scripts/archive/`. The primary search instance is `https://searxng.claw.graf.priv.at` (no localhost entry in the fallback chain).
- **Reason**: The skill runs on multiple hosts — a localhost endpoint only resolves on the SearXNG host itself; the public URL works everywhere (on the SearXNG host it goes through the local nginx). One skill owning its MCP server also guarantees exactly one search skill.
- **Considered**: Keeping the requests-based server in `scripts/`, keeping `localhost:8888` first with public fallback
- **Tradeoff**: Requests from the SearXNG host take the nginx/TLS hop; the archived legacy copy remains in the repo (inert, unregistered).
- **Also added**: Richer tool schema (`category`, `engines`, `time_range`, `safesearch`) ported into the stdlib server; empty result sets are valid answers instead of triggering instance fallbacks.

## 2026-09-12: Route SearXNG egress via the school network (tinyproxy on gregor)
- **Choice**: Send all outgoing SearXNG engine traffic through a tinyproxy on host gregor (`10.8.0.16:1080`, over VPN `tun0`), so requests leave via the HTL Spengergasse school IP (`192.189.51.211`) instead of claw's datacenter IP. Configured globally in the instance's `settings.yml` (`outgoing.proxies`).
- **Reason**: claw's datacenter IP (`85.215.162.182`) is bot-blocked or served random/spam results by most engines; the school IP is treated like normal user traffic. `google` — now the primary general engine — only works via the school IP.
- **Considered**: Staying on the datacenter IP with the reduced engine set (no google; only mwmbl/searchmysite/brave), using a commercial proxy/VPN egress.
- **Tradeoff**: Search quality now depends on gregor + the VPN being up; if the proxy is down, all engines return 0 results (recovery is automatic via systemd restart). tinyproxy is restricted to the VPN interface (`Listen 10.8.0.16`, `Allow 10.8.0.0/24`).
- **Kept out of the skill**: These host/IP/proxy specifics are deployment operations, not portable usage knowledge. They live in `ARCHITECTURE.md`/`PITFALLS.md`; `skills/searxng/SKILL.md` only notes the 0-results failure mode and points to the docs.

## 2026-09-12: Keep Brave Search API as the non-scraper fallback; consolidate the account to prepaid
- **Choice**: Keep the `braveapi` engine in SearXNG as a dormant fallback, and use a single prepaid Brave "Search" plan (`$5`/1,000 requests, `$5` free credit per month) with a `$0` prepay balance so the service simply pauses when the free credit is used up. Retire the postpaid plan.
- **Reason**: `google` is now primary, but every other general engine is an HTML scraper exposed to the same bot-blocking arms race that forced the school-IP egress. `braveapi` is the only API-based engine (independent index, immune to scraping blocks) and costs nothing while suspended, so it is valuable insurance.
- **Considered**: Removing `braveapi` entirely to simplify the engine set; keeping both the postpaid and prepaid plans (rejected — the `$5` free credit is per plan, not per billing model, so a second plan adds no free credit while postpaid can incur pay-as-you-go charges).
- **Tradeoff**: The engine is unavailable whenever the monthly credit is exhausted or the key/auth is wrong, and a plan change requires generating a new API key and updating `settings.yml`. Prepaid caps spend but gives no overage.
- **Verified 2026-09-12**: After topping up, a direct Brave call returned HTTP 200 and the instance `engines=braveapi` query returned results with an empty `unresponsive_engines` list — no restart required.

## 2026-09-12: Quality-gated Brave fallback in the wrapper (credit conservation)
- **Choice**: Keep `braveapi` `disabled: true` on the instance and implement a two-phase search in `skills/searxng/searxng-search.sh`: phase 1 queries the normal engines; phase 2 queries `engines=braveapi` only when a general search yields no reasonable result — 0 results, or no Google result and fewer than 3 results. Results are merged and deduplicated (primary first) and the answer carries `fallback_used`/`fallback_reason`. An explicit `engines=` argument bypasses the fallback.
- **Reason**: Brave was in the default engine pool, so every search consumed its small monthly quota. SearXNG has no native conditional fallback (`weight` only re-ranks), so the quality gate lives in our canonical search script, where it is portable and versioned.
- **Considered**: Leaving Brave enabled and relying on ranking weight (does not gate usage); a SearXNG plugin (heavier and instance-specific); agent-only manual escalation (no enforcement).
- **Tradeoff**: Brave fires only when results are weak — real failures still get a good answer while quota lasts far longer. The thresholds (0 / no-Google & <3, general only) are a heuristic, hardcoded in the script for portability.
- **Also fixed**: SearXNG ignores `engines=` whenever `categories=` is present (the MCP always sends `category=general`), so explicit engine selection had silently never worked — the wrapper now omits the category when engines are given.

## 2026-09-12: Repo-root tests/ with a hermetic stdlib unittest suite
- **Choice**: Add a root `tests/` directory covering the repo's executable code (currently the `searxng` skill). Tests use Python 3 `unittest` plus an in-process `http.server` mock and run with `python3 -m unittest discover -s tests -v`; no network and no external dependencies.
- **Reason**: Tests are development tooling for the repo, not part of the globally symlinked skills. A hermetic mock makes the fallback logic (triggers, merge/dedupe, explicit-engine bypass, instance chain) verifiable without spending Brave quota or depending on the live instance.
- **Considered**: Putting tests inside the skill (`skills/searxng/tests/` — pollutes the global symlink); pytest (extra dependency vs. the stdlib-only MCP); a CI workflow (repo has no CI and is trunk/SVN-oriented — deferred).
- **Tradeoff**: The suite patches a temp copy of the `INSTANCES=(...)` array in `searxng-search.sh` rather than adding a production seam, keeping the shipped script free of test-only environment variables or arguments — at the cost of coupling the tests to that literal.

## 2026-09-13: Prioritized engine chain with a token gate (supersedes the quality-gated fallback)
- **Choice**: Replace the two-phase quality gate in `skills/searxng/searxng-search.sh` with a strict prioritized chain for general searches: `brave` → `google` → `mwmbl,searchmysite` → `braveapi`. A tier fails on suspension (`unresponsive_engines`) or 0 results. `braveapi` is queried **only** when `brave` and `google` both failed and the free tier-3 result has fewer than 3 hits (`FALLBACK_MIN_RESULTS`); when it runs, its results are merged ahead of the free results (URL-deduplicated). The envelope now carries `engine_used`/`fallback_used`/`tried`/`unresponsive_engines`; `fallback_reason` is dropped. Explicit `engines=` and non-general categories bypass the chain.
- **Reason**: The user's overriding goal is good results while minimizing Brave-API spend. `brave` and `google` are both HTML scrapers and are frequently blocked *at the same time* on the shared school-IP egress, so a plain `brave → google → braveapi` chain would spend a Brave request on almost every search. Inserting the free `mwmbl,searchmysite` tier as a buffer and gating the paid API behind a `< 3` free-result threshold keeps the token usage low while still escalating to the independent Brave index when the free result is too thin. `brave` first (it is the scraper least blocked in practice) and `google` second keeps the chain free-first.
- **Considered**: The literal user chain `brave → google → braveapi` (rejected — token-heavy); "strict: braveapi only when every free engine returns 0" (rejected — accepts mwmbl noise too often); a parallel `brave,google` tier (rejected in favour of strict sequential so `google` is not queried when `brave` works); a local result cache with TTL (rejected — the SearXNG/Redis cache suffices).
- **Tradeoff**: Quality now depends on the free tier-3 bar (`< 3`): a query that returns exactly 3 mwmbl hits never escalates to Brave. The threshold is a hardcoded heuristic, kept in the script for portability. Worst-case latency is four sequential requests; per-request timeout is 20 s for tier 1 and 12 s thereafter, and the MCP subprocess timeout is raised to 90 s.
- **Also changed**: `run_query` now remembers the **first** responsive instance and reuses it for later tiers (instead of the last, which could be a dead mirror); chain tiers propagate `time_range`/`safesearch`/`language`/`pageno`; the mock and both test modules were rewritten for per-engine resolution and the new chain semantics.

## 2026-09-13: SearXNG access control (shared secret) + local hardening
- **Choice**: Close the public instance. nginx now enforces **HTTP Basic Auth** (shared secret, `/etc/nginx/searxng.htpasswd`) on the whole `searxng.claw.graf.priv.at` vhost for UI and API, plus `limit_req` (60 r/m, burst 20) and `limit_conn`; the SearXNG container port is published as `127.0.0.1:8888` only; `searxng-search.sh` authenticates from `$SEARXNG_AUTH` or `~/.config/opencode/searxng.cred`; intended clients are claw/think/dell. Local hygiene: `/home/georg` → `750`, `opencode.service` gets `UMask=0077`, secret files → `600`, key-bearing `settings.yml.bak*` deleted.
- **Reason**: On 2026-09-13 the instance was found publicly reachable and used by third parties — foreign-language queries in the container logs that never appeared in the nginx access log, i.e. requests hitting `8888` **directly**, bypassing the proxy; plus `TelegramBot`-UA API calls with explicit `engines=`. The leaked Brave key (`settings.yml` plaintext) was indirectly queryable by anyone via `engines=braveapi`, so an open instance risks the paid Brave quota.
- **Considered**: Leaving the instance open with only rate limiting (rejected — the goal is claw/think/dell-only); IP allowlist / Tailscale-only (rejected — 443 stays open and the hosts' addresses are not fixed); disabling the JSON API entirely (rejected — the MCP tool and bots depend on it).
- **Tradeoff**: A single shared credential must be deployed to claw/think/dell and rotated by hand; a credential leak reopens the instance. Public reachability was the real problem; `robots.txt`/noindex did **not** actually limit indexing before 2026-09-13 (`robots.txt` returned `401` and there was no `X-Robots-Tag`) — an explicit indexing policy was added afterwards (see the 2026-09-13 vhost indexing decision below).
- **Open item (not yet done)**: The SVN deployment mirror `svn+ssh://www@murl/home/www/svnrepos/georg` (`EDV/Deployed/`) contains secret material — SearXNG/Brave/GitHub tokens, bot `.env` files, the OpenCode password, and **private key material** (internal CA `ca.key` + host `*.key`/`.pem`, SSH host keys, a user `id_rsa`, OpenVPN keys, `EDV/api-keys.txt`). No rotation was performed (repo is access-protected). History purge (`svnadmin dump`/`svndumpfilter`, ~3.1 GB / 7420 revs) is pending a decision because the scope is far larger than the search secrets.

## 2026-09-13: SearXNG vhost indexing policy (public robots.txt + X-Robots-Tag) and per-vhost logging
- **Choice**: Serve `/robots.txt` on the SearXNG vhost **without** auth (`location = /robots.txt`) as `User-agent: *` / `Disallow: /`; add a server-level `add_header X-Robots-Tag "noindex, nofollow, noarchive" always;`; suppress the backend's own `X-Robots-Tag` with `proxy_hide_header`. Split the vhost logs into `/var/log/nginx/searxng.access.log` (custom `searxng` `log_format` incl. `rt=$request_time`) and `searxng.error.log`.
- **Reason**: With the whole vhost behind Basic Auth, `/robots.txt` returned `401`, so well-behaved crawlers (observed: `OAI-SearchBot/1.4` at 22:30 on 2026-09-13) never learned the site should not be indexed. A public `Disallow: /` plus `X-Robots-Tag` gives an explicit, machine-readable exclusion while access stays gated. Dedicated logs make Basic-Auth `401`s and rate-limit `429`s measurable instead of being buried in the shared `access.log`.
- **Considered**: Proxying the backend's own `robots.txt` (rejected — it is permissive, `Allow: /`); leaving the `401` as the only signal (rejected — invisible to robots parsers); a separate `map`/bot allow-list (deferred).
- **Tradeoff**: `robots.txt` is now reachable without a credential and confirms the host exists; it is a policy signal only (misbehaving bots ignore it) — Basic Auth remains the real gate. The custom `log_format` must live in the `http` context (`conf.d`).
- **Deployment**: mirrored 1:1 into the SVN `EDV/Deployed` snapshot (revision 7424), together with the earlier auth/limit/log backfill; `conf.d/searxng-limits.conf` and `conf.d/searxng-logformat.conf` added there.

## 2026-09-15: Continuous issue awareness + proactive commit/push (replaces wait-for-trigger policy)
- **Choice**: Make issue-linked work a continuous state instead of a user-invoked mode sequence. (1) The agent always knows which GitHub issue it works under; it searches open issues first, creates a new issue without user interaction when the task is clearly new, and asks only when the assignment is ambiguous. (2) After every completed, verified unit of work the agent commits (with `(#N)` issue reference) and pushes to trunk immediately — no waiting for a trigger. (3) Issue closure: normally ask the user; autonomous closing only when the goal is fully covered, verification is green, no open sub-issues, and nothing contradicts completion. (4) Implemented as a repo-root `AGENTS.global.md` linked to `~/.config/opencode/AGENTS.md` (same symlink pattern as skills/agents), plus a rewrite of `skills/issue-workflow/SKILL.md` (modes `start`/`commit`/`finish` are now manual overrides of the continuous behavior).
- **Reason**: Daily observations: completed issues stayed open too often, and uncommitted/unpushed work accumulated, causing unnecessary merge conflicts when resuming on another host. The old skill rule "do not commit in `start` mode unless the user explicitly asks" reinforced both.
- **Considered**: Only changing the skill (insufficient — opencode's built-in "never commit unless asked" default would still win); per-project overrides via `AGENTS.template.md` only (earlier projects would keep the wait-for-trigger behavior); asking before every commit (still too much friction).
- **Tradeoff**: Commits land more frequently on `main` — mitigated by the green-commit gate (tests/lint must pass first). The global override applies to all repos, so read-only/grading skills and student repos are explicitly excluded in `AGENTS.global.md`; those skills' own "never commit" rules always win. Requires an opencode session restart once to load the new global file.

## 2026-09-17: Gregor SearXNG instance is the school's agentic search instance (rollout: think → dell → student agents)
- **Choice**: Position the Gregor SearXNG instance (`http://10.8.0.16` — VPN `tun0`, port 80, no auth) as the search instance that empowers agents: live as MCP primary on think (#74, `SEARXNG_CHAIN=gregor`), dell replication next, then gradual onboarding of student agents (students empower their own agents with it — no browser-UI role for student use).
- **Reason**: One school-wide instance for agentic search keeps chain semantics and egress behavior uniform across agent hosts. Google-CAPTCHA suspensions on the shared school-IP egress are a browser-context phenomenon — agent-side they are absorbed by the engine chain (`google` → `brave` → `braveapi`), so students clicking "Verify I'm Human" on google.com is unrelated to instance health.
- **Considered**: Keeping claw primary everywhere (Gregor would stay an egress-proxy host only); offering the Gregor web UI as a student search portal (rejected — the instance's role is agentic, students search in the browser).
- **Tradeoff**: All agent hosts share Gregor's availability; when it is down, the claw fallback in each host's MCP environment carries the load.
## 2026-09-23: create-lesson output conventions — dark toggle, README housekeeping, Aufgabe framing
- **Choice**: (1) Every lesson HTML carries a shared light/dark toggle asset (`assets/`: CSS variables + toggle JS), OS default via `prefers-color-scheme`, persisted in `localStorage`, print light, no CDN. (2) The three housekeeping infos (Lehrplan · KM-Bezug · Runtime) live in a `## Housekeeping` block at the very bottom of the Tages-README, not in the HTML header. (3) Student-facing wording is always **Aufgabe**, never "Hausübung"; the Aufgabe **is** the Mitarbeit.
- **Reason**: Driver was the GRG-WMC 5akif async-await lesson (dark-only HTML; Tages-README led with KM-Bezug/Lehrplan/Runtime, burying the content). "Aufgabe = Mitarbeit" reframes the take-home task as graded participation so it reads as classwork, not optional homework.
- **Considered**: Inline per-lesson toggle code (rejected — duplicate, shared asset wins); housekeeping in the HTML footer (rejected — the README is the index); keeping "Hausübung" with an "Aufgabe" gloss (rejected — one term).
- **Tradeoff**: On-disk master files may still be named `hausaufgabe.md`/`Hausübung.md` (repo convention) while the student-facing term is Aufgabe; `homework`/grading skills keep their existing artifact names.
- **Issue**: #77 (`3183819`)

## 2026-09-23: Skills-Entkopplung von mattpocock — alles aus opencode-helpers
- **Choice**: Alle Skills werden in `opencode-helpers/skills/` gepflegt;
  OpenCode-Instanzen werden per Symlink (`~/.config/opencode/skills`)
  versorgt. Projekt-Repos führen kein `.opencode/`-Verzeichnis (in GRG-PMM
  entfernt). Übernommen: neuer globaler `create-lesson`-Skill (Bau von
  Klassen-Lektionen aus Semesterplänen, Abgrenzung zu `teach` als Referenz);
  Zweistelligkeits-Regel für Klassen-Lessons im `teach`-Skill (Selbststudium
  vierstellig ausgenommen); vier nur-projektlokale Skills aus dem alten
  Symlink-Bestand (`handoff`, `to-questionnaire`, `wait-what`,
  `writing-for-agents` inkl. SKILL-MECHANICS; Codex-`agents/` weggelassen).
  `grill-me`/`grilling`/`teach`-Deltas waren trivial (Frontmatter) —
  Helpers-Bestand gilt. Falscher lokaler Commit im mattpocock-Klon per Reset
  entfernt (Klon wieder sauber, kein Push ins Upstream).
- **Reason**: Host-Konfigurationsfehler — `GRG-PMM/.opencode/skills/
  productivity/` zeigte in den mattpocock-Klon statt in entkoppelte Skills;
  4 Skills existierten nur dort (nirgends versioniert unter eigener
  Kontrolle). Die Entkopplung war früher entschieden, aber nie vollzogen.
- **Tradeoff**: `sync-upstream-skills` muss die übernommenen Inhalte bei
  Upstream-Syncs erhalten (Prüfpunkt); `create-lesson` ist Eigenentwicklung
  ohne Upstream. Neustart von opencode nötig, damit neue/geänderte Skills
  laden.

## 2026-09-23: create-lesson Quiz 3–5 Fragen (passungsabhängig) mit Rotation
- **Choice**: Statt "genau 1 Frage pro Lesson" erzeugt `create-lesson` **3–5 Fragen** je nach Stoff; die Richtige-Positionen rotieren ausgewogen über die Fragen (A/B/C/D), je Frage genau eine Richtige. Die Lessons-Tabelle führt die Sequenz (z. B. `B·A·C·D·B`).
- **Reason**: Die GRG-WMC-Lektion async/await (siehe #77) brauchte für mehr Stoff mehr Prüf-Oberfläche; eine Frage deckt mehrstufige Konzepte nicht ab.
- **Considered**: Fest bei 5 (verworfen — Stoffmenge schwankt); bei 1 bleiben (verworfen — zu dünn für mehrstufige Lessons).
- **Tradeoff**: Die Rotation wird pro Lesson statt pro Frage dokumentiert (Sequenz in der Tabelle); Präludium/Skill verlangen das Ablesen der Start-Rotation.
- **Issue**: #78 (`6049e7f`)

## 2026-09-24: oc-models-report moves into the repo with a 12h auto-refresh cache (#79)
- **Choice**: `scripts/oc-models-report` (Python 3, stdlib only) replaces the old SVN `~/bin` script. It caches the `opencode models --verbose` dump at `~/.local/share/oc-models-report/models-verbose.txt` (`$XDG_DATA_HOME` respected) and regenerates it silently-but-visibly (prints `collected info of <N> models`) whenever the cache is missing or older than 12 h. CLI: `<substring> …` filters plus `--refresh` (force) and `--file PATH` (parse a given dump, bypass cache); the old `~/f` default and positional path arg are gone. Failed regeneration falls back to the existing (stale) cache with a stderr warning, or exits 2 when no cache exists. `~/bin/oc-models-report` becomes a symlink into the repo (committed in SVN); the script's table output is byte-identical to the old one. Hermetic tests (`tests/test_oc_models_report.py`, fake collect command + temp cache dir) cover generate/skip/stale/force/`--file`/fallback/no-match.
- **Reason**: The old script forced a manual `opencode models --verbose > ~/f` step before every use; the model list changes slowly, so a TTL cache removes the friction while staying fresh enough.
- **Considered**: `~/.cache/` per XDG (rejected — user chose `.local/share`); keeping the script source in SVN (rejected — helper scripts belong in the versioned project); a lock file for concurrent regenerations (deferred — atomic `os.replace` makes races harmless).
- **Tradeoff**: A stale cache is silently used (with warning) when regeneration fails; the 12 h TTL is fixed unless `OC_MODELS_REPORT_MAX_AGE` overrides it.

## 2026-09-24: oc-models-report --provider <ID> (exakt, case-insensitive) (#80)
- **Choice**: `--provider ID` schränkt die Ausgabe auf Modelle eines Providers ein; der Match ist exakte, case-insensitive Gleichheit gegen `providerID` (kein Substring). Unbekannter Provider → `error: unknown provider: <ID>` auf stderr, exit 2. Genau ein Provider pro Aufruf. `filters` ist jetzt `nargs="*"`, aber ohne Filter und ohne `--provider` bricht argparse ab (exit 2). Provider-Selektion und Substring-Filter sind additiv (`--provider openrouter opus`); ohne Filter listet `--provider` alle Modelle des Providers.
- **Reason**: Provider-Scoping war vorher nur über Substrings im gemeinsamen Haystack (provider/id/name/family) möglich, was Treffer anderer Provider nicht ausschließt.
- **Considered**: Substring-Match für Provider (verworfen — Tippfehler sollen auffallen); mehrere/kommagetrennte Provider (verworfen — YAGNI); unbekannter Provider als „no match“ mit exit 1 (verworfen — Nutzungsfehler, kein leeres Ergebnis).
- **Tradeoff**: Provider-Fehler wird erst nach einem evtl. Cache-Refresh geprüft (die „collected info“-Zeile kann davor erscheinen). Tests decken provider-only, provider+Filter, case-insensitive, exakter Match (Teilstring-Fehler), unbekannter Provider, provider+Filter ohne Treffer und „weder noch“ ab.
- **Issue**: #80
