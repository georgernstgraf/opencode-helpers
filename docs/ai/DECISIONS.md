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
