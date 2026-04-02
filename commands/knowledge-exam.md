---
description: Generate a class knowledge exam from recent Git history
---
Create a German mini-exam for class `$1` based on the last `$2` weeks.

Use the `knowledge-exam` skill for the full workflow.

Pass these inputs into the skill:

- `class`: `$1`
- `weeks`: `$2`
- `exam-date`: `$3` (mandatory) — must be an ISO date (`YYYY-MM-DD`), or the literal `today` or `tomorrow`
- `mc-count`: `$4` (optional, default 10) — number of multiple-choice questions
- `free-count`: `$5` (optional, default 3) — number of free-text questions

## Usage

```
/knowledge-exam <class> <weeks> <exam-date>                          # Uses defaults, asks for confirmation
/knowledge-exam <class> <weeks> <exam-date> <mc-count>              # Custom MC count, default free-text
/knowledge-exam <class> <weeks> <exam-date> <mc-count> <free-count> # Both counts specified
```

## Behavior

- `exam-date` is mandatory. If not provided, stop with an error.
- If neither question count is provided, ask the user to confirm the defaults
  (10 MC, 3 free-text) before generating.
- If at least one count is explicitly provided, proceed without confirmation.

Important constraints:

- If folder `$1` does not exist, stop and report the typo.
- Create the student exam and separate teacher solutions inside folder `$1`.
- Do not commit any generated files.
