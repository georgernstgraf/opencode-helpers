---
description: Start or continue working on a task (existing or new)
---
Let's work on the task: `$ARGUMENTS`

Use the `issue-workflow` skill for this.

Pass these inputs into the skill:

- `mode`: `start`
- `issue`: `$ARGUMENTS`
- `context`: current user request and any inferred plan

Important constraints:

- If the issue already appears complete in the codebase, comment on it, close it,
  and stop.
- If no issue exists yet, create one before proceeding.
- Do not commit in this mode unless the user explicitly asks for it.
