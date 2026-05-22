# opencode-helpers

Reusable AI agent configuration templates for opencode projects.

## Framework Isolation (CRITICAL)

This agent operates with ZERO knowledge of the OpenClaw framework.

**Forbidden:**
- Creating SOUL.md, USER.md, IDENTITY.md, HEARTBEAT.md, TOOLS.md, BOOTSTRAP.md
- Referencing OpenClaw concepts (gh-issue workflow, HEARTBEAT, skills, hooks, etc.)
- Using OpenClaw-specific workflows or tools
- **Using OpenClaw bundled skills** (e.g., github, gh-issues, weather, etc.)

**Allowed:**
- Standard git/github operations (trunk-based development: always commit and push directly to main; no branches or PRs)
- AGENTS.md for project instructions
- docs/ai/ knowledge files
- **ONLY skills from workspace skills/ directory** (this repository's skills)
- Project-specific workflows only

## Project Identity

Template repository providing standardized commands, skills, and knowledge
persistence patterns for AI-assisted development workflows.

## Tech Stack

- Markdown for commands and skills
- Bash for utility scripts

## Knowledge Bootstrap

Before starting any task, read the following files in order:

1. `docs/ai/HANDOFF.md` ← **read first, act on it**
2. `docs/ai/CONVENTIONS.md`
3. `docs/ai/DECISIONS.md`
4. `docs/ai/ARCHITECTURE.md`
5. `docs/ai/PITFALLS.md`
6. `docs/ai/STATE.md`
7. `docs/ai/DOMAIN.md` (if task involves business logic)

If the user says "continue", "resume", or "finish where we left off":
read and act on HANDOFF.md immediately without asking clarifying questions. If `HANDOFF.md` contains open tasks, complete them before starting any new work unless the user explicitly says otherwise.

When the user asks to save context or invokes the knowledge-persist workflow, the intended
knowledge-persistence output is the `docs/ai/` knowledge set:

- `HANDOFF.md` for open tasks and next-session context
- `CONVENTIONS.md` for ongoing rules and working patterns
- `DECISIONS.md` for durable architectural or process choices and rationale
- `ARCHITECTURE.md` for the living structural map of the current system
- `PITFALLS.md` for non-obvious failures, gotchas, and ordering constraints
- `DOMAIN.md` for business or teaching-domain rules when relevant
- `STATE.md` for the current focus, completed work, pending work, and blockers

Treat this as the contract for the future knowledge-persistence implementation,
even if the surrounding automation is still being refined.

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

## Repository

- GitHub: `georgernstgraf/opencode-helpers`
- Issue tracker: GitHub Issues

## Key Contacts

- Owner: Georg Graf <grafg@spengergasse.at>

## Development Environment

- Markdown for skills and commands
- ev. JSON configs
