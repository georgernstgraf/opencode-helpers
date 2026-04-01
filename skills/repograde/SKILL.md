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
1. Discovering homework assignments from two possible sources (see Homework
   Discovery below):
   - **Legacy**: a cumulative `Hausübungen.md` in the CWD
   - **Per-lesson**: individual `Hausübung.md` files inside `<date>_<topic>`
     subdirectories
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
2. Verify that at least one homework source exists (legacy `Hausübungen.md`
   in CWD, or per-lesson `Hausübung.md` files in subdirectories). If neither
   exists, stop immediately. (Homework files are NEVER inside the student
   repository.)
3. Navigate to the student repository at path $1.
4. Run `git pull` to verify latest version is checked out.
5. Run `git status` to check for uncommitted changes. If found, stop immediately.
6. Derive the output stem from `basename "$1"` or equivalent.
7. Discover homework assignments from both sources (see Homework Discovery
   below) and build a unified homework list.
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
2. Maintain dynamic concurrency with a default target of 5 repository subagents in
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

## Homework Discovery (CRITICAL)

Homework assignments may exist in two formats. The skill MUST discover and
merge both sources into a unified homework list before matching against student
commits.

### Source 1: Legacy Cumulative File (`Hausübungen.md`)

Check for a `Hausübungen.md` file in the current working directory (may be a
symbolic link; follow symlinks when reading).

If found, parse it using the full semantic date analysis below.

#### Semantic Date Extraction

**You MUST perform a thorough semantic analysis of the entire file.**

Many agents fail at this step because they:
- Only read the first entry
- Miss dates embedded in the text (not just headings)
- Fail to convert German date formats to ISO
- Skip entries that don't match a naive pattern match

Required steps:

1. **Read the ENTIRE file** — do not stop after the first homework entry
2. **Extract ALL date references** from:
   - Headings: `## Hausübung vom 18. Februar`
   - Inline dates: `Abgabe bis 25. Februar`
   - Date ranges: `Zeitraum: 10.-18. März`
   - Relative dates: `nächste Woche`, `in 2 Wochen` (convert to absolute)
3. **Normalize ALL dates to ISO format** (YYYY-MM-DD)
4. **Build a homework list**: `[(iso_date, topic, content), ...]`

Date patterns to recognize:

| Pattern | Example | Extraction |
|---------|---------|------------|
| `vom DD. Monat` | `vom 18. Februar` | 2026-02-18 (infer year) |
| `vom DD. Monat YYYY` | `vom 18. Februar 2026` | 2026-02-18 |
| `DD.MM.YYYY` | `18.02.2026` | 2026-02-18 |
| `bis DD. Monat` | `Abgabe bis 25. Februar` | 2026-02-25 (deadline) |
| `Zeitraum: DD.-DD. Monat` | `Zeitraum: 10.-18. März` | 2026-03-10 to 2026-03-18 |

Month name mapping:

```
Januar = 01    Juli = 07
Februar = 02   August = 08
März = 03      September = 09
April = 04     Oktober = 10
Mai = 05       November = 11
Juni = 06      Dezember = 12
```

When year is not explicit, infer from the grading context or cross-reference
with commit dates.

### Source 2: Per-Lesson Files (`Hausübung.md` in `<date>_<topic>` directories)

Scan the CWD for subdirectories matching the pattern `<YYYY-MM-DD>_<topic>`.
For each matching directory, check if `Hausübung.md` exists inside it.

If found:
- Extract the date directly from the directory name (e.g., `2026-03-21_promises`
  → date `2026-03-21`). No German date parsing needed.
- Extract the topic from the directory name and/or the file content.
- Read the file content for assignment details.
- Add to the homework list: `(iso_date, topic, content)`.

### Merging Both Sources

1. Collect homework entries from both sources into a single unified list.
2. If both sources contain an entry for the same date, prefer the per-lesson
   file. This is expected to be rare.
3. Sort the unified list by date.
4. If neither source provides any homework entries, report this to the user
   and grade based on available work only.

## Homework Matching

After repository analysis, map the detected work onto the unified homework list.

### Step-by-Step Matching Process

1. **Parse ALL homework entries** from the unified list.

2. **Match commits to homework**:
   - For each commit, determine which homework it relates to
   - Use commit date + content to identify the relevant homework period
   - A commit dated `2026-02-20` likely belongs to homework dated `2026-02-18`

3. **Build completion status for ALL homeworks**:
   - List all homeworks in the unified list
   - Mark each as completed (✅) or missing (❌)

### Important Considerations

- **Parse ALL entries before matching** — never stop at the first entry
- **Convert all dates to ISO format** — use the same format for comparison
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
- `GRADINGS.md` with a comprehensive table of all students ordered
  alphabetically by name, including repository identifiers and final scores
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

### Example Structure

```markdown
# Bewertungen

| Name | Endbewertung |
|------|-------------|
| Huber Maria | 85/100 |
| Maier Thomas | 72/100 |
| Schmidt Anna | 91/100 |
```

## Email and Database Rules

Always use `grading-shared` for:

- class-to-address-style mapping
- greeting and closing formulas
- gender fallback protocol
- database lookup using `/home/georg/OneDrive/uploadthing.db`
- email payload structure and paragraph preservation
- **missing email address handling** (STOP if any student has no email)

If any student cannot be matched in the database, follow the missing email
protocol in `grading-shared`: stop, present all unresolved names to the user,
and wait for database update before retrying.

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
- In single-repo mode, stop if no homework source is found (neither legacy
  `Hausübungen.md` nor per-lesson `Hausübung.md` files).
- In single-repo mode, never write `INDIVIDUAL.md` or `CLASS.md`.
- In single-repo mode, never write shared `EMAIL.json`.
- In bulk mode, generate `GRADINGS.md` with class-wide overview table after all
  per-repo grading is complete.
- In bulk mode, keep the concurrent grading workflow and generate shared
  `EMAIL.json` only after all per-repo outputs are complete.
- Use proper quoting for paths with spaces.
- Preserve natural German umlauts in generated German content.
