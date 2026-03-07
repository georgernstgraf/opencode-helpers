---
name: knowledge-assessment
description: Assess German knowledge-check submissions and prepare reports and email payloads
license: MIT
compatibility: opencode
metadata:
  category: education
  output: assessment
---

# Knowledge Assessment Skill

## Purpose

This skill assesses student submissions for a knowledge-check exam, produces
teacher-facing reports in German, and prepares structured email payloads for
communicating individual results.

## Inputs

- Student submission files in the current directory; each submission filename
  contains the class identifier that determines whether formal or informal
  address should be used
- Matching knowledge-check files with questions and solutions, including a
  solutions file in the same directory that can be used as the reference for
  correct answers
- `vacuum.db` for student email address lookup

## Protocol

### 1. Discover Assessment Inputs

- Inspect the current directory for student submission files and the matching
  knowledge-check files containing the questions and solutions.
- Derive the class for each submission from its filename.
- If a student submitted multiple versions, grade only the highest version.
- Read any student comments where they used `-` to mark an answer as ambiguous
  or context-dependent, and consider that explanation during assessment.

### 2. Grade Submissions

- Evaluate each submission against the available solutions.
- Use the defined point totals instead of an Austrian school grading scheme.
- Grade multiple-choice questions per answer option: award 1 point for each
  option that was handled correctly, whether it was correctly checked or
  correctly left blank.
- Do not award partial fractions within an option; each option is worth
  either 1 point or 0 points.
- Treat each multiple-choice question as worth 4 points total because it has
  exactly 4 answer options.
- Treat each free-text question as worth 15 points.
- Keep grading consistent across all students.

### 3. Create Report Files

- Create `GRADINGS.md` in German.
- Include a comprehensive table ordered alphabetically by student name, not by grade.
- Create `INDIVIDUAL.md` in German.
- Provide a relatively detailed assessment for each student's submission.
- Use a respectful teacher-to-student tone that is friendly, warm, and
  encouraging without becoming informal where the class context requires a
  formal address.
- Structure each individual assessment with a fair amount of newlines so it is
  easy to read when copied directly into an email.
- Discuss both strengths and weaknesses in meaningful detail.
- Include an in-depth analysis of specific questions or answer patterns that
  were handled correctly or incorrectly.
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
- Determine the addressing style from the class parsed from the submission
  filename:
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
    `   Georg Graf`
  - Informal: `Lieben Gruß,` followed by two new lines and then
    `   Georg Graf`
- Include a note in every email body stating that a file with the correct
  solutions has been uploaded to the Git repository. Place this note near the
  end of the body, before the closing formula.
- If the gender still cannot be determined with high confidence, do not guess.
  Use `Guten Tag [First Name] [Last Name],` as a neutral fallback greeting,
  keep the class-based closing formula, and flag the case in `INDIVIDUAL.md`
  for manual review before the emails are sent.

### 5. Constraints

- Write all report files in German.
- Treat `INDIVIDUAL.md` as the source for the personalized email bodies.
- Keep `CLASS.md` anonymous.
- Prefer deterministic, auditable grading language over vague praise while
  still conveying warmth, respect, and genuine appreciation for the student's
  effort.
- The email greeting and closing in `EMAIL.json` must follow the class-based
  formal or informal rules exactly.
- `EMAIL.json` bodies must preserve the paragraph spacing and readable newline
  structure from the corresponding individual assessments.

## Output Expectations

- `GRADINGS.md` with class-wide grading overview.
- `INDIVIDUAL.md` with detailed per-student feedback.
- `CLASS.md` with anonymized class patterns and teacher recommendations.
- `EMAIL.json` with one personalized email payload per student.
