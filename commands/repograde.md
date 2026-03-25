---
name: repograde
description: Grade student repositories via the repograde skill
---
# Grade Student Repositories

IMPORTANT: This command must be invoked from a local folder, NOT from within
a Git repository. The `Hausübungen.md` file must exist in the current
working directory (may be a symbolic link; follow symlinks when reading).
Student repositories must already exist locally; this command will NOT clone
them. If any student repository has uncommitted changes, the command will
stop immediately.

Use the `repograde` skill for this.

Pass these inputs into the skill:

- `context`: current user request, current arguments, and the explicit issue #22 constraints
- `grading-shared`: required in both single-repo and bulk mode

MODE SELECTION:

IF exactly one argument is provided:
  → Use SINGLE-REPO MODE
ELSE:
  → Use BULK MODE (no arguments)

SINGLE-REPO MODE:
- Treat the argument as the explicit repository path and use it verbatim
- Require `Hausübungen.md` in the current working directory
- Derive output stem from `basename($1)`
- Write only `<basename>_grading.md` plus `<basename>_email.json`
- Do NOT write `INDIVIDUAL.md`, `CLASS.md`, or shared `EMAIL.json`

BULK MODE:
- Treat each directory as a student repository
- Use concurrent multi-repository grading (max 4 concurrent)
- Each subagent writes only basename-derived per-repo artifacts
- After all subagents finish, generate:
  - `GRADINGS.md` with class-wide overview table (alphabetically ordered)
  - Shared `EMAIL.json` aggregating all per-repo email payloads

All grading rules, repository analysis, database lookup, and email generation
remain inside the `repograde` skill.
