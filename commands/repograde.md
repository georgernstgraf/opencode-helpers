---
name: repograde
description: Grade Student Repositories with configurable batch size (default: 7 concurrent)
---
# Grade Student Repositories

Every directory within this folder is named after a student. Invoke the `@repograder` agent for each individual directory.

## Dependencies

This command uses the `grading-shared` skill for:
- Class-to-address-style mapping
- Email generation protocol (greetings, closings, gender determination)
- Database lookup patterns
- Email JSON structure

Reference `skills/grading-shared/SKILL.md` for centralized configuration.

## Parameters

- `$1` (optional): Maximum concurrent sub-agents. Default: `7`

## Execution

### Phase 1: Run RepoGrader Agents

- Run one `@repograder` agent instance per student directory
- Execute in batches of **$1 concurrent instances maximum** (default: 7)
- As each sub-agent completes, start the next one to maintain maximum throughput
- Continue until all student directories are processed

### Phase 2: Generate Bulk Email JSON

After all agents complete, generate a single `EMAIL.json` file:

1. **Collect Results**: Read all `*_grading.md` files from the repo root
2. **Database Lookup**: Query `/home/georg/OneDrive/uploadthing.db` SQLite database
   - Table: `users`
   - Match students by name to retrieve email addresses and class
3. **Determine Address Style**: Use `grading-shared` skill configuration
   - Reference class-to-address-style mapping from shared skill
4. **Generate EMAIL.json**: Create a JSON array following `grading-shared` structure

**Email JSON Structure (see `grading-shared` for full details):**
```json
[
  {
    "mailto": "student@example.com",
    "subject": "Repository-Bewertung - Max Mustermann",
    "body": "<personalized German assessment>"
  },
  ...
]
```

**Email Body Requirements:**
- Language: German
- Greeting: Use formulas from `grading-shared` based on class address style
- **Content: The ENTIRE grading report from `<basename>_grading.md`** - the email body should be the full, detailed report
- Closing: Use formulas from `grading-shared` based on class address style

**If student not found in database:**
- Set `mailto: null`
- Add `note` field with explanation
- Flag for manual review

## Progress Reporting

After each batch completes, report:
- Completed batch number and total batches (e.g., "Batch 2/6 complete")
- Number of students processed so far
- After all batches: "All grading complete. Generating EMAIL.json..."

## Input

Pass each student's directory path to the sub-agent. Handle paths with spaces correctly:

- Use proper quoting when passing paths (e.g., `"./John Doe"` or `'./John Doe'`)
- Each directory corresponds to one student's repository

## Constraints

- Do not commit anything (this folder is not a git repo)
- Output files (`*_grading.md`) will be placed in the repo root
- `EMAIL.json` will be placed in the repo root
- **All grading reports must be written in German**
- All email bodies in German with UTF-8 encoding
- Email body contains the FULL grading report (long emails are expected)
- Preserve German umlauts in natural form (ä, ö, ü, ß)
