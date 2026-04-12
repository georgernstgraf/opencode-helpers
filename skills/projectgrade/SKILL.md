---
name: projectgrade
description: Grade student project repositories based on Git commits, GitHub Issues, and Pull Requests
license: MIT
compatibility: opencode
metadata:
  category: education
  scope: execution
---

# Projectgrade Skill

## Purpose

This skill grades student Git repositories for collaborative project work where
students contribute via branches, Pull Requests, and GitHub Issues. It evaluates
code contributions (via Git commits), issue management (creation, editing,
commenting, quality), pull request activity (creation, reviews, merging), and
further measurable contributions (wiki, CI/CD, testing, documentation, project
management).

Unlike `repograde`, this skill does NOT use homework assignments or `Hausübungen.md`.
Student identification is derived exclusively from Git commit email addresses,
then mapped to student names via the uploadthing database.

This skill relies on `grading-shared` for: address style, email formulas,
second-person address rules, database lookup, email JSON structure,
repository analysis protocol, and reporting protocol.

## Differences from repograde

- Invoked from INSIDE the project Git repository (not from a local folder)
- No `Hausübungen.md` required (project grading, not homework)
- Evaluates GitHub Issues participation and Pull Request activity
- Student identification from Git commit emails only
- Issue quality, PR reviews, and collaboration factor into grading
- Single project mode (no bulk grading)
- Holistic assessment approach (no rigid numeric weights)

## Execution Context

This skill is invoked directly as a skill (no standalone command). It MUST be
invoked from within the Git repository being evaluated. Calling this skill from
outside a Git repository is an error.

The skill grades a single collaborative project repository where multiple
students contribute via branches, Pull Requests, and GitHub Issues by:
1. Verifying we are inside a Git repository (error if not)
2. Using `git pull` to ensure the latest version is checked out
3. Inspecting the repository content and Git history for grading
4. Querying GitHub API for issue and PR metadata (creation, edits, comments, reviews, merges)
5. Detecting further measurable contributions (wiki, CI/CD, tests, docs, project management)
6. Mapping contributor email addresses to student names via uploadthing.db

## Input

- `--gh-token`: GitHub token for API access (optional, defaults to environment)

Behavior:

- This skill operates on the current Git repository (CWD must be a Git repo)
- No repository path argument is needed; we are already inside the project

## Protocol

1. Verify we are in a Git repository. If not, STOP IMMEDIATELY with error.
2. Run `git pull` to verify latest version is checked out.
3. Run `git status` to check for uncommitted changes. If found, stop immediately.
4. Derive the output stem from `basename "$(git rev-parse --show-toplevel)"` or
   the current directory name.
5. Extract all unique contributor email addresses from git commits.
6. Query the uploadthing database to map emails to student names.
7. Analyze repository contributions (see Repository Analysis section).
8. Analyze GitHub Issues participation (see Issue Analysis section).
9. Analyze Pull Request activity (see Pull Request Analysis section).
10. Detect further measurable contributions (see Further Contributions section).
11. Apply holistic grading philosophy (see Holistic Grading Philosophy section).
12. Generate `<basename>_grading.md` as the repository grading report.
13. Generate `<basename>_email.json` as a JSON array with student entries,
    following `grading-shared` structure.

## Repository Analysis

Inspect repository content directly from within the current Git repository.

### Pre-Grading Verification

Before inspecting repository content, verify repository state:

1. Verify we are inside a Git repository:
   ```bash
   git rev-parse --is-inside-work-tree
   ```
   If this returns `false` or errors, STOP IMMEDIATELY and report to user.
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

#### Deleted Branch Recovery

**IMPORTANT:** `git branch -a` only shows currently existing branches. Branches
used for Pull Requests are frequently deleted after merge. The grading MUST
account for contributions made on branches that no longer exist.

Recovery methods:

1. **Merge commit history**: Commits from deleted branches remain in the Git
   history and are fully attributable via `git log --all`. Commit attribution
   is unaffected by branch deletion.
   ```bash
   git log --all --merges --format='%H %P'  # show merge commits and parents
   ```
2. **GitHub PR API**: Pull Requests retain their source branch name and author
   even after the branch is deleted. Use:
   ```
   GET /repos/{owner}/{repo}/pulls?state=all
   ```
   Each PR record contains `head.ref` (source branch name), `user.login`
   (creator), and `merged_by.login` — all preserved regardless of branch
   deletion.
3. **GitHub commit association**: For any commit SHA, the GitHub API can reveal
   which PR introduced it:
   ```
   GET /repos/{owner}/{repo}/commits/{sha}/pulls
   ```

When attributing work to students, always cross-reference Git commits with PR
history to ensure no contributions from deleted branches are missed.

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

### Issue Quality Rubric

