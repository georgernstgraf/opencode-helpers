---
description: Save current progress to an issue (creates one if missing)
---
We've made progress and want to save it, but we aren't finished yet.

Use the `issue-workflow` skill for this.

Pass these inputs into the skill:

- `mode`: `commit`
- `issue`: current issue if known, otherwise infer or create one
- `context`: recent implementation progress, plans, and todos

Important constraints:

- No commit is allowed without an associated GitHub issue number.
- If no issue exists yet, create one before committing.
- Keep the issue open after commenting, committing, and pushing.
