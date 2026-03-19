# Domain Knowledge

Business rules and domain relationships not obvious from code.
Only populate this file when the project has meaningful domain logic.

## Central Configuration

The `grading-shared` skill (`skills/grading-shared/SKILL.md`) provides centralized
configuration for all grading workflows:
- Class-to-address-style mapping
- Email generation protocol (greetings, closings, gender determination)
- Database lookup patterns
- Email JSON structure

All grading-related skills and commands reference this shared configuration.

## Entities

- **Student**: Submits knowledge-check answers, receives personalized feedback via email
- **Teacher**: Generates exams from Git history, assesses submissions, sends bulk emails
- **Class**: Group of students with shared communication preferences (formal/informal address)

## Rules

- Knowledge exams contain exactly 10 multiple-choice questions and 3 free-text questions
- Multiple-choice questions have exactly 4 answer options, worth 4 points total (1 point per correctly handled option)
- Free-text questions are worth 15 points each
- Address style and email formulas: see `grading-shared` skill for centralized configuration

## Workflows

- **Exam generation**: Git history analysis → German exam file → separate solutions file
- **Assessment**: Student submissions → point-based grading → individual feedback → class patterns → bulk email JSON
- **Email composition**: Individual assessment → structured paragraphs → solutions note → sign-off → EMAIL.json
- **Repository grading**: `repograde` skill → explicit single-repo path mode or bulk mode → per-repo `<basename>_grading.md` and `<basename>_email.json` outputs → bulk master aggregation into `EMAIL.json`

## Constraints

- All exam and assessment content must be written in German
- All repository grading reports must be written in German
- `CLASS.md` must remain anonymous for public repository use
- `*_solutions.md` files are git-ignored to avoid exposing answers
- Individual assessments must preserve paragraph spacing when copied to email bodies
- Email body contains the ENTIRE grading report (long emails expected)

## Database

Databases and lookup protocol are defined in `grading-shared` skill.

| Database | Path | Purpose |
|----------|------|---------|
| UploadThing | `/home/georg/OneDrive/uploadthing.db` | Repository grading |
| Vacuum | `vacuum.db` (current directory) | Knowledge-check grading |

Table schema: `users` with columns `email`, `name`, `klasse`
