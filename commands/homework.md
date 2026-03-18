---
description: Generate a short homework assignment suggestion from recent Git history
---
Generate a short homework assignment suggestion for class `$1` based on the last 24 hours.

Use the `homework` skill for the full workflow.

Pass these inputs into the skill:

- `class`: `$1`

Important constraints:

- If folder `$1` does not exist, stop and report the typo.
- Analyze Git commits from the last 24 hours that changed files inside the class folder.
- **Do NOT modify any files.** Output the homework suggestion directly for the user to copy.
- Keep the suggestion in German.
- Make the assignment short and focused (2-4 exercises).
