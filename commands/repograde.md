---
name: repograde
description: Grade student repositories via the repograde skill
---
# Grade Student Repositories

IMPORTANT: This command must be invoked from a local folder, NOT from within
a Git repository. The `Hausübungen.md` file must exist in the current
working directory. Student repositories must already exist locally; this
command will NOT clone them. If any student repository has uncommitted
changes, the command will stop immediately.

Use the `repograde` skill for this.

Pass these inputs into the skill:

- `context`: current user request, current arguments, and the explicit issue #22 constraints
- `grading-shared`: required in both single-repo and bulk mode

Required behavior to preserve:

- If exactly one argument is provided, treat it as an explicit repository path and use it verbatim.
- In single-repo mode, require `Hausübungen.md`, derive the output stem from `basename($1)`, and write only `<basename>_grading.md` plus `<basename>_email.json`.
- In bulk mode, preserve the concurrent multi-repository grading workflow, have each subagent write only basename-derived per-repo artifacts, and generate shared `EMAIL.json` only after all subagents finish.
- Keep detailed grading, repository analysis, database lookup, and email generation rules inside the `repograde` skill.
