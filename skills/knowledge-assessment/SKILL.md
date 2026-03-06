# Knowledge Assessment Skill

## Purpose

This skill assesses student submissions for a knowledge-check exam, produces
teacher-facing reports in German, and prepares structured email payloads for
communicating individual results.

## Inputs

- Student submission files in the current directory
- Matching knowledge-check files with questions and solutions
- `vacuum.db` for student email address lookup
- Class membership to decide whether the email should use formal or informal
  address

## Protocol

### 1. Discover Assessment Inputs

- Inspect the current directory for student submission files and the matching
  knowledge-check files containing the questions and solutions.
- If a student submitted multiple versions, grade only the highest version.
- Read any student comments where they used `-` to mark an answer as ambiguous
  or context-dependent, and consider that explanation during assessment.

### 2. Grade Submissions

- Evaluate each submission against the available solutions.
- Use the Austrian grading system for the overall result.
- Keep grading consistent across all students.

### 3. Create Report Files

- Create `GRADINGS.md` in German.
- Include a comprehensive table ordered alphabetically by student name, not by
  grade.
- Create `INDIVIDUAL.md` in German.
- Provide a detailed assessment for each student's submission.
- Create `CLASS.md` in German.
- Summarize the most common mistakes across the class and add recommendations
  for the teacher on how to address them.
- Do not name any students in `CLASS.md` because it is intended for a public
  repository.

### 4. Create Bulk Email JSON

- Query the `vacuum.db` SQLite database to retrieve student email addresses from
  the `users` table.
- Match students carefully so that each result is sent to the correct person.
- Determine the student's gender from the first name so the salutation matches
  the correct German form.
- If the gender is not clear from the first name alone, use additional context
  such as class records, submission wording, or other available student data.
- Determine the addressing style from the class:
  - Informal classes: `2ahwii`, `3ahwii`, `5ahwii`, `4aaif`
  - All other classes use formal address.
- Create `EMAIL.json` as a JSON array.
- Each object must contain exactly these fields:
  - `mailto`: recipient email address
  - `subject`: `Ergebnis der Wissensueberpruefung am <isodate>`
  - `body`: the student's individual assessment text
- Build the email body in German and include the correct greeting:
  - Formal: `Liebe Frau [Last Name]` or `Lieber Herr [Last Name]`
  - Informal: `Liebe [First Name]` or `Lieber [First Name]`
- End each email body with the correct closing formula:
  - Formal: `Mit freundlichen Grüßen,` followed by two new lines and then
    `   Georg Graf.`
  - Informal: `Liebe Grüße` followed by two new lines and then
    `   Georg Graf.`
- If the gender still cannot be determined with high confidence, do not guess.
  Use `Guten Tag [First Name] [Last Name],` as a neutral fallback greeting,
  keep the class-based closing formula, and flag the case in `INDIVIDUAL.md`
  for manual review before the emails are sent.

### 5. Constraints

- Write all report files in German.
- Treat `INDIVIDUAL.md` as the source for the personalized email bodies.
- Keep `CLASS.md` anonymous.
- Prefer deterministic, auditable grading language over vague praise.
- The email greeting and closing in `EMAIL.json` must follow the class-based
  formal or informal rules exactly.

## Output Expectations

- `GRADINGS.md` with class-wide grading overview.
- `INDIVIDUAL.md` with detailed per-student feedback.
- `CLASS.md` with anonymized class patterns and teacher recommendations.
- `EMAIL.json` with one personalized email payload per student.
