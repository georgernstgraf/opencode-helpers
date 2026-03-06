---
description: Assess knowledge-check submissions and prepare reports
---
Assess the student knowledge-check submissions in the current directory.

Use the `knowledge-assessment` skill for the full workflow.

Required outputs:

- `GRADINGS.md`
- `INDIVIDUAL.md`
- `CLASS.md`
- `EMAIL.json`

Important constraints:

- If multiple submission versions exist, grade the highest version only.
- Use the Austrian grading system.
- Keep `CLASS.md` anonymous because it may be committed publicly.
- Retrieve recipient email addresses from `vacuum.db`.
- Address students using polite German (`Sie`).