Evaluate issue quality based on:

- **Title clarity**: Descriptive, specific, actionable
- **Description completeness**: Steps to reproduce, expected vs actual behavior
- **Code examples**: Minimal reproducible examples provided
- **Screenshots/logs**: Supporting evidence for bug reports
- **Labels**: Appropriate categorization (bug, enhancement, question)
- **Response to feedback**: Updates based on maintainer comments

Quality Rating (1-5):
  5 = Exceptional: Complete, clear, with reproducible examples
  4 = Good: Well-described with most relevant details
  3 = Average: Adequate description but missing some context
  2 = Below Average: Vague, incomplete, or poorly structured
  1 = Poor: No clear description or incorrectly filed

## Pull Request Analysis

This skill evaluates Pull Request activity as a key collaboration indicator.

### PR Discovery

Use GitHub API to fetch all Pull Requests and their metadata:

```
GET /repos/{owner}/{repo}/pulls?state=all
GET /repos/{owner}/{repo}/pulls/{number}/reviews
GET /repos/{owner}/{repo}/pulls/{number}/comments
GET /repos/{owner}/{repo}/pulls/{number}/commits
```

### PR Attribution

Map PRs to students using the same email-to-username lookup as Issue Analysis.
PRs contain `user.login` (creator), `merged_by.login` (merger), and review
authors — all resolved to student emails via the GitHub username mapping.

### Per-student PR Metrics

For each contributing student, collect:

- **PRs created**: total count, broken down by state (open / merged / closed without merge)
- **PRs merged**: successfully integrated contributions
- **Reviews given**: count by type (approved / changes requested / commented)
- **PR comments**: inline code review comments on others' PRs
- **Review responsiveness**: time between review feedback and author's response
- **Commits per PR**: volume of work per PR (distinguish large features from typo fixes)

### PR Quality Rubric

Evaluate PR quality based on:

- **Description completeness**: Context, motivation, linked issues, screenshots for UI changes
- **Code review quality**: When reviewing others' PRs — constructive, specific, helpful suggestions
- **Responsiveness to feedback**: Timely and thorough responses to review comments on own PRs
- **Branch management**: Clean commit history, meaningful commit messages, appropriately scoped changes
- **Linked issues**: PRs that reference or close related issues

### Merge Status Evaluation

- **Merged PRs**: Successfully integrated — strong indicator of accepted contribution quality
- **Closed (not merged) PRs**: Investigate reason — may indicate learning process, rejected approaches,
  or superseded by other work. Do not automatically penalize; consider context.
- **Open PRs**: Pending review — note as work in progress

## Further Contributions

Beyond commits, issues, and PRs, detect and list additional measurable
contributions for each student. These are presented descriptively in the
grading report — not scored numerically.

### Detection Methods

| Contribution | Detection Method |
|---|---|
| **Wiki edits** | GitHub Wiki is a separate Git repo; check `GET /repos/{owner}/{repo}/contents/docs/` or wiki commit history |
| **GitHub Discussions** | GraphQL API: `Discussion` and `DiscussionComment` nodes |
| **Project board management** | `GET /repos/{owner}/{repo}/projects` + cards/columns (or v2 Projects via GraphQL) |
| **Milestone management** | `GET /repos/{owner}/{repo}/milestones` — creation and due-date setting |
| **Label taxonomy** | `GET /repos/{owner}/{repo}/labels` — custom labels created; also check issue label assignments |
| **Releases / tagging** | `GET /repos/{owner}/{repo}/releases` — release notes, version management |
| **CI/CD setup** | Commits touching `.github/workflows/`, `Makefile`, `Dockerfile`, `docker-compose.yml` |
| **Testing** | Commits touching test files (`*_test.*`, `*.spec.*`, `tests/`, `__tests__/`) — recognized separately from feature code |
| **Documentation** | Commits touching `*.md`, `docs/`, `README*` — separate from code contributions |
| **Merge conflict resolution** | Merge commits with multiple parents; inspect diff for manual resolution effort |
| **Dependency management** | Commits touching `package.json`, `Cargo.toml`, `requirements.txt`, `pom.xml`, etc. |
| **Configuration / tooling** | Commits touching `.editorconfig`, `.eslintrc*`, `.prettierrc*`, `tsconfig.json`, etc. |

### Attribution

All contributions detected via commits are automatically attributed via the
email-based student mapping. Contributions detected via GitHub API (wiki,
discussions, project boards) use the same username-to-email lookup as issues
and PRs.

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

## Holistic Grading Philosophy

This skill uses a holistic, descriptive assessment approach rather than rigid
numeric weights. The goal is to produce a transparent, comprehensive listing
of each student's contributions that supports intuitive evaluation and
individual discussion.

### Core Principles

