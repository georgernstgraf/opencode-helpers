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
- `~/.opencode/skills` is a symlink to the repo's `skills/` directory; editing one location updates both automatically.
- When refactoring shared content into `grading-shared`, keep grading-specific logic (date filtering, homework weighting) in the consuming skill — only truly shared protocols belong in `grading-shared`.
- The `repograde` skill now handles both full-history and date-filtered grading; there is no separate `repogradesince` skill or command.

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

## Project Configuration

- OpenClaw-specific configuration (agent binding, Telegram groups, memory settings) belongs in OpenClaw's channel config, not in `AGENTS.md` or other project files.
- Project `AGENTS.md` should contain only project-relevant instructions and conventions.
- Searching for "latest" technologies or software versions (e.g., "Gemma 4") without a `time_range` or exact quoting (`"Gemma 4"`) often returns irrelevant legacy documentation due to higher domain authority of old sites (e.g., Firefox 4, MDN). Always check if a time filter is needed for brand-new topics.
