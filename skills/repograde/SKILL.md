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

This skill relies on `grading-shared` for: address style, email formulas,
second-person address rules, database lookup, email JSON structure, repository
analysis protocol, homework discovery protocol, bulk grading concurrency,
German/UTF-8 constraints, and reporting protocol.

Derive output filenames from the repository basename, while using the provided
repository path verbatim to locate the repository.

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
2. Navigate to the student repository at path $1.
3. Follow the `grading-shared` Pre-Grading Verification.
4. Derive the output stem from `basename "$1"` or equivalent.
5. Discover homework assignments using the `grading-shared` Homework Discovery
   Protocol and build a unified homework list. If no homework is found, stop
   immediately. (Homework files are NEVER inside the student repository.)
6. Follow the `grading-shared` Repository Analysis Protocol to inspect the
   repository history and actual commit content, not just commit messages.
7. Evaluate work against the homework periods and produce an updated grading
   result.
8. Do not write `INDIVIDUAL.md`.
9. Do not write `CLASS.md`.
10. Do not modify shared `EMAIL.json`.
11. Generate `<basename>_grading.md` as the repository grading report.
12. Generate `<basename>_email.json` as a JSON array with exactly one object,
    following `grading-shared` Email JSON Structure.

### 2. Bulk mode

Use this mode when no argument is provided.

Protocol:

1. Enumerate student repositories following the `grading-shared` Bulk Grading
   Protocol directory exclusion rules.
2. Follow the `grading-shared` Bulk Grading    Protocol for concurrency (default
   max 5, ~3 second delay between runs).
3. Each subagent writes only `<basename>_grading.md` plus
    `<basename>_email.json`.
4. Subagents must never write shared `EMAIL.json`.
5. Continue until all repositories are processed.
6. After all subagents finish, aggregate per-repo `*_email.json` files into
   shared `EMAIL.json` following `grading-shared` rules.

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

## Constraints

- This skill must NOT be invoked from within a Git repository.
- This skill must NOT clone student repositories; use `git pull` to update.
- If uncommitted changes exist in any student repository, STOP IMMEDIATELY.
- Do not commit changes or modify repository history.
- All grading content follows `grading-shared` rules (German, second-person,
  UTF-8 umlauts, email structure, missing email handling).
- In single-repo mode, stop if no homework source is found from any location.
- In single-repo mode, never write `INDIVIDUAL.md` or `CLASS.md`.
- In single-repo mode, never modify shared `EMAIL.json`.
- In bulk mode, generate `GRADINGS.md` with class-wide overview table after all
  per-repo grading is complete.
- In bulk mode, generate shared `EMAIL.json` only after all per-repo outputs
  are complete.
- Use proper quoting for paths with spaces.
