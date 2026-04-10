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

## Dependencies

This skill relies on `grading-shared` for: address style, email formulas,
second-person address rules, database lookup, email JSON structure,
German/UTF-8 constraints, and reporting protocol.

## Execution Context

This skill operates from a local folder (current working directory), NOT from
within a Git repository. Calling this skill from inside a Git repository is
an error.

The skill grades student submissions located in the current working directory
alongside knowledge-check solution files.

## Inputs

- Student submission files in the current working directory (local folder,
  NOT a Git repository); each submission filename contains the class
  identifier that determines whether formal or informal address should be used
- Matching knowledge-check files with questions and solutions, including a
  solutions file in the same directory that can be used as the reference for
  correct answers and for the total achievable points listed at the bottom of
  that file
- `vacuum.db` for student email address lookup; must exist in the current
  working directory at start; if missing, stop immediately (do not create or copy)

## Protocol

### 1. Discover Assessment Inputs

- Inspect the current directory for student submission files and the matching
  knowledge-check files containing the questions and solutions.
- Derive the class for each submission from its filename.
- Determine the addressing style from the class using the centralized
  configuration in `grading-shared` skill.
- If a student submitted multiple versions, grade only the highest version.
- Read any student comments where they used `-` to mark an answer as ambiguous
  or context-dependent, and consider that explanation during assessment.

### 2. Grade Submissions

- Evaluate each submission against the available solutions.
- Read the total achievable points from the bottom of the knowledge solutions
  Markdown file and treat that value as the authoritative total.
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
- When parsing free-text answers, treat text that starts immediately after a
  separator such as `---` on the same line as a valid answer, not as an empty
  section.
- More generally, do not classify a free-text response as unanswered before
  checking whether substantive answer text appears on the same line as a
  heading or separator, or directly after Markdown markers.

### 3. Create Report Files

- Create `GRADINGS.md` in German.
- Include a comprehensive table ordered alphabetically by student name, not by
  grade.
- Create `<name>_grading.md` for each student in German (e.g., `haas_alexander_grading.md`).
- Address each student directly in the second person (Sie or Du based on class).
- Provide a relatively detailed assessment for each student's submission.
- Ensure every reported score in the grading file is consistent with the
  authoritative total achievable points from the solutions file.
- Use a respectful teacher-to-student tone that is friendly, warm, and
  encouraging without becoming inappropriately informal.
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
- Do NOT create `INDIVIDUAL.md` (deprecated; use per-student `<name>_grading.md` files).

### Example: Second-Person Tone in `<name>_grading.md` (Informal/2ahwii)

```
# Bewertung: Haas Alexander (2AHWII)

Du hast bei dieser Wissensüberprüfung insgesamt 72 von 80 Punkten erreicht.
Das ist eine solide Leistung.

## Stärken

Du hast Frage 3 (SQL-JOINs) vollständig und korrekt beantwortet. Auch bei
Frage 7 (Normalisierung) hast du die Grundkonzepte gut verstanden.

## Verbesserungspotenzial

Bei Frage 4 (Subqueries) wäre etwas mehr Erklärung hilfreich gewesen. Du hast
die Antwort zwar angegeben, aber den Lösungsweg nicht erläutert.

## Empfehlungen

Es empfiehlt sich, die Unterschiede zwischen INNER JOIN und OUTER JOIN noch
einmal zu üben. Nutze dazu die hochgeladene Lösungedatei als Referenz.
```

### Example: Second-Person Tone in `<name>_grading.md` (Formal/Other class)

```
# Bewertung: Huber Maria (5AHIF)

Sie haben bei dieser Wissensüberprüfung insgesamt 68 von 80 Punkten erreicht.
Das ist eine gute Leistung.

## Stärken

Sie haben Frage 3 (SQL-JOINs) vollständig und korrekt beantwortet. Auch bei
Frage 7 (Normalisierung) haben Sie die Grundkonzepte gut verstanden.

## Verbesserungspotenzial

Bei Frage 4 (Subqueries) wäre etwas mehr Erklärung hilfreich gewesen. Sie haben
die Antwort zwar angegeben, aber den Lösungsweg nicht erläutert.

## Empfehlungen

Es empfiehlt sich, die Unterschiede zwischen INNER JOIN und OUTER JOIN noch
einmal zu üben. Nutzen Sie dazu die hochgeladene Lösungedatei als Referenz.
```

### 4. Create Bulk Email JSON

Follow the `grading-shared` skill protocol for:
- Database lookup (use `vacuum.db` in current directory)
- Gender determination and fallback handling
- Email JSON structure
- Greeting and closing formulas
- **Missing email address handling** (STOP if any student has no email)

If any student cannot be matched in the database, follow the missing email
protocol in `grading-shared`: stop, present all unresolved names to the user,
and wait for database update before retrying. Do NOT generate `EMAIL.json`
with null mailto values.

Additional requirements specific to knowledge-check:

- Create `EMAIL.json` as a JSON array.
- Each object must contain exactly these fields (see `grading-shared` for structure):
  - `mailto`: recipient email address
  - `subject`: `Ergebnis der Wissensüberprüfung am <isodate>`
  - `body`: the student's individual assessment text, formatted as plain ASCII
    text following the `grading-shared` Email Body Format section for
    knowledge-check emails
- Ensure every reported score inside the email body is consistent with the
  authoritative total achievable points from the solutions file.
- Use greeting and closing formulas from `grading-shared` based on class
  address style.
- Include this exact first-person note in every email body: `Ich habe die Datei
  mit den korrekten Lösungen in das Git-Repository hochgeladen.` Place this
  note near the end of the body, before the closing formula.
- If gender cannot be determined, use neutral fallback greeting per
  `grading-shared` protocol and flag in the grading file for manual review.
- Email bodies MUST follow the `grading-shared` Email Body Format: plain ASCII
  text, no Markdown formatting except code blocks with backtick fences. Follow
  the knowledge-check email structure defined there.

### 5. Constraints

- This skill must NOT be invoked from within a Git repository.
- Write all report files in German.
- Write `EMAIL.json` bodies in German.
- All student-facing content must use second-person address (Sie or Du).
- Never use third-person references to the student in grading files or emails.
- Use per-student `<name>_grading.md` files as the source for personalized email bodies.
- Keep `GRADINGS.md` as a class-wide overview table.
- Keep `CLASS.md` anonymous for public repository use.
- UTF-8 is explicitly allowed and preferred in both Markdown and JSON outputs.
- Write German umlauts and Eszett in natural UTF-8 form in generated `.md`
  and `.json` files, for example `ä`, `ö`, `ü`, `Ä`, `Ö`, `Ü`, and `ß`.
- Do not replace German umlauts with transliterations such as `ae`, `oe`, or
  `ue` unless the surrounding source material explicitly requires that form.
- Prefer deterministic, auditable grading language over vague praise while
  still conveying warmth, respect, and genuine appreciation for the student's
  effort.
- Follow email constraints from `grading-shared` (greeting, closing, trailing
  comma, paragraph spacing, email body format, praise guidelines).
- If any point-total consistency error appears between the solutions file,
  grading files, or `EMAIL.json`, stop immediately instead of generating or
  continuing with inconsistent output.

## Output Expectations

- `GRADINGS.md` with class-wide grading overview (mandatory)
- `CLASS.md` with anonymized class patterns and teacher recommendations (mandatory)
- `<name>_grading.md` files (one per student) with detailed individual feedback
- `EMAIL.json` with one personalized email payload per student
