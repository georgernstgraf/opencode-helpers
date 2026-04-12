# Coding Conventions

Coding patterns, naming rules, and style agreements for this project.
Follow these without question. Do not deviate unless explicitly told.

## File Layout

<!-- e.g., "One class per file, file name matches class name" -->

- Keep slash commands short; use them as entrypoints, not long procedures.
- Move reusable multi-step workflows into `skills/<name>/SKILL.md`.
- Prefer thin commands that pass arguments and constraints into a skill.
- Every `skills/<name>/SKILL.md` must start with OpenCode YAML frontmatter.
- Keep skill `name` values lowercase, hyphenated, and identical to the skill directory name.
- Keep issue-related commands as thin wrappers around the shared `issue-workflow` skill.
- Use class-folder content generation commands as thin wrappers around dedicated standalone skills.
- Lesson directories inside class folders follow the naming pattern `<YYYY-MM-DD>_<topic>` (e.g., `2026-03-21_promises`).
- Homework is generated as per-lesson `Hausübung.md` (singular) files inside lesson directories, not as cumulative `Hausübungen.md`.

## Grading Workflow

- **All grading skills must output a percentage (0-100%) alongside the score.** This is mandatory for every skill that produces grading outputs.
- `repograde` is the canonical repository-grading skill; it handles both full-history and date-filtered grading. There is no separate command — invoke the skill directly.
- `projectgrade` is the project-grading skill; it runs from inside the project Git repo. There is no separate command — invoke the skill directly.
- Grading operates from a local folder (CWD), NOT from within a Git repository — except `projectgrade` which MUST run from inside a Git repo.
- `Hausübungen.md` (legacy, cumulative) or per-lesson `Hausübung.md` files in `<date>_<topic>` directories provide homework assignments for grading; at least one must exist in the CWD.
- Student repositories must already exist locally; never clone them as part of grading.
- Before grading, use `git pull` to verify latest version and `git status` to check for uncommitted changes; if uncommitted changes exist, stop immediately.
- Single-repo and bulk repository grading must both use `grading-shared` for address style, email formulas, database lookup, email JSON structure, and second-person address rules.
- All grading content must use second-person address (Sie or Du based on class); never use third-person to refer to the student.
- In `repograde`, derive output filenames from the repository basename; single-repo and bulk per-repo outputs are `<basename>_grading.md` and `<basename>_email.json`.
- `repograde` must never write `INDIVIDUAL.md` or `CLASS.md` (except date-filtered bulk mode which writes `CLASS.md`).
- `repograde` bulk mode must write `GRADINGS.md` (class-wide overview table).
- `repograde` date-filtered bulk mode must write `GRADINGS.md` and `CLASS.md`.
- `knowledge-assessment` must write per-student `<name>_grading.md` files instead of `INDIVIDUAL.md`.
- `knowledge-assessment` must always write `GRADINGS.md` and `CLASS.md` (both mandatory).
- Shared `EMAIL.json` is created only by the bulk-mode master workflow after all per-repo outputs are finished.
- In bulk repository grading, use dynamic concurrency with default 5 concurrent runs and an approximately 3-second delay before starting the next run.
- `grading-shared` contains shared protocols for: repository analysis, homework discovery, bulk grading concurrency, email/database rules, German/UTF-8 constraints, email body format, praise guidelines, and reporting. Grading skills reference these instead of duplicating.
- All grading reports written in German with 0-100 score (Endbewertung)
- EMAIL.json contains full grading reports as email body (long emails expected)
- Email bodies MUST be plain ASCII text. Only code blocks with backtick fences are allowed as Markdown. No headers, bold, tables, or lists in email bodies.
- Formal/informal address and email formulas: see `grading-shared` skill for centralized configuration
- `vacuum.db` must exist at start of `knowledge-assessment`; if missing, stop immediately (do not create or copy)
- If any student email address is missing from the database, stop immediately and present all unresolved names to the user; do not generate `EMAIL.json` until all emails are resolved

## Naming

<!-- e.g., "Use camelCase for variables, PascalCase for types" -->

## API Integration

<!-- e.g., "All API calls go through api/ module, never directly from UI" -->

## Logging

<!-- e.g., "Use structured logging with correlation IDs" -->

## Build & Deploy

<!-- e.g., "Run tests before every commit, use semantic versioning" -->
