# opencode-helpers

Reusable AI agent configuration templates for opencode projects.

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
4. `docs/ai/PITFALLS.md`
5. `docs/ai/STATE.md`
6. `docs/ai/DOMAIN.md` (if task involves business logic)

If the user says "continue", "resume", or "finish where we left off":
read and act on HANDOFF.md immediately without asking clarifying questions. If `HANDOFF.md` contains open tasks, complete them before starting any new work unless the user explicitly says otherwise.

When the user asks to save context or invokes the knowledge-persist workflow, the intended
knowledge-persistence output is the `docs/ai/` knowledge set:

- `HANDOFF.md` for open tasks and next-session context
- `CONVENTIONS.md` for ongoing rules and working patterns
- `DECISIONS.md` for durable architectural or process choices and rationale
- `PITFALLS.md` for non-obvious failures, gotchas, and ordering constraints
- `DOMAIN.md` for business or teaching-domain rules when relevant
- `STATE.md` for the current focus, completed work, pending work, and blockers

Treat this as the contract for the future knowledge-persistence implementation,
even if the surrounding automation is still being refined.

## Repository

- GitHub: `georgernstgraf/opencode-helpers`
- Issue tracker: GitHub Issues

## Key Contacts

- Owner: Georg Graf <grafg@spengergasse.at>

## Development Environment

- Markdown for skills and commands
- ev. JSON configs
