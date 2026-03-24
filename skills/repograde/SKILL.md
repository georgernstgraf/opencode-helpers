---
name: repograde
description: Grade student repositories in single-repo or bulk mode
license: MIT
compatibility: opencode
metadata:
  category: education
  scope: execution
---

# Repograde Skill

## Purpose

This skill is the canonical workflow for grading student Git repositories.
It absorbs the former `repo-report` analysis behavior into a grading-specific
workflow so repository inspection, homework matching, report writing, and email
payload generation live in one place.

This skill must use the `grading-shared` skill in both single-repo and bulk
mode for address style, email formulas, database lookup, email JSON
structure, and second-person address requirements.

Derive output filenames from the repository basename, while using the provided
repository path verbatim to locate the repository.

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
4. Inspecting the repository content for grading

## Input

- `$1` (optional): explicit repository path

Behavior:

- If exactly one argument is provided, treat it as an explicit repository path
  and use it verbatim.
- If no argument is provided, run bulk mode for multiple student repositories in
  the current folder.

## Modes

### 1. Single-repo mode

Use this mode when `$1` is present.

Protocol:

1. Treat `$1` as the target repository path exactly as passed.
2. Verify that `Hausübungen.md` exists in the current working directory.
   If it does not, stop immediately. (Hausübungen.md is NEVER inside the
   student repository.)
3. Navigate to the student repository at path $1.
4. Run `git pull` to verify latest version is checked out.
5. Run `git status` to check for uncommitted changes. If found, stop immediately.
6. Derive the output stem from `basename "$1"` or equivalent.
7. Read `Hausübungen.md` from the current working directory to identify
   homework periods and expectations.
8. Inspect the repository history and actual commit content, not just commit
   messages.
9. Evaluate work against the homework periods and produce an updated grading
   result.
10. Do not write `INDIVIDUAL.md`.
11. Do not write `CLASS.md`.
12. Do not modify shared `EMAIL.json`.
13. Generate `<basename>_grading.md` as the repository grading report.
14. Generate `<basename>_email.json` as a JSON array with exactly one object,
    following `grading-shared` structure.

### 2. Bulk mode

Use this mode when no argument is provided.

Protocol:

1. Treat each directory path as a student repository to grade. These are
   separate Git repositories (do NOT clone them).
2. Maintain dynamic concurrency with a default maximum of 5 repositories in
   progress at once.
3. When one grading run completes, start the next after an approximately
   3-second delay.
4. Each subagent must derive its output stem from the repository basename and
   write only `<basename>_grading.md` plus `<basename>_email.json`.
5. Subagents must never write shared `EMAIL.json`.
6. Continue until all repositories are processed.
7. After all subagents finish, the master workflow must read the generated
   `*_email.json` files and create shared `EMAIL.json` using `grading-shared`
   rules.

## Repository Analysis

In both modes, inspect repository content directly.

### Pre-Grading Verification

Before inspecting repository content, verify repository state:

1. Navigate to the student repository directory
2. Run `git pull` to ensure latest version is checked out
3. Run `git status` to check for uncommitted changes
4. If uncommitted changes exist, STOP IMMEDIATELY and report to user
5. If pull fails or reports errors, STOP IMMEDIATELY and report to user

### Discovery

- Identify relevant branches.
- Enumerate commits while avoiding duplicate SHA processing.
- Collect commit metadata: SHA, author, date, branch context, and message.

### Per-commit inspection

For every relevant commit, inspect actual changes with commands equivalent to:

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
- Count commits over time.
- Detect inactive gaps between first and last relevant commits.
- Use evidence-based diligence signals such as `high`, `medium`, or `low`.

## Homework Matching

After repository analysis, map the detected work onto the homework schedule in
`Hausübungen.md` (from the current working directory).

- Identify assignment periods from the homework list.
- Match commits to the corresponding homework period by date and content.
- Summarize coverage, diligence, and missing or late work per assignment.
- Base judgments on actual code and text changes, not only on commit messages.

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

Reports should include, where applicable:

- repository overview
- homework-by-homework summary
- topic coverage
- per-commit technical analysis
- non-main branch activity
- activity over time
- inactive gaps
- diligence assessment
- final evaluation with `Endbewertung: XX/100`

### Example: Second-Person Tone (Informal/2ahwii)

```
## Repository-Übersicht

Du hast in diesem Semester durchweg solide Arbeit geleistet. Dein
Repository zeigt eine klare Struktur und regelmäßige Commits.

## Hausübungen

### HU1: SQL-Grundlagen
Du hast die JOIN-Operationen korrekt implementiert. Besonders positiv
ist, dass du die Fremdschlüssel-Beziehung sauber modelliert hast.

### HU2: Normalisierung
Hier wäre etwas mehr Sorgfalt hilfreich gewesen. Du hast die
Dritte Normalform nicht durchgängig eingehalten.
```

### Example: Second-Person Tone (Formal/Other class)

```
## Repository-Übersicht

Sie haben in diesem Semester durchweg solide Arbeit geleistet. Ihr
Repository zeigt eine klare Struktur und regelmäßige Commits.

## Hausübungen

### HU1: SQL-Grundlagen
Sie haben die JOIN-Operationen korrekt implementiert. Besonders positiv
ist, dass Sie die Fremdschlüssel-Beziehung sauber modelliert haben.
```

## Constraints

- This skill must NOT be invoked from within a Git repository.
- This skill must NOT clone student repositories; use `git pull` to update.
- If uncommitted changes exist in any student repository, STOP IMMEDIATELY.
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