1. **Comprehensive listing first**: For each student, list ALL factual
   contributions — commits, issues, PRs, reviews, wiki edits, CI/CD setup,
   tests, documentation, project management, and any other measurable work.
2. **Estimated time investment**: Intuitively estimate hours invested based on
   the volume and quality of contributions. This is a rough assessment, not
   a precise calculation.
3. **Different contribution styles are equally valued**: Some students contribute
   more through code, others through issues, reviews, documentation, or project
   management. All forms of meaningful contribution are recognized.
4. **Diligence rating**: Assess as `high`, `medium`, or `low` based on:
   - Regular commit frequency (not just bursts at deadlines)
   - Consistent involvement throughout the project duration
   - Quality of changes (substantive vs. superficial)
   - Proper branch management and PR workflow
   - Engagement in reviews and discussions
5. **Not fully objective — and that is acceptable**: This assessment cannot be
   100% objective. Transparency of listed contributions compensates. The
   grading report provides the factual basis for individual conversations.
6. **Individual discussion**: The report is designed to support one-on-one
   conversations with students. List contributions factually so that both
   teacher and student can discuss the assessment.

### Qualitative Aids

The following are used as qualitative reference points, NOT as numeric score inputs:

- **Substantive vs. superficial work** distinction (from per-commit inspection)
- **Issue Quality Rubric** (1-5 scale, used descriptively)
- **PR Quality Rubric** (used descriptively)
- **Commit message quality** (clear, descriptive messages vs. generic ones)
- **Contribution spread** (evenly distributed vs. clustered at deadlines)

## Outputs

- `<basename>_grading.md` in German
- `<basename>_email.json` as a JSON array following `grading-shared` rules

## Grading Report Structure

The `<basename>_grading.md` file should include:

```markdown
# Projekt-Bewertung: [Repository Name]

## Beteiligte Studierende

- [Name 1] (email1@example.com) — GitHub: @username1
- [Name 2] (email2@example.com) — GitHub: @username2
...

## Beiträge im Überblick

### [Name 1]

**Commits:**
- Anzahl: X (davon Y substanziell, Z oberflächlich)
- Zeitlicher Verlauf: [Analyse: regelmäßig / phasenhaft / Deadline-getrieben]
- Branches: [Liste der genutzten Branches, inkl. gelöschter]
- Codequalität: [Beschreibung]

**Pull Requests:**
- Erstellt: X (davon Y merged, Z closed, W open)
- Reviews verfasst: X (davon Y approved, Z changes requested)
- PR-Kommentare: X
- Beschreibungsqualität: [Beschreibung]
- Review-Verhalten: [Beschreibung]

**Issues:**
- Erstellt: X (Qualität: [Bewertung])
- Kommentiert: X Issues
- Bearbeitet: X Issue-Beschreibungen

**Weitere Beiträge:**
- [z.B. CI/CD eingerichtet, X Tests geschrieben, Wiki bearbeitet, ...]
- [z.B. Dokumentation verfasst, Merge-Konflikte gelöst, ...]

**Geschätzter Zeitaufwand:** [hoch / mittel / niedrig]

**Qualitative Bewertung:**
- Arbeitsstil: [regelmäßig / phasenhaft / Deadline-getrieben]
- Beitragstyp: [kodeorientiert / kommunikativ / gemischt / organisatorisch]
- Sorgfalt: [hoch / mittel / niedrig]

**Gesamteinschätzung:** [Freitext — intuitive Zusammenfassung]

### [Name 2]
...

## Zusammenfassung

Kurze Gesamtbewertung der Projektarbeit, auffällige Beobachtungen,
Empfehlungen für das weitere Gespräch mit Studierenden.
```

## Email and Database Rules

Always use `grading-shared` for:

- class-to-address-style mapping
- greeting and closing formulas
- gender fallback protocol
- database lookup using `/home/georg/OneDrive/uploadthing.db`
- email payload structure and paragraph preservation

## Constraints

- This skill MUST be invoked from within a Git repository (the project being evaluated)
- If not inside a Git repository, STOP IMMEDIATELY with an error
- If uncommitted changes exist in the repository, STOP IMMEDIATELY
- Do not commit changes or modify repository history
- All grading content must use second-person address (Sie or Du)
- Never use third-person references to the student
- Student identification comes from Git commit emails only
- Issue and PR attribution prefers email over username for accuracy
- Grade all project contributors, not just code authors
- Account for contributions on branches that have since been deleted
- Pair programming and mentoring contributions are invisible to Git — the
  driver's commit is attributed, not the navigator. Note where such
  contributions are suspected but unmeasurable.
- Offline coordination (Slack, verbal discussion, external research) cannot
  be detected. The grading report should acknowledge this limitation.
