# File Templates and Content Rules

Every knowledge file in `docs/ai/` is an OKF v0.2 **concept document**
(see [OKF-SPEC.md](./OKF-SPEC.md), §4): YAML frontmatter plus a markdown
body. `log.md` (§9) and `index.md` (§8) are reserved filenames and carry
no (or only `okf_version`) frontmatter.

## Frontmatter Envelope (required by this skill)

Every template below opens with this envelope; per-file types are given
in each section. The `type` attribute is the only OKF-required key,
but this skill mandates the full envelope when a file is (re)written:

```yaml
---
type: <Concept type>       # REQUIRED by OKF (see per-file types below)
title: <File title>        # human-readable display name
description: <one-line summary>
tags: [<tag>, ...]         # e.g. [ki-kustodiat, infrastructure]
generated: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
verified: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
status: stable             # draft | stable | deprecated
sources:                   # when a GitHub issue is the provenance
  - id: issue-<N>
    resource: <issue URL>
    title: <issue title, short>
---
```

Envelope rules:

- `generated`: update `generated.at` on EVERY persistence run that edits
  the file. `by` uses the OKF actor convention (OKF-SPEC.md §7).
- `verified`: set by this skill when the agent confirmed an entry against
  the current codebase (machine-confirmed trust tier). Upgrade to
  human-reviewed only by human append (`by: human:<id>`).
- `status`: `stable` unless the whole file is retired. The per-entry
  lifecycle convention (`[ACTIVE until #NNN]`, relocation to HISTORY.md)
  operates at entry level, not file level. Mark a whole file
  `status: deprecated` only when every entry in it is no longer active.
- `stale_after` (OKF-SPEC.md §5.5): optional; set it only for files with a
  known deadline (e.g. a STATE focus expected to change within a week).
- Legacy files without frontmatter are tolerated (OKF conformance is
  permissive, §11) but MUST be migrated the next time the skill touches
  them. Migration means: prepend the envelope, keep the body intact.
- Known content still in force after a superseded entry is removed keeps
  its existing frontmatter; only `generated.at` gets bumped.

## DECISIONS.md

Records ACTIVE architectural and technical decisions — one-time
choices still in force. Superseded decisions are relocated to
HISTORY.md. Each entry must have a date, a title, and a reason.

```markdown
---
type: Decisions
title: Decisions
description: Active architectural and technical decisions still in force.
tags: [knowledge, decisions]
generated: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
verified: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
---

# Decisions

Active architectural and technical decisions still in force.
Superseded decisions are relocated to HISTORY.md.

## YYYY-MM-DD: <Short Title>
- **Choice**: What was chosen
- **Reason**: Why this option was selected
- **Considered**: What alternatives were evaluated
- **Tradeoff**: Known downsides accepted
```

## CONVENTIONS.md

Records coding patterns, naming rules, file layout, and style
agreements that the agent must follow without re-discovering them.
Entries are terse, imperative, and grouped by topic.

```markdown
---
type: Conventions
title: Conventions
description: Coding patterns, naming rules, and style agreements to follow.
tags: [knowledge, conventions]
generated: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
verified: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
---

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

## PITFALLS.md

Records hard-won knowledge: things that failed, subtle bugs,
ordering issues, and non-obvious constraints. The purpose is to
prevent a new agent from repeating mistakes.

**What stays vs what moves to HISTORY.md:**
- Permanent non-obvious constraints (invariants, platform quirks,
  validation rules) → stays here.
- Bugs that were fixed, workarounds since removed, regressions
  since patched → moves to HISTORY.md once the fix ships.

```markdown
---
type: Pitfalls
title: Pitfalls
description: Hard-won knowledge about what does not work and non-obvious constraints.
tags: [knowledge, pitfalls]
generated: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
verified: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
---

# Pitfalls

Things that do not work, subtle bugs, and non-obvious constraints.
Read this file carefully before making changes in affected areas.

- <pitfall description, one line, actionable>
```

## HISTORY.md

Chronological archive of superseded decisions and entries pruned
from active files. This file is append-only; never delete entries.
Superseded entries are EXPECTED here — this is the full audit trail.

Note: HISTORY.md is NOT the OKF `log.md` (reserved filename, §9) — it
is an ordinary concept document that keeps the SUPERSEDED audit-trail
format below. The OKF `log.md` is the per-run persistence log described
in its own section further down.

```markdown
---
type: History Archive
title: History
description: Append-only archive of superseded decisions and pruned entries.
tags: [knowledge, history, audit]
generated: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
---

# History

Chronological archive of superseded decisions and pruned entries.
Entries here are no longer active truth. Never delete from this file.

## YYYY-MM-DD (SUPERSEDED YYYY-MM-DD, origin: <FILE>, reason: <why or #NNN>): <Title>
- <original entry text>
- **Origin**: <source file>
- **Reason**: <why it was superseded or pruned>
```

## DOMAIN.md

Records business logic, domain rules, and relationships that are
not obvious from the code alone. Only populate this file when the
project has meaningful domain logic.

```markdown
---
type: Domain Notes
title: Domain Knowledge
description: Business rules and domain relationships not obvious from code.
tags: [knowledge, domain]
generated: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
verified: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
---

# Domain Knowledge

Business rules and domain relationships not obvious from code.

## Entities
- <entity>: <short description and key constraints>

