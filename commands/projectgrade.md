---
name: projectgrade
description: Grade student project repositories via the projectgrade skill
---
# Grade Student Project Repositories

IMPORTANT: This command must be invoked from a local folder, NOT from within
a Git repository. Student repositories must already exist locally; this command
will NOT clone them. If any student repository has uncommitted changes, the
command will stop immediately.

Use the `projectgrade` skill for this.

Pass these inputs into the skill:

- `context`: current user request and current arguments
- `grading-shared`: required in both single-repo and bulk mode

MODE SELECTION:

IF exactly one argument is provided:
  → Use SINGLE-REPO MODE
ELSE:
  → Use BULK MODE (no arguments)

SINGLE-REPO MODE:
- Treat the argument as the explicit repository path and use it verbatim
- Derive output stem from `basename($1)`
- Write only `<basename>_grading.md` plus `<basename>_email.json`
- Do NOT write shared `EMAIL.json`

BULK MODE:
- Treat each directory as a student repository
- Use concurrent multi-repository grading (max 4 concurrent)
- Each subagent writes only basename-derived per-repo artifacts
- Generate shared `EMAIL.json` only after all subagents finish

## Key Differences from repograde

- No `Hausübungen.md` required (project grading, not homework)
- Evaluates GitHub Issues participation
- Student identification from Git commit emails only
- Issue quality and participation factor into grading

All grading rules, repository analysis, database lookup, issue analysis, and
email generation remain inside the `projectgrade` skill.