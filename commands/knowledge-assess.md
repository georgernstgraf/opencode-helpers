---
description: Assess knowledge-check submissions and prepare reports
---
IMPORTANT: This command must be invoked from a local folder, NOT from within
a Git repository. The `vacuum.db` file must exist in the current working
directory at start; if missing, the command will stop immediately.

Assess the student knowledge-check submissions in the current directory.

Use the `knowledge-assessment` skill for the full workflow.

Required outputs:

- `GRADINGS.md`
- `INDIVIDUAL.md`
- `CLASS.md`
- `EMAIL.json`

Important constraints:

- If multiple submission versions exist, grade the highest version only.
- Use the point-based scoring rules defined in the `knowledge-assessment`
  skill.
- Keep `CLASS.md` anonymous because it may be committed publicly.
- Retrieve recipient email addresses from `vacuum.db`.
- Use class-based email salutations and closings as defined in the
  `knowledge-assessment` skill.
- Keep the individual feedback and email bodies warm, respectful, well
  structured, and detailed as defined in the `knowledge-assessment` skill.
