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

## 2026-03-18: RepoGrader delegates to repo-report skill for commit analysis
- **Choice**: RepoGrader agent invokes `repo-report` skill for homework-agnostic analysis, then post-processes for assignment matching
- **Reason**: Separates concerns - skill handles commit inspection, agent handles homework-specific context
- **Considered**: Embedding all analysis logic in the agent
- **Tradeoff**: Two files to maintain, but skill is reusable for non-grading scenarios

## 2026-03-18: Batched parallel execution for RepoGrader sub-agents
- **Choice**: Execute RepoGrader agents in configurable batches (default 5 concurrent), not all at once
- **Reason**: OpenCode has no built-in throttling; 30 parallel sub-agents could overwhelm machine/API limits
- **Considered**: Fully parallel or fully sequential execution
- **Tradeoff**: Slightly more complex command logic, but safer for rate limits and system resources
