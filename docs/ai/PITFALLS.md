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
- `~/.opencode/skills` is a symlink to the repo's `skills/` directory; editing one location updates both automatically

## Database

- Class lookup in `uploadthing.db` is case-sensitive; `klasse` column stores uppercase (e.g., "2AHWII") but `grading-shared` config uses lowercase ("2ahwii"); always use `UPPER(klasse)` comparison

## Grading Workflow

- Never assume grading commands run from within a Git repository - they operate from a local folder (CWD)
- `projectgrade` is the exception: it MUST run from within a Git repository (the project being evaluated)
- `Hausübungen.md` is always in the CWD, never inside a student repository
- `Hausübungen.md` may be a symbolic link; follow symlinks when reading
- Student repositories must already exist locally; never attempt to clone them
- If any student repository has uncommitted changes, grading must stop immediately
- All grading skills use `<name>_grading.md` pattern; `INDIVIDUAL.md` is deprecated
- `knowledge-assessment` outputs `GRADINGS.md` and `CLASS.md` (both mandatory) plus per-student `<name>_grading.md` files

## Project Configuration

- OpenClaw-specific configuration (agent binding, Telegram groups, memory settings) belongs in OpenClaw's channel config, not in `AGENTS.md` or other project files
- Project `AGENTS.md` should contain only project-relevant instructions and conventions
