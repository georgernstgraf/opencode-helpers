---
name: projectgrade
description: Grade student project repositories based on Git commits and GitHub Issues
license: MIT
compatibility: opencode
metadata:
  category: education
  scope: execution
---

# Projectgrade Skill

## Purpose

This skill grades student Git repositories for collaborative project work where
students contribute via branches and GitHub Issues. It evaluates both code
contributions (via Git commits) and issue management (creation, editing,
commenting, quality).

Unlike `repograde`, this skill does NOT use homework assignments or `Hausübungen.md`.
Student identification is derived exclusively from Git commit email addresses,
then mapped to student names via the uploadthing database.

This skill must use the `grading-shared` skill for address style, email formulas,
database lookup, email JSON structure, and second-person address requirements.

## Execution Context

This skill operates from a local folder (current working directory), NOT from
within a Git repository. Calling this skill from inside a Git repository is
an error.

The skill grades student project repositories by:
1. Accessing student repositories at the paths provided (these already exist;
   do NOT clone them)
2. Using `git pull` to verify the latest version is checked out
3. Inspecting the repository content and Git history for grading
4. Querying GitHub API for issue metadata (creation, edits, comments)
5. Mapping contributor email addresses to student names via uploadthing.db

## Input

- `$1` (optional): explicit repository path
- `--gh-token`: GitHub token for API access (optional, defaults to environment)

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
3. Run `git pull` to verify latest version is checked out.
4. Run `git status` to check for uncommitted changes. If found, stop immediately.
5. Derive the output stem from `basename "$1"` or equivalent.
6. Extract all unique contributor email addresses from git commits.
7. Query the uploadthing database to map emails to student names.
8. Analyze GitHub Issues participation (see Issue Analysis section).
9. Generate `<basename>_grading.md` as the repository grading report.
10. Generate `<basename>_email.json` as a JSON array with student entries,
    following `grading-shared` structure.

### 2. Bulk mode

Use this mode when no argument is provided.

Protocol:

1. Treat each directory path as a student repository to grade. These are
   separate Git repositories (do NOT clone them).
2. Maintain dynamic concurrency with a default maximum of 4 repositories in
   progress at once.
3. When one grading run completes, start the next after an approximately
   3-second delay.
4. Each subagent must derive its output stem from the repository basename and
   write only `<basename>_grading.md` plus `<basename>_email.json`.
5. Continue until all repositories are processed.
6. After all subagents finish, the master workflow must read the generated
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

### Git Commit Analysis

Extract all unique contributor email addresses:

```bash
git log --all --format='%ae' | sort -u
```

For each contributor, collect commit statistics:

```bash
git log --all --author='<email>' --format='%H' | wc -l  # commit count
git log --all --author='<email>' --format='' --numstat | awk '{added+=$1; deleted+=$2} END {print added, deleted}'
```

### Branch Analysis

- Enumerate all branches: `git branch -a`
- Count commits per branch per author
- Identify significant non-main branch contributions
- Note branch naming patterns and merge activity

### Per-commit Inspection

For significant commits, inspect actual changes:

- `git show --stat --summary <sha>`
- `git show --format=fuller --unified=3 <sha>`

Use diff content to identify substantive vs superficial work:
- substantive: meaningful implementation, debugging, refactoring, feature work
- superficial: formatting-only, whitespace, trivial renames, auto-generated files

## Issue Analysis

This skill evaluates GitHub Issues participation as a key grading factor.

### Issue Discovery

Use GitHub API to fetch repository issues:

```
GET /repos/{owner}/{repo}/issues
GET /repos/{owner}/{repo}/issues/{issue_number}/comments
GET /repos/{owner}/{repo}/issues/{issue_number}/events
```

### Issue Attribution by Email

GitHub API returns `user.login` (username), not email. To attribute issues to
students:

1. Extract all unique email addresses from Git commits
2. For each commit author email, query GitHub API to find their username:
   ```
   GET /search/users?q=<email>+in:email
   ```
3. Or use commit author name and compare to GitHub usernames cautiously
   - Names often differ from usernames
   - Prefer email-based matching for accuracy
4. Map issue activity to student emails via the username lookup

### Issue Metrics

For each contributing student, track:

| Metric | Weight | Description |
|--------|--------|-------------|
| Issues Created | 15% | Number of issues opened |
| Issues Closed | 5% | Issues closed by their PRs |
| Issue Comments | 20% | Constructive comments on discussions |
| Issue Edits | 10% | Improvements to issue descriptions |
| Issue Quality | 25% | Clarity, completeness, reproducibility |
| Commit Quality | 25% | Code quality from commit analysis |

### Issue Quality Rubric

Evaluate issue quality based on:

