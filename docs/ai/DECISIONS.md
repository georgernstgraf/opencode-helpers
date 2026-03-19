# Architectural Decisions

Records architectural and technical decisions with rationale.
Each entry documents WHAT was decided and WHY.

<!-- Add decisions using this format:
## YYYY-MM-DD: <Short Title>
- **Choice**: What was chosen
- **Reason**: Why this option was selected
- **Considered**: What alternatives were evaluated
- **Tradeoff**: Known downsides accepted
-->

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

## 2026-03-18: Consolidate repo-report into repograde
- **Choice**: Absorb the former `repo-report` analysis workflow into `skills/repograde/SKILL.md`
- **Reason**: Repository grading should have one authoritative skill, while `/repograde` stays a thin command wrapper and both single-repo and bulk mode share the same logic
- **Considered**: Keeping a separate generic analysis skill, or preserving the older agent-plus-skill split
- **Tradeoff**: The repograde skill becomes broader, but the grading workflow is clearer and easier to maintain

## 2026-03-19: Repograde writes basename-derived artifact files only
- **Choice**: In `repograde`, generate only `<basename>_grading.md` and `<basename>_email.json` per repository, and reserve shared `EMAIL.json` for the bulk-mode master aggregation step
- **Reason**: Artifact-based outputs are clearer than mutating `INDIVIDUAL.md` or `CLASS.md`, and they make the subagent/master split explicit in bulk mode
- **Considered**: Continuing to write `INDIVIDUAL.md` and `CLASS.md`, or allowing subagents to append directly to shared `EMAIL.json`
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

## 2026-03-18: Centralize grading configuration in grading-shared skill
- **Choice**: Create `skills/grading-shared/SKILL.md` as single source of truth for class-to-address-style mapping, email formulas, and database patterns
- **Reason**: Both `knowledge-assessment` and `repograde` were duplicating class lists, email greetings/closings, and database lookup patterns
- **Considered**: Keeping configuration duplicated in each skill, or using a JSON config file
- **Tradeoff**: One more skill file, but eliminates duplication and ensures consistency across grading workflows
