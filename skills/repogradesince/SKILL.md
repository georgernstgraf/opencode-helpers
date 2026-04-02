---
name: repogradesince
description: Grade student repositories filtering commits after a specified date
license: MIT
compatibility: opencode
metadata:
  category: education
  scope: execution
---

# Repogradesince Skill

## Purpose

This skill grades student Git repositories identically to `repograde`, but only
processes commits that occurred after a specified cutoff date. This is useful
for incremental grading, catching up on work after absences, or focusing on
recent submissions.

This skill relies on `grading-shared` for: address style, email formulas,
second-person address rules, database lookup, email JSON structure, repository
analysis protocol, homework discovery protocol, bulk grading concurrency,
German/UTF-8 constraints, and reporting protocol.

## Execution Context

This skill operates from a local folder (current working directory), NOT from
within a Git repository. Calling this skill from inside a Git repository is
an error.

The CWD contains student Git repositories as subdirectories. It may also
contain a `_class` symlink pointing to the corresponding class folder in the
teaching repository (e.g., `_class -> /home/georg/gitm/GRG-SWP/2ahwii/`).
This symlink provides access to homework assignments and lesson materials.

The skill grades student Git repositories by:
1. Discovering homework assignments from multiple sources using the
   `grading-shared` Homework Discovery Protocol
2. Accessing student repositories at the paths provided (these already exist;
   do NOT clone them)
3. Using `git pull` to verify the latest version is checked out
4. Inspecting the repository content for grading, filtered by commit date

## Input

- `$1` (required): ISO date string in format `YYYY-MM-DD` (e.g., `2025-03-15`)
- `$2` (optional): explicit repository path

Behavior:

- If `$1` does not match the ISO date format `YYYY-MM-DD`, STOP IMMEDIATELY
  with an error message indicating the expected format.
- If `$2` is provided after the date, treat it as an explicit repository path
  and use it verbatim for single-repo mode.
- If only the date is provided, run bulk mode for multiple student repositories
  in the current folder.

## Date Handling

### Validation

The date parameter MUST strictly follow ISO 8601 date format:

```
YYYY-MM-DD
```

Where:
- `YYYY` is a 4-digit year
- `MM` is a 2-digit month (01-12)
- `DD` is a 2-digit day (01-31)

Examples of valid dates:
- `2025-03-15`
- `2024-12-01`
- `2025-01-31`

Examples of invalid dates:
- `2025-3-15` (month must be 2 digits)
- `15-03-2025` (wrong order)
- `2025/03/15` (wrong separator)
- `2025-03-5` (day must be 2 digits)
- `2025-03-15T10:00` (time component not allowed)
- `2025-03` (incomplete date)

If the date parameter is invalid:
1. STOP IMMEDIATELY
2. Report the error clearly: "Invalid date format: '[input]'. Expected ISO date format: YYYY-MM-DD (e.g., 2025-03-15)"
3. Do not proceed with any repository operations

### Filtering Logic

For each repository, filter commits as follows:

1. Parse the cutoff date as `YYYY-MM-DD`
2. Convert to datetime: `YYYY-MM-DDT00:00:00` (midnight at start of that day)
3. For each commit in the repository history:
   - Retrieve commit date using `git log --format=%ci` or equivalent
   - Compare commit datetime against the cutoff datetime
   - Include only commits where `commit_date >= cutoff_date`
   - That is: include commits from 0:00 AM of the specified date onwards

4. If no commits match the date filter for a repository:
   - Report this in the grading output
   - Continue to the next repository (do not fail the entire run)

### Git Commands for Date Filtering

Use the following approach to filter commits:

```bash
git log --after="YYYY-MM-DD" --format="%H %ci %s"
```

Or equivalently:

```bash
git log --format="%H %ci" | while read sha date time tz; do
  # Compare date against cutoff
done
```

## Modes

### 1. Single-repo mode

Use this mode when `$2` (repository path) is provided.

Protocol:

1. Validate `$1` as ISO date format. If invalid, STOP IMMEDIATELY.
2. Set cutoff date to `$1` at 0:00 AM.
3. Treat `$2` as the target repository path exactly as passed.
4. Navigate to the student repository at path `$2`.
5. Follow the `grading-shared` Pre-Grading Verification.
6. Derive the output stem from `basename "$2"` or equivalent.
7. Discover homework assignments using the `grading-shared` Homework Discovery
   Protocol and build a unified homework list. If no homework is found, stop
   immediately. (Homework files are NEVER inside the student repository.)
8. **Filter commits**: Only inspect commits dated at or after `$1T00:00:00`.
9. Follow the `grading-shared` Repository Analysis Protocol to inspect filtered
   repository history and actual commit content.