- **Title clarity**: Descriptive, specific, actionable
- **Description completeness**: Steps to reproduce, expected vs actual behavior
- **Code examples**: Minimal reproducible examples provided
- **Screenshots/logs**: Supporting evidence for bug reports
- **Labels**: Appropriate categorization (bug, enhancement, question)
- **Response to feedback**: Updates based on maintainer comments

### Issue Scoring

For each student's issues:

```
Issue Score = (Quality Rating × Weight) × Count Factor

Quality Rating (1-5):
  5 = Exceptional: Complete, clear, with reproducible examples
  4 = Good: Well-described with most relevant details
  3 = Average: Adequate description but missing some context
  2 = Below Average: Vague, incomplete, or poorly structured
  1 = Poor: No clear description or incorrectly filed

Count Factor:
  More issues > fewer issues (up to reasonable threshold)
  Diminishing returns after ~10 issues per student
```

## Student Identification

### Email Extraction

Extract all unique commit author emails:

```bash
git log --all --format='%ae' | sort -u
```

### Database Lookup

Query uploadthing.db for student identification:

```sql
SELECT email, name, klasse FROM users WHERE email IN (email_list)
```

Database path: `/home/georg/OneDrive/uploadthing.db`

### Address Style

Use `grading-shared` address style mapping based on `klasse`:

| Class | Address Style |
|-------|---------------|
| `2ahwii` | Informal |
| `3ahwii` | Informal |
| `5ahwii` | Informal |
| `4aaif` | Informal |
| All others | Formal |

### Unmatched Students

If an email cannot be matched in the database:
- Set `mailto` to `null` in the email JSON
- Add a `note` field for manual review
- Include the student in grading using the email as identifier
- Do not invent contact data

## Grading Calculation

### Contribution Scoring

| Category | Weight | Metrics |
|----------|--------|---------|
| Commit Activity | 25% | Count, frequency, spread over time |
| Commit Quality | 25% | Code quality, meaningful changes |
| Issue Creation | 15% | Number and quality of issues opened |
| Issue Comments | 20% | Constructive participation in discussions |
| Issue Edits | 10% | Improvements to issue descriptions |
| Issue Quality | 5% | Overall quality of issue management |

### Diligence Assessment

Rate student diligence as `high`, `medium`, or `low` based on:

- Regular commit frequency (not bursts at deadlines)
- Consistent issue involvement throughout project
- Quality of code changes (not superficial)
- Proper branch management and merge requests

### Final Score Calculation

```
Final Score = Σ(Category Score × Weight)
Rounded to nearest integer
Max: 100 points
```

## Outputs

### Single-repo mode

- `<basename>_grading.md` in German
- `<basename>_email.json` as a JSON array following `grading-shared` rules

### Bulk mode

- Per-repository `<basename>_grading.md` files in German
- Per-repository `<basename>_email.json` files following `grading-shared` rules
- Shared `EMAIL.json`, created only by the master workflow after all per-repo
  outputs are finished

## Grading Report Structure

The `<basename>_grading.md` file should include:

```markdown
# Projekt-Bewertung: [Repository Name]

## Beteiligte Studierende

- [Name 1] (email1@example.com)
- [Name 2] (email2@example.com)
...

## Commit-Aktivität

### [Name 1]
- Anzahl Commits: X
- Zeitlicher Verlauf: [Analyse]
- Branches: [Liste]
- Codequalität: [Bewertung]

### [Name 2]
...

## Issue-Management

### [Name 1]
- Erstellt: X Issues
- Kommentiert: X Issues
- Quality: [Bewertung]
...

## Bewertung pro Studierendem

### [Name 1]
| Kategorie | Punkte | Max |
|----------|--------|-----|
| Commit-Aktivität | XX | 25 |
| Codequalität | XX | 25 |
| Issues erstellt | XX | 15 |
| Issue-Kommentare | XX | 20 |
| Issue-Qualität | XX | 15 |

**Gesamtpunkte: XX/100**

### [Name 2]
...

## Endbewertung

Zusammenfassung der Projektarbeit und Bewertung.
```

## Email and Database Rules

Always use `grading-shared` for:

- class-to-address-style mapping
- greeting and closing formulas
- gender fallback protocol
- database lookup using `/home/georg/OneDrive/uploadthing.db`
- email payload structure and paragraph preservation

## Constraints

- This skill must NOT be invoked from within a Git repository
- This skill must NOT clone student repositories; use `git pull` to update
- If uncommitted changes exist in any student repository, STOP IMMEDIATELY
- Do not commit changes or modify repository history
- All grading content must use second-person address (Sie or Du)
- Never use third-person references to the student
- In single-repo mode, never write shared `EMAIL.json`
- In bulk mode, generate shared `EMAIL.json` only after all per-repo outputs
  are complete
- Student identification comes from Git commit emails only
- Issue attribution prefers email over username for accuracy
- Grade all project contributors, not just code authors