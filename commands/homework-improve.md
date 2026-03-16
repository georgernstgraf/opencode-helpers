---
description: Enrich a class homework file from recent Git history
---
Improve the homework writeup for class `$1`.

Use the `homework-improve` skill for the full workflow.

Pass these inputs into the skill:

- `class`: `$1`

Important constraints:

- If folder `$1` does not exist, stop and report the typo.
- Update or create `Hausübungen.md` inside folder `$1`.
- Keep the file in German.
- Keep newest homework entries at the top.
- Make the workflow re-entrant so existing covered dates are not recreated.
- Do not commit any generated changes.
