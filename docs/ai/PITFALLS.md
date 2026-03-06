# Pitfalls and Gotchas

Things that do not work, subtle bugs, and non-obvious constraints.
Read this file carefully before making changes in affected areas.

<!-- Add pitfalls as bullet points, one per line, actionable:
- When doing X, always Y first or Z will fail
- Library A has a bug with version B, use C as workaround
-->

## General

- Always read existing files before editing - opencode requires this
- Never assume a library is available - check imports/package files first
- OpenCode may show linked skills as `None` when `SKILL.md` files are missing required YAML frontmatter
