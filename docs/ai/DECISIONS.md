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

## 2026-03-16: Add homework-improve as a standalone education skill
- **Choice**: Implement `/homework-improve` as a thin command wrapper around a dedicated `homework-improve` skill that writes `Hausübungen.md`
- **Reason**: The workflow needs reusable rules for class-folder history analysis, German homework expansion, newest-first ordering, and re-entrant updates
- **Considered**: Embedding the workflow directly in the command file, or overloading `knowledge-exam` with homework behavior
- **Tradeoff**: One more standalone skill to maintain, but the homework workflow stays explicit and reusable
- **Superseded by**: 2026-04-01 unified homework decision

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

## 2026-03-18: Add /homework command as read-only homework suggestion generator
- **Choice**: Implement `/homework` as a thin command wrapper around a dedicated `homework` skill that outputs suggestions without modifying files
- **Reason**: Teachers need quick homework ideas from recent lesson commits; unlike `/homework-improve`, this should be read-only for easy copy-paste
- **Considered**: Combining with `/homework-improve`, or extending `/knowledge-exam`
- **Tradeoff**: Another standalone skill, but keeps the read-only output pattern explicit and separate from file-modifying workflows
- **Superseded by**: 2026-04-01 unified homework decision

## 2026-03-18: Centralize grading configuration in grading-shared skill
- **Choice**: Create `skills/grading-shared/SKILL.md` as single source of truth for class-to-address-style mapping, email formulas, and database patterns
- **Reason**: Both `knowledge-assessment` and `repograde` were duplicating class lists, email greetings/closings, and database lookup patterns
- **Considered**: Keeping configuration duplicated in each skill, or using a JSON config file
- **Tradeoff**: One more skill file, but eliminates duplication and ensures consistency across grading workflows

## 2026-03-21: Require second-person address (Du/Sie) in all grading content
- **Choice**: All grading content (grading reports, INDIVIDUAL.md, email bodies) must address students directly in second person, matching the class-based email salutation style
- **Reason**: Third-person address ("der Schüler hat...") is inconsistent with email salutations and feels impersonal; students should be addressed directly
- **Considered**: Mixed third-person in reports with second-person in emails, or only second-person in emails
- **Tradeoff**: Requires careful grammar (Sie vs Du conjugation), but creates consistent student experience

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
