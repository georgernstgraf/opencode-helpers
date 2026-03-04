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

## Repository

- GitHub: `georgernstgraf/opencode-helpers`
- Issue tracker: GitHub Issues

## Key Contacts

- Owner: Georg Graf <grafg@spengergasse.at>

## Development Environment

- Markdown for skills and commands
- ev. JSON configs
