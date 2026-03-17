# Domain Knowledge

Business rules and domain relationships not obvious from code.
Only populate this file when the project has meaningful domain logic.

## Entities

- **Student**: Submits knowledge-check answers, receives personalized feedback via email
- **Teacher**: Generates exams from Git history, assesses submissions, sends bulk emails
- **Class**: Group of students with shared communication preferences (formal/informal address)

## Rules

- Knowledge exams contain exactly 10 multiple-choice questions and 3 free-text questions
- Multiple-choice questions have exactly 4 answer options, worth 4 points total (1 point per correctly handled option)
- Free-text questions are worth 15 points each
- Formal address classes use `Liebe Frau [Last Name]` or `Lieber Herr [Last Name]`
- Informal address classes (`2ahwii`, `3ahwii`, `5ahwii`, `4aaif`) use `Liebe [First Name]` or `Lieber [First Name]`
- Email sign-offs differ by class: formal uses `Mit freundlichen Grüßen,`, informal uses `Lieben Gruß,`

## Workflows

- **Exam generation**: Git history analysis → German exam file → separate solutions file
- **Assessment**: Student submissions → point-based grading → individual feedback → class patterns → bulk email JSON
- **Email composition**: Individual assessment → structured paragraphs → solutions note → sign-off → EMAIL.json
- **Repository grading**: Student repos → batched RepoGrader agents → German grading reports → EMAIL.json with full reports

## Constraints

- All exam and assessment content must be written in German
- All repository grading reports must be written in German
- `CLASS.md` must remain anonymous for public repository use
- `*_solutions.md` files are git-ignored to avoid exposing answers
- Individual assessments must preserve paragraph spacing when copied to email bodies
- Email body contains the ENTIRE grading report (long emails expected)

## Database

- **Location**: `/home/georg/OneDrive/uploadthing.db`
- **Table**: `users` with columns `email`, `name`, `klasse`
- **Purpose**: Email address lookup and class-based address style determination
- **Address style by class**:
  - Informal (`Liebe [First Name]`): `2ahwii`, `3ahwii`, `5ahwii`, `4aaif`
  - Formal (`Sehr geehrte Frau [Last Name]`): all other classes
