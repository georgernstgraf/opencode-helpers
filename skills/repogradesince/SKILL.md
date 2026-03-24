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

This skill must use the `grading-shared` skill in both single-repo and bulk
mode for address style, email formulas, database lookup, email JSON
structure, and second-person address requirements.

## Execution Context

This skill operates from a local folder (current working directory), NOT from
within a Git repository. Calling this skill from inside a Git repository is
an error.

The skill grades student Git repositories by:
1. Reading `Hausübungen.md` from the current working directory
   (may be a symbolic link; follow symlinks when reading)
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
# Get commits after the cutoff date
git log --after="YYYY-MM-DD" --format="%H %ci %s"
```

Or equivalently:

```bash
# Get all commits and filter by date
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
4. Verify that `Hausübungen.md` exists in the current working directory.
   If it does not, stop immediately. (Hausübungen.md is NEVER inside the
   student repository.)
5. Navigate to the student repository at path `$2`.
6. Run `git pull` to verify latest version is checked out.
7. Run `git status` to check for uncommitted changes. If found, stop immediately.
8. Derive the output stem from `basename "$2"` or equivalent.
9. Read `Hausübungen.md` from the current working directory to identify
   homework periods and expectations.
10. **Filter commits**: Only inspect commits dated at or after `$1T00:00:00`.
11. Inspect the filtered repository history and actual commit content.
12. Evaluate work against the homework periods (only for matching date ranges).
13. Generate `<basename>_grading.md` as the repository grading report.
14. Generate `<basename>_email.json` as a JSON array with exactly one object,
    following `grading-shared` structure.

### 2. Bulk mode

Use this mode when only `$1` (date) is provided.

Protocol:

1. Validate `$1` as ISO date format. If invalid, STOP IMMEDIATELY.
2. Set cutoff date to `$1` at 0:00 AM.
3. Treat each directory path as a student repository to grade.
4. Maintain dynamic concurrency with a default maximum of 5 repositories in
   progress at once.
5. When one grading run completes, start the next after an approximately
   3-second delay.
6. Each subagent must derive its output stem from the repository basename and
   write only `<basename>_grading.md` plus `<basename>_email.json`.
7. Subagents must never write shared `EMAIL.json`.
8. Continue until all repositories are processed.
9. After all subagents finish, the master workflow must read the generated
   `*_email.json` files and create shared `EMAIL.json` using `grading-shared`
   rules.

## Repository Analysis

In both modes, inspect only filtered repository content (commits meeting the
date criteria).

### Pre-Grading Verification

Before inspecting repository content, verify repository state:

1. Navigate to the student repository directory
2. Run `git pull` to ensure latest version is checked out
3. Run `git status` to check for uncommitted changes
4. If uncommitted changes exist, STOP IMMEDIATELY and report to user
5. If pull fails or reports errors, STOP IMMEDIATELY and report to user

### Discovery

- Identify relevant branches.
- Enumerate commits, filtering to only those at or after the cutoff date.
- Avoid duplicate SHA processing.
- Collect commit metadata: SHA, author, date, branch context, and message.

### Per-commit inspection

For every relevant commit (after cutoff date), inspect actual changes:

- `git show --stat --summary <sha>`
- `git show --format=fuller --unified=3 <sha>`

Use diff content, not filenames alone, to identify what the student worked on.

### Topic detection

Detect technical topics from the diffs and distinguish substantive work from
superficial edits.

- substantive: meaningful implementation, debugging, refactoring, feature work
- superficial: formatting-only edits, whitespace changes, trivial renames,
  auto-generated files without meaningful modification

Consider common patterns across JavaScript, Java, C#, SQL, CSS, HTML, and
general programming constructs.

### Branch and activity analysis

- Focus primarily on `main`, but highlight significant non-main branch work.
- Count commits over time (only counting commits after the cutoff date).
- Detect inactive gaps between first and last relevant commits.
- Use evidence-based diligence signals such as `high`, `medium`, or `low`.

## Homework Matching

After repository analysis, map the detected work onto the homework schedule in
`Hausübungen.md` (from the current working directory).

- Identify assignment periods from the homework list.
- Match commits to the corresponding homework period by date and content.
- **Important**: Only include homework periods that overlap with or follow the
  cutoff date.
- Summarize coverage, diligence, and missing or late work per assignment.
- Base judgments on actual code and text changes, not only on commit messages.
- Clearly indicate in the report that grading covers commits from
  `[cutoff date]` onwards.

## Homework Completion Weighting (CRITICAL)

This section is essential for fair grading. A student who completes only a
subset of assigned homework must receive a proportionally reduced score.

### Completion Ratio Calculation

For each homework assignment in the grading period:

1. Identify ALL homework assignments from `Hausübungen.md` that fall within
   or after the cutoff date.
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
- Shared `EMAIL.json`, created only by the master workflow after all per-repo
  outputs are finished

## Email and Database Rules

Always use `grading-shared` for:

- class-to-address-style mapping
- greeting and closing formulas
- gender fallback protocol
- database lookup using `/home/georg/OneDrive/uploadthing.db`
- email payload structure and paragraph preservation

If a student cannot be matched in the database:

- set `mailto` to `null`
- add a note for manual review
- do not invent contact data

## Reporting Expectations

All grading content must be written in German and address the student
directly in the second person (Sie or Du based on class).

Reports MUST include:

- clear indication of the cutoff date (Commits von YYYY-MM-DD onwards)
- **Hausübungs-Abdeckung section**: Complete list of all assigned homeworks
  with completion status (✅/❌) and Abdeckungsquote percentage
- repository overview
- homework-by-homework summary (filtered to relevant periods)
- topic coverage
- per-commit technical analysis (only commits after cutoff)
- non-main branch activity
- activity over time
- inactive gaps
- diligence assessment
- **weighted final evaluation**: Base score × completion ratio
- final evaluation with `Endbewertung: XX/100` (the weighted score, not base)

## Constraints

- This skill must NOT be invoked from within a Git repository.
- This skill must NOT clone student repositories; use `git pull` to update.
- If uncommitted changes exist in any student repository, STOP IMMEDIATELY.
- If the date parameter is not a valid ISO date (YYYY-MM-DD), STOP IMMEDIATELY.
- Do not commit changes or modify repository history.
- All grading content must use second-person address (Sie or Du).
- Never use third-person references to the student.
- In single-repo mode, stop if `Hausübungen.md` is missing.
- In single-repo mode, never write `INDIVIDUAL.md` or `CLASS.md`.
- In single-repo mode, never write shared `EMAIL.json`.
- In bulk mode, keep the concurrent grading workflow and generate shared
  `EMAIL.json` only after all per-repo outputs are complete.
- Use proper quoting for paths with spaces.
- Preserve natural German umlauts in generated German content.