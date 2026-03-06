# Knowledge Assessment Skill

## Purpose

This skill assesses student submissions for a knowledge-check exam, produces
teacher-facing reports in German, and prepares structured email payloads for
communicating individual results.

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
- Create `EMAIL.json` as a JSON array.
- Each object must contain exactly these fields:
  - `mailto`: recipient email address
  - `subject`: `Ergebnis der Wissensueberpruefung am <isodate>`
  - `body`: the student's individual assessment text
- Address students using the polite German form `Sie`.

### 5. Constraints

- Write all report files in German.
- Treat `INDIVIDUAL.md` as the source for the personalized email bodies.
- Keep `CLASS.md` anonymous.
- Prefer deterministic, auditable grading language over vague praise.

## Output Expectations

- `GRADINGS.md` with class-wide grading overview.
- `INDIVIDUAL.md` with detailed per-student feedback.
- `CLASS.md` with anonymized class patterns and teacher recommendations.
- `EMAIL.json` with one personalized email payload per student.
