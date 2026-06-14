# <PROJECT_NAME>

<!--
  Template for new opencode projects.
  How to use:
    1. Copy this file as AGENTS.md into your project root
    2. Fill in placeholders (<PROJECT_NAME>, <OWNER>, etc.)
    3. Symlink or copy opencode-helpers skills & commands:
       ln -s /path/to/opencode-helpers/skills skills
       ln -s /path/to/opencode-helpers/commands commands
       ln -s /path/to/opencode-helpers/docs/ai docs/ai
    4. In opencode, run: /init
    5. The agent reads this file and sets up the rest.

  A full opencode-helpers checkout is at:
  https://github.com/georgernstgraf/opencode-helpers
-->

## Project Identity

<PROJECT_NAME> provides <BRIEF_DESCRIPTION>.

## Knowledge Bootstrap

Before starting any task, read the following files in order:

1. `docs/ai/HANDOFF.md` ← **read first, act on it**
2. `docs/ai/CONVENTIONS.md`
3. `docs/ai/DECISIONS.md`
4. `docs/ai/ARCHITECTURE.md`
5. `docs/ai/PITFALLS.md`
6. `docs/ai/STATE.md`
7. `docs/ai/DOMAIN.md` (if task involves business logic)

If `HANDOFF.md` contains open tasks, complete them before starting
any new work unless the user explicitly says otherwise.

## Skill Triggers

The following skills have NO slash commands. Invoke them by natural language:

**Knowledge Persistence** — when the user says:
  "remember", "merke dir", "don't forget", "behalte das im Kopf",
  "merk dir das", "save context", "persist knowledge"
  → load and execute the `knowledge-persistence` skill

**Issue Workflow** — when the user says:
  - start: "issue start", "start issue", "begin issue", "neues issue",
           "ich arbeite an"
  - commit: "issue commit", "commit issue", "speichere issue", "checkpoint"
  - finish: "issue commit and push", "finish issue", "issue done",
            "issue fertig", "schließe issue"
  → parse intent (start/commit/finish) and load the `issue-workflow` skill
    with the corresponding mode.

## Tech Stack

- <TECHNOLOGY>
- <TECHNOLOGY>

## Repository

- GitHub: <OWNER>/<PROJECT_NAME>
- Issue tracker: GitHub Issues

## Key Contacts

- Owner: <NAME> <<EMAIL>>

## gh CLI Conventions

- Always use `gh issue view <N> --json title,body,comments` — never bare `gh issue view`. The bare form triggers a deprecation warning and may break in future `gh` versions.
- Prefer `--json` with explicit field selection for all `gh` read commands to avoid deprecation warnings and reduce output noise.

## Development Environment

- <DETAILS>
