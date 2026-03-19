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
- Do not move runtime-critical skill instructions into adjacent helper Markdown files unless skill loading is known to include them
- Do not allow issue workflow commits without a GitHub issue number in the commit message
- When passing Markdown with backticks to `gh issue comment` through the shell, quote it safely or the shell may try to execute the backticked fragments before posting the comment
- OpenCode has no built-in throttling for parallel sub-agent execution - use dynamic concurrency with a maximum limit and ~3 second delays between agent starts to avoid overwhelming API rate limits
- When removing or renaming a skill, update every dependent command, agent, README entry, and knowledge file in the same change or stale workflow references remain behind
