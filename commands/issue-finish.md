---
description: Complete the task, commit, push, and close the issue
---
The work is finished. Let's wrap it up:

Use the `issue-workflow` skill for this.

Pass these inputs into the skill:

- `mode`: `finish`
- `issue`: current issue if known, otherwise infer or create one
- `context`: final implementation summary

Important constraints:

- No commit is allowed without an associated GitHub issue number.
- Persist all newly acquired session knowledge by invoking the
  `knowledge-persistence` skill during the finish workflow.
- Close the issue only after the final report, commit, and push succeed.