## Rules
- <business rule, one line>
```

## STATE.md

Records the current project status. This is the most volatile file.
It is overwritten (not appended) on every persistence run.

```markdown
---
type: State
title: Project State
description: Current project status as of the last persistence run.
tags: [knowledge, state]
generated: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
verified: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
---

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

## HANDOFF.md

Records open tasks for the next session. Overwritten on every
persistence run.

```markdown
---
type: Handoff
title: Handoff
description: Open tasks for the next agent session.
tags: [knowledge, handoff]
generated: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
verified: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
---

# Handoff

## Open Tasks
1. [ ] <task with file paths and issue references>

## Current Branch
<main>
```

## ARCHITECTURE.md

Living structural map of the system. Overwritten on every persistence
run when structural changes occurred. If nothing structural changed,
the file is left untouched (= frontmatter stays valid, only a body
change would require a `generated.at` bump).

```markdown
---
type: Architecture
title: Architecture
description: Living structural map of the system.
tags: [knowledge, architecture]
generated: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
verified: { by: opencode/knowledge-persistence, at: <ISO 8601 UTC datetime> }
---

# Architecture

Living structural map of the system as of YYYY-MM-DD.
Overwritten when structural changes occur during a session.

## Overview
<one-paragraph description of what this system is and how it is organized>

## Commands (`commands/`)
| Command | Purpose | Delegates to |
|---------|---------|-------------|
| `/name`  | <what it does> | `skills/<name>` or "none" |

## Skills (`skills/`)
| Skill | Purpose | Used by |
|-------|---------|---------|
| `name` | <what it does> | `/<command>` |

## Knowledge Files (`docs/ai/`)
| File | OKF type | Purpose | Update mode |
|------|----------|---------|------------|
| HANDOFF.md | Handoff | Open tasks for next session | Overwrite |
| DECISIONS.md | Decisions | Active decisions still in force | Append; prune superseded → HISTORY.md |
| ARCHITECTURE.md | Architecture | Living structural map | Overwrite |
| CONVENTIONS.md | Conventions | Ongoing rules to follow | Append |
| PITFALLS.md | Pitfalls | Hard-won failure knowledge | Append |
| DOMAIN.md | Domain Notes | Business/domain rules | Append |
| STATE.md | State | Current project status | Overwrite |
| HISTORY.md | History Archive | Superseded entries archive | Append-only |

## Data Flows
- <source> → <target>: <what flows and when>
```

## `docs/ai/log.md` (OKF reserved filename, §9)

Per-run persistence log, newest first, date-grouped. Appended at the
end of every persistence run. NO frontmatter (OKF §9 forbids it).

```markdown
# Persistence Log

## YYYY-MM-DD
* **Update**: Regenerated [STATE.md](STATE.md) and [HANDOFF.md](HANDOFF.md).
* **Update**: Added 1 entry to [PITFALLS.md](PITFALLS.md).
* **Deprecation**: Moved one superseded CONVENTIONS entry to [HISTORY.md](HISTORY.md).

## YYYY-MM-DD (earlier)
* ...
```

## `docs/ai/index.md` (OKF reserved filename, §8)

Progressive-disclosure entry point, regenerated by every persistence
run. No frontmatter except the bundle-root `okf_version` declaration.

```markdown
---
okf_version: "0.2"
---

# Knowledge Bundle Index

Short pointers; open individual concept files for details. Files
without frontmatter are legacy-but-tolerated and migrate on next touch.

## Active Files
* [HANDOFF.md](HANDOFF.md) - Open tasks for the next session
* [STATE.md](STATE.md) - Current project status
* [CONVENTIONS.md](CONVENTIONS.md) - Ongoing rules to follow
* [DECISIONS.md](DECISIONS.md) - Active decisions still in force
* [ARCHITECTURE.md](ARCHITECTURE.md) - Living structural map
* [PITFALLS.md](PITFALLS.md) - Hard-won failure knowledge
* [DOMAIN.md](DOMAIN.md) - Business/domain rules

## Reference
* [HISTORY.md](HISTORY.md) - Superseded-entries archive (append-only)
* [log.md](log.md) - Per-run persistence log
```

## AGENTS.md Bootstrap Block

Ensure this block exists in the project's `AGENTS.md`. If `AGENTS.md`
does not exist, create it with this content. If it exists, append this
block only if it is not already present.

```markdown
## Knowledge Bootstrap
Before starting any task, read the knowledge entry point first:
0. `docs/ai/index.md` (OKF index; if missing, fall back to the file
   list below) ← **start here**

Then, in order (skip files the index says are absent):
1. `docs/ai/HANDOFF.md` ← **read first, act on it**
2. `docs/ai/CONVENTIONS.md`
3. `docs/ai/DECISIONS.md`
4. `docs/ai/ARCHITECTURE.md`
5. `docs/ai/PITFALLS.md`
6. `docs/ai/STATE.md`
7. `docs/ai/DOMAIN.md` (if task involves business logic)
8. `docs/ai/HISTORY.md` (reference only — read last, as needed)

Knowledge files follow the Open Knowledge Format v0.2 (see
`skills/knowledge-persistence/OKF-SPEC.md` in opencode-helpers when
editing): each has YAML frontmatter with `type` and trust fields.
Legacy files without frontmatter are tolerated but migrate on next
persistence run.

If `HANDOFF.md` contains open tasks, complete them before starting
any new work unless the user explicitly says otherwise.
```
