---
name: repogradesince
description: Grade student repositories filtering commits after a specified date
---
# Grade Student Repositories (Date-Filtered)

IMPORTANT: This command must be invoked from a local folder, NOT from within
a Git repository. Homework assignments are discovered from two sources:
- Legacy: a cumulative `Hausübungen.md` file in the current working directory
  (may be a symbolic link; follow symlinks when reading)
- Per-lesson: individual `Hausübung.md` files inside `<date>_<topic>`
  subdirectories
At least one homework source must exist. Student repositories must already
exist locally; this command will NOT clone them. If any student repository has
uncommitted changes, the command will stop immediately.

## Mandatory Date Parameter

The first argument MUST be a valid ISO date in format `YYYY-MM-DD`.

- Valid examples: `2025-03-15`, `2024-12-01`, `2025-01-31`
- Invalid examples: `2025-3-15`, `2025/03/15`, `2025-03`

If the date format is invalid, STOP IMMEDIATELY with an error message.

Use the `repogradesince` skill for this.

Pass these inputs into the skill:

- `context`: current user request and current arguments
- `grading-shared`: required in both single-repo and bulk mode

MODE SELECTION:

IF `$1` is NOT a valid ISO date:
  → STOP IMMEDIATELY with error: "Invalid date format: '[input]'. Expected ISO date format: YYYY-MM-DD (e.g., 2025-03-15)"

IF two arguments are provided (date + repository path):
  → Use SINGLE-REPO MODE

IF one argument is provided (date only):
  → Use BULK MODE

DATE HANDLING:
- Parse `$1` as the cutoff date at 0:00 AM
- Only process commits dated at or after this date
- Use `git log --after="YYYY-MM-DD"` to filter commits

SUBMISSION DEADLINE POLICY:
- Students have one week to complete homework from the assignment date
- Example: Assignment dated March 11th → due March 18th
- Submissions are only considered late after the one-week deadline
- When grading, factor this deadline into the evaluation

SINGLE-REPO MODE (two arguments):
- `$1` = ISO date (cutoff)
- `$2` = repository path
- Derive output stem from `basename($2)`
- Write only `<basename>_grading.md` plus `<basename>_email.json`
- Do NOT write `INDIVIDUAL.md`, `CLASS.md`, or shared `EMAIL.json`

BULK MODE (one argument):
- `$1` = ISO date (cutoff)
- Treat each directory as a student repository
- Use concurrent multi-repository grading (max 4 concurrent)
- Each subagent writes only basename-derived per-repo artifacts
- After all subagents finish, generate:
  - `GRADINGS.md` with class-wide overview table (alphabetically ordered)
  - `CLASS.md` with anonymized class-wide patterns and teacher recommendations
  - Shared `EMAIL.json` aggregating all per-repo email payloads

All grading rules, repository analysis, database lookup, and email generation
remain inside the `repogradesince` skill.