10. Evaluate work against the homework periods (only for matching date ranges).
11. Generate `<basename>_grading.md` as the repository grading report.
12. Generate `<basename>_email.json` as a JSON array with exactly one object,
    following `grading-shared` Email JSON Structure.

### 2. Bulk mode

Use this mode when only `$1` (date) is provided.

Protocol:

1. Validate `$1` as ISO date format. If invalid, STOP IMMEDIATELY.
2. Set cutoff date to `$1` at 0:00 AM.
3. Enumerate student repositories following the `grading-shared` Bulk Grading
   Protocol directory exclusion rules.
4. Follow the `grading-shared` Bulk Grading    Protocol for concurrency (default
   max 5, ~3 second delay between runs).
5. Each subagent writes only `<basename>_grading.md` plus
   `<basename>_email.json`.
6. Subagents must never write shared `EMAIL.json`.
7. Continue until all repositories are processed.
8. After all subagents finish, aggregate per-repo `*_email.json` files into
   shared `EMAIL.json` following `grading-shared` rules.

## Homework Matching

After repository analysis, map the detected work onto the unified homework list.

### Step-by-Step Matching Process

1. **Parse ALL homework entries** from the unified list.

2. **Identify relevant homework for the cutoff date**:
   - A homework assignment is RELEVANT if its date is **on or after** the
     cutoff date, OR if it spans a period that includes the cutoff date
   - Example: Cutoff `2026-02-10`, homework dated `2026-02-18` → this
     homework is assigned AFTER the cutoff and should be considered as
     "upcoming work" that the student should have completed

3. **Match commits to homework**:
   - For each commit after cutoff date, determine which homework it relates to
   - Use commit date + content to identify the relevant homework period
   - A commit dated `2026-02-20` likely belongs to homework dated `2026-02-18`

4. **Build completion status for ALL relevant homeworks**:
   - List all homeworks with dates on or after cutoff
   - Mark each as completed (✅) or missing (❌)

### Matching Examples

| Cutoff Date | Homework Date | Match? | Reason |
|-------------|---------------|--------|--------|
| 2026-02-10 | 2026-02-18 | ✅ YES | Homework assigned after cutoff, student should have done it |
| 2026-02-10 | 2026-02-05 | ❌ NO | Homework assigned before cutoff period |
| 2026-02-10 | 2026-02-10 | ✅ YES | Exact match |
| 2026-02-10 | 2026-03-01 | ✅ YES | Homework within grading period |

### Important Considerations

- **Parse ALL entries before matching** — never stop at the first entry
- **Convert all dates to ISO format** — use the same format for comparison
- **Include homework from the cutoff date onwards** — not just commits
- Clearly indicate in the report that grading covers commits from
  `[cutoff date]` onwards.
- Base judgments on actual code and text changes, not only on commit messages.

## Homework Completion Weighting (CRITICAL)

This section is essential for fair grading. A student who completes only a
subset of assigned homework must receive a proportionally reduced score.

### Completion Ratio Calculation

For each homework assignment in the grading period:

1. Identify ALL homework assignments from the unified homework list that fall
   within or after the cutoff date.
2. For each assignment, determine if the student has substantive work
   (not just superficial edits).
3. Calculate the completion ratio:

```
completion_ratio = completed_assignments / total_assignments
```

Example: If 3 homeworks are assigned and student completed 2:
- completion_ratio = 2/3 ≈ 0.67

### Scoring Impact

The final score MUST reflect incomplete homework proportionally:

1. Calculate a base score from quality of completed work (0-100).
2. Apply completion weighting:

```
weighted_score = base_score * completion_ratio
```

**Example of correct weighting:**

|Assigned| Completed | Base Score | Weighted Score |
|--------|-----------|------------|----------------|
| 3| 3 | 90 | 90 (90 × 1.0) |
| 3| 2 | 90 | 60 (90 × 0.67) |
| 3| 1 | 95 | 32 (95 × 0.33) |

**Anti-Pattern (DO NOT DO THIS):**
Assigning 90% to a student who only completed 1 of 3 assignments just because
that one assignment was excellent. This is incorrect and unfair to students
who completed all work.

### Missing Assignment Documentation

In the grading report, explicitly list:

- All assigned homeworks for the period
- Which were completed (with brief summary)
- Which were missing or incomplete

Example German phrasing:

```
##Hausübungs-Abdeckung

Insgesamt waren 3 Hausübungen im Bewertungszeitraum aufgegeben:
- HU1: ✅vollständig bearbeitet
- HU2: ❌ nicht bearbeitet
- HU3: ❌ nicht bearbeitet

Abdeckungsquote: 1von3(33%)

DieEndbewertung berücksichtigt diese unvollständige Abdeckung entsprechend.
```

