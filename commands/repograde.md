---
name: repograde
description: Grade student repositories via the repograde skill
---
# Grade Student Repositories

Use the `repograde` skill for this.

Pass these inputs into the skill:

- `context`: current user request, current arguments, and the explicit issue #22 constraints
- `grading-shared`: required in both single-repo and bulk mode

Required behavior to preserve:

- If exactly one argument is provided, treat it as an explicit repository path and use it verbatim.
- In single-repo mode, require `Hausübungen.md`, update `INDIVIDUAL.md`, optionally nudge `CLASS.md`, and write `$1_email.json` instead of shared `EMAIL.json`.
- In bulk mode, preserve the concurrent multi-repository grading workflow.
- Keep detailed grading, repository analysis, database lookup, and email generation rules inside the `repograde` skill.
