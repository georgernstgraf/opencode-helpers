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

## Naming

<!-- e.g., "Use camelCase for variables, PascalCase for types" -->

## API Integration

<!-- e.g., "All API calls go through api/ module, never directly from UI" -->

## Logging

<!-- e.g., "Use structured logging with correlation IDs" -->

## Build & Deploy

<!-- e.g., "Run tests before every commit, use semantic versioning" -->
