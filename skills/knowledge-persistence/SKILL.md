---
name: knowledge-persistence
description: Persist session context into the structured docs/ai knowledge files
license: MIT
compatibility: opencode
metadata:
  category: workflow
  scope: documentation
---

# Knowledge Persistence Skill

## Purpose

This skill extracts the agent's accumulated understanding from the current
session and persists it into a structured set of knowledge files on disk.
Use this skill at the end of a productive session, or when explicitly asked
to "save context", "persist knowledge", or "update knowledge file".

## Target Structure

Ensure the following directory and files exist relative to the project root.
Create any missing files. Never delete existing content unless it is
explicitly outdated or contradicted by newer information.

```text
docs/ai/
├── HANDOFF.md
├── DECISIONS.md
├── CONVENTIONS.md
├── PITFALLS.md
├── DOMAIN.md
└── STATE.md
```

## Protocol

### 1. Discovery

- Read all existing files in `docs/ai/` to understand what is
  already persisted.
- If the directory does not exist, create it.
- If a file does not exist, create it with the template provided below.

### 2. Diff Against Session

- Review the full conversation history of the current session.
- For each knowledge file, identify facts, decisions, patterns, or status
  changes that emerged during this session and are NOT yet in the file.
- Ignore transient chatter, failed attempts that were fully superseded,
  and speculative discussion that did not lead to a conclusion.

### 3. Write Updates

- Append new entries to the appropriate file.
- If an existing entry is now outdated, replace it in-place and prepend
  the date of the change.
- Never duplicate an entry that already exists.
- Write only facts. One item per bullet. No preamble, no commentary,
  no summaries at the top of the file.

### 4. Write `HANDOFF.md`

- Check the task list maintained during this session.
- If any tasks are still [PENDING] or [IN PROGRESS], write them to
  `docs/ai/HANDOFF.md` using the template below.
- Include: the current branch, each open task with file paths and
  line numbers where applicable, and any context the next agent
  needs to avoid re-discovery.
- If all tasks are complete, clear the file body and write only:
  `No pending tasks. Last cleared: YYYY-MM-DD.`

#### Escalation Rule

- If an open task would require more than ~30 minutes of agent work,
  do NOT put it in HANDOFF.md alone.
- Create a GitHub issue: `gh issue create --title "<title>" --body "<body>"`
- In HANDOFF.md, reference only the issue number:
  `1. [ ] See #42 — Refactor enrollment module to cursor pagination`
- This keeps HANDOFF.md small and actionable while large work is
  properly tracked in GitHub.

### 5. Update `AGENTS.md`

- Ensure the project-level `AGENTS.md` (in project root or `.opencode/`)
  contains the bootstrap instruction block. If it does not, append it.

### 6. Confirmation

- After writing, list every file that was created or modified, and for each
  show the number of entries added, updated, or removed.

## File Templates and Content Rules

### DECISIONS.md

Records architectural and technical decisions with rationale.
Each entry must have a date, a title, and a reason.

```markdown
# Decisions

Architectural and technical decisions made in this project.
Each entry documents WHAT was decided and WHY.

## YYYY-MM-DD: <Short Title>
- **Choice**: What was chosen
- **Reason**: Why this option was selected
- **Considered**: What alternatives were evaluated
- **Tradeoff**: Known downsides accepted
```

### CONVENTIONS.md

Records coding patterns, naming rules, file layout, and style
agreements that the agent must follow without re-discovering them.
Entries are terse, imperative, and grouped by topic.

```markdown
# Conventions

Coding patterns, naming rules, and style agreements for this project.
Follow these without question. Do not deviate unless explicitly told.

## Naming
- <rule>

## File Layout
- <rule>

## API Patterns
- <rule>

## Database
- <rule>

## Testing
- <rule>
```

### PITFALLS.md

Records hard-won knowledge: things that failed, subtle bugs,
ordering issues, and non-obvious constraints. The purpose is to
prevent a new agent from repeating mistakes.

```markdown
# Pitfalls

Things that do not work, subtle bugs, and non-obvious constraints.
Read this file carefully before making changes in affected areas.

- <pitfall description, one line, actionable>
```

### DOMAIN.md

Records business logic, domain rules, and relationships that are
not obvious from the code alone. Only populate this file when the
project has meaningful domain logic.

```markdown
# Domain Knowledge

Business rules and domain relationships not obvious from code.

## Entities
- <entity>: <short description and key constraints>

## Rules
- <business rule, one line>
```

### STATE.md

Records the current project status. This is the most volatile file.
It is overwritten (not appended) on every persistence run.

```markdown
# Project State

Current status as of YYYY-MM-DD.

## Current Focus
<one-liner describing the active workstream>

## Completed (this cycle)
- [x] <task>

## Pending
- [ ] <task>

## Blockers
- <blocker or "None">

## Next Session Suggestion
<what the next agent should start with>
```

## AGENTS.md Bootstrap Block

Ensure this block exists in the project's `AGENTS.md`. If `AGENTS.md`
does not exist, create it with this content. If it exists, append this
block only if it is not already present.

```markdown
## Knowledge Bootstrap
Before starting any task, read the following files in order:
1. `docs/ai/HANDOFF.md` ← **read first, act on it**
2. `docs/ai/CONVENTIONS.md`
3. `docs/ai/DECISIONS.md`
4. `docs/ai/PITFALLS.md`
5. `docs/ai/STATE.md`
6. `docs/ai/DOMAIN.md` (if task involves business logic)

If `HANDOFF.md` contains open tasks, complete them before starting
any new work unless the user explicitly says otherwise.
```

## Constraints

- Write only verified facts from the session. Do not speculate.
- Keep entries atomic: one fact, one bullet.
- Respect existing content. Merge, do not overwrite (except STATE.md).
- If unsure whether something belongs in DECISIONS vs CONVENTIONS,
  apply this test: "Is this a one-time choice (DECISIONS) or an
  ongoing rule to follow (CONVENTIONS)?"
- Total content per file should stay under 200 lines. If a file
  grows beyond that, split it by topic into sub-files within the
  same directory (e.g., `CONVENTIONS-api.md`, `CONVENTIONS-db.md`).
