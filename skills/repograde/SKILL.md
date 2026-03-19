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
mode for address style, email formulas, database lookup, and email JSON
structure.

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
2. Verify that `Hausübungen.md` exists in the repository. If it does not,
   stop immediately.
3. Read `Hausübungen.md` to identify homework periods and expectations.
4. Inspect the repository history and actual commit content, not just commit
   messages.
5. Evaluate work against the homework periods and produce an updated grading
   result.
6. Update `INDIVIDUAL.md` with the refreshed German grading.
7. Optionally update `CLASS.md` if a class-level nudge or pattern update is
   warranted. Keep `CLASS.md` anonymous.
8. Do not modify shared `EMAIL.json`.
9. Generate `$1_email.json` semantics for the provided repository target as a
   JSON array with exactly one object, following `grading-shared` structure.

### 2. Bulk mode

Use this mode when no argument is provided.

Protocol:

1. Treat each directory in the current folder as one student repository.
2. Maintain dynamic concurrency with a default maximum of 4 repositories in
   progress at once.
3. When one grading run completes, start the next after an approximately
   3-second delay.
4. Continue until all repositories are processed.
5. Produce the expected grading outputs for all repositories.
6. Generate shared `EMAIL.json` only in bulk mode, using `grading-shared`
   rules.

## Repository Analysis

In both modes, inspect repository content directly.

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
`Hausübungen.md`.

- Identify assignment periods from the homework list.
- Match commits to the corresponding homework period by date and content.
- Summarize coverage, diligence, and missing or late work per assignment.
- Base judgments on actual code and text changes, not only on commit messages.

## Outputs

### Single-repo mode

- Updated `INDIVIDUAL.md` in German
- Optionally updated `CLASS.md` in German and anonymized
- A one-entry JSON array for the repository-specific email payload following
  `grading-shared` rules

### Bulk mode

- Per-student grading outputs in German
- Shared `EMAIL.json` built from the individual grading results and
  `grading-shared` rules

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

All grading content must be written in German.

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

## Constraints

- Do not commit changes or modify repository history.
- In single-repo mode, stop if `Hausübungen.md` is missing.
- In single-repo mode, never write shared `EMAIL.json`.
- In bulk mode, keep the concurrent grading workflow.
- Use proper quoting for paths with spaces.
- Preserve natural German umlauts in generated German content.