### Grading Report Requirements

Every grading report MUST include:

1. **Hausübungs-Abdeckung section**: List all assignments and completion status
2. **Abdeckungsquote**: The completion ratio as percentage
3. **Weighted final score**: Base score multiplied by completion ratio
4. **Clear explanation**: Why the score is what it is

### Edge Cases

- **No homeworks in period**: If no assignments fall within the grading period,
  report this clearly and grade based on available work only.
- **Empty repository**: If the student has no commits after the cutoff date,
  assign 0points with clear explanation.
- **Late submissions**: Note late submissions separately; they may still count
  toward completion at reduced weight per instructor policy.

## Outputs

### Single-repo mode

- `<basename>_grading.md` in German
- `<basename>_email.json` as a one-entry JSON array following `grading-shared`
  rules

### Bulk mode

- Per-repository `<basename>_grading.md` files in German
- Per-repository `<basename>_email.json` files following `grading-shared`
  rules
- `GRADINGS.md` with a comprehensive table of all students ordered
  alphabetically by name, including repository identifiers and final scores
- `CLASS.md` with anonymized class-wide patterns and teacher recommendations
  (written in German, no student names, suitable for public repository use)
- Shared `EMAIL.json`, created only by the master workflow after all per-repo
  outputs are finished

## GRADINGS.md Generation (Bulk Mode Only)

After all per-repository grading is complete in bulk mode, generate `GRADINGS.md`
as a class-wide overview table.

### Content Requirements

`GRADINGS.md` MUST include:

1. A table with columns for student identifier (repository basename or name) and
   final score (`Endbewertung`)
2. Ordered alphabetically by student name, NOT by grade
3. Written in German
4. Clear indication of the cutoff date in a header or introduction

### Example Structure

```markdown
# Bewertungen (ab YYYY-MM-DD)

| Name | Endbewertung |
|------|-------------|
| Huber Maria | 85/100 |
| Maier Thomas | 72/100 |
| Schmidt Anna | 91/100 |
```

## CLASS.md Generation (Bulk Mode Only)

After all per-repository grading is complete in bulk mode, generate `CLASS.md`
as an anonymized class summary for the teacher.

### Content Requirements

`CLASS.md` MUST include:

1. **Overview**: Summary of the grading period (cutoff date, number of
   repositories graded)
2. **Common Patterns**: Frequently observed strengths across submissions
3. **Common Weaknesses**: Recurring issues or mistakes
4. **Homework Completion Statistics**: Aggregate completion ratios
5. **Teacher Recommendations**: Actionable suggestions for addressing issues

### Anonymity Rules

- NEVER include student names or repository names that identify individuals
- Use generic terms: "einige Schüler", "viele Abgaben", "vereinzelt"
- Focus on patterns, not individuals
- This file may be committed to a public repository

### Example Structure

```markdown
# Klassenzusammenfassung

## Bewertungszeitraum
Bewertet wurden Commits ab dem YYYY-MM-DD.
Anzahl der bewerteten Repositories: N

## Gemeinsame Stärken
- ...

## Häufige Schwächen
- ...

## Hausübungserledigung
Durchschnittliche Abdeckungsquote: X%

## Empfehlungen
- ...
```

## Reporting Expectations

Reports MUST follow `grading-shared` Reporting Protocol and additionally include:

- clear indication of the cutoff date (Commits von YYYY-MM-DD onwards)
- **Hausübungs-Abdeckung section**: Complete list of all assigned homeworks
  with completion status (✅/❌) and Abdeckungsquote percentage
- **weighted final evaluation**: Base score × completion ratio
- final evaluation with `Endbewertung: XX/100` (the weighted score, not base)

## Constraints

- This skill must NOT be invoked from within a Git repository.
- This skill must NOT clone student repositories; use `git pull` to update.
- If uncommitted changes exist in any student repository, STOP IMMEDIATELY.
- If the date parameter is not a valid ISO date (YYYY-MM-DD), STOP IMMEDIATELY.
- Do not commit changes or modify repository history.
- All grading content follows `grading-shared` rules (German, second-person,
  UTF-8 umlauts, email structure, missing email handling).
- In single-repo mode, stop if no homework source is found.
- In single-repo mode, never write `INDIVIDUAL.md` or `CLASS.md`.
- In single-repo mode, never write shared `EMAIL.json`.
- In bulk mode, generate `GRADINGS.md` and `CLASS.md` after all per-repo
  grading is complete.
- In bulk mode, generate shared `EMAIL.json` only after all per-repo outputs
  are complete.
- Use proper quoting for paths with spaces.
