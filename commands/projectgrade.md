---
name: projectgrade
description: Grade student project repositories via the projectgrade skill
---
# Grade Student Project Repositories

IMPORTANT: This command must be invoked from WITHIN the Git repository being
evaluated. You must be inside the project repository (the CWD must be a Git
repository). If you are not inside a Git repository, this command will fail
with an error.

Use the `projectgrade` skill for this.

Pass these inputs into the skill:

- `context`: current user request and current arguments
- `grading-shared`: required for grading workflow

## Execution Requirement

- CWD must be a Git repository (the collaborative project being graded)
- The repository must have no uncommitted changes
- Run `git pull` before grading to ensure latest version

## Key Differences from repograde

- Invoked from INSIDE the project Git repository (not from a local folder)
- No `Hausübungen.md` required (project grading, not homework)
- Evaluates GitHub Issues participation
- Student identification from Git commit emails only
- Issue quality and participation factor into grading
- Single project mode (no bulk grading)

All grading rules, repository analysis, database lookup, issue analysis, and
email generation remain inside the `projectgrade` skill.