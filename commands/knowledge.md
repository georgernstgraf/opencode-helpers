---
description: Generate a class knowledge exam from recent Git history
---
Create a German mini-exam for class `$1` based on the last `$2` weeks.

Use the `knowledge-exam` skill for the full workflow.

Pass these inputs into the skill:

- `class`: `$1`
- `weeks`: `$2`

Important constraints:

- If folder `$1` does not exist, stop and report the typo.
- Create the student exam and separate teacher solutions inside folder `$1`.
- Do not commit any generated files.
