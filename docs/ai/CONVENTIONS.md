# Coding Conventions

Coding patterns, naming rules, and style agreements for this project.
Follow these without question. Do not deviate unless explicitly told.

## Architecture

<!-- e.g., "Use layered architecture: presentation → service → repository" -->

## File Layout

<!-- e.g., "One class per file, file name matches class name" -->

- Keep slash commands short; use them as entrypoints, not long procedures.
- Move reusable multi-step workflows into `skills/<name>/SKILL.md`.
- Prefer thin commands that pass arguments and constraints into a skill.
- Every `skills/<name>/SKILL.md` must start with OpenCode YAML frontmatter.
- Keep skill `name` values lowercase, hyphenated, and identical to the skill directory name.
- Keep issue-related commands as thin wrappers around the shared `issue-workflow` skill.
- Use class-folder content generation commands as thin wrappers around dedicated standalone skills.

## Grading Workflow

- `repograde` is the canonical repository-grading workflow; keep `/repograde` as a thin wrapper around `skills/repograde/SKILL.md`.
- Grading commands operate from a local folder (CWD), NOT from within a Git repository.
- `Hausübungen.md` must exist in the CWD before invoking grading commands; it is never inside a student repository.
- Student repositories must already exist locally; never clone them as part of grading.
- Before grading, use `git pull` to verify latest version and `git status` to check for uncommitted changes; if uncommitted changes exist, stop immediately.
- In `/repograde`, treat a single argument as an explicit repository path and use it verbatim.
- Single-repo and bulk repository grading must both use `grading-shared` for address style, email formulas, database lookup, email JSON structure, and second-person address rules.
- All grading content must use second-person address (Sie or Du based on class); never use third-person to refer to the student.
- In `repograde`, derive output filenames from the repository basename; single-repo and bulk per-repo outputs are `<basename>_grading.md` and `<basename>_email.json`.
- `repograde` must never write `INDIVIDUAL.md` or `CLASS.md`.
- Shared `EMAIL.json` is created only by the bulk-mode master workflow after all per-repo outputs are finished.
- In bulk repository grading, use dynamic concurrency with default 4 concurrent runs and an approximately 3-second delay before starting the next run.
- All grading reports written in German with 0-100 score (Endbewertung)
- EMAIL.json contains full grading reports as email body (long emails expected)
- Formal/informal address and email formulas: see `grading-shared` skill for centralized configuration
- `vacuum.db` must exist at start of `knowledge-assessment`; if missing, stop immediately (do not create or copy)

## Naming

<!-- e.g., "Use camelCase for variables, PascalCase for types" -->

## API Integration

<!-- e.g., "All API calls go through api/ module, never directly from UI" -->

## Logging

<!-- e.g., "Use structured logging with correlation IDs" -->

## Build & Deploy

<!-- e.g., "Run tests before every commit, use semantic versioning" -->
