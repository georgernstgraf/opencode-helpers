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

## Constraints

- All exam and assessment content must be written in German
- `CLASS.md` must remain anonymous for public repository use
- `*_solutions.md` files are git-ignored to avoid exposing answers
- Individual assessments must preserve paragraph spacing when copied to email bodies
