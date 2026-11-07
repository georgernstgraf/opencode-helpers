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
The files follow the **Open Knowledge Format (OKF) v0.2** — the full
specification is vendored alongside this skill in
[OKF-SPEC.md](./OKF-SPEC.md).
Use this skill at any checkpoint during or at the end of a productive
session, or when explicitly asked to "save context", "persist knowledge",
or "update knowledge file".

Persisting to disk is **not** the end of the skill: **every persistence run
finishes with its own commit and push** (SVN: `svn ci`) of the updated
knowledge files, referencing the active issue. Knowledge that is written but
not committed does not exist for the next agent — the run is only complete
once the changes are on the trunk.

## Target Structure

Ensure the following directory and files exist relative to the project root.
Create any missing files. Never delete entries from HISTORY.md (it is
an append-only archive). Do delete superseded entries from active files
by relocating them to HISTORY.md.

`docs/ai/` is treated as an OKF **bundle**: every non-reserved `.md` file
is a concept document carrying a YAML frontmatter envelope with the
required `type` field plus the trust and lifecycle fields (see
[FILE-TEMPLATES.md](./FILE-TEMPLATES.md)). The reserved filenames
`index.md` and `log.md` carry no (or only `okf_version`) frontmatter.

```text
docs/ai/
├── index.md        (OKF §8: progressive-disclosure index, okf_version)
├── log.md          (OKF §9: per-run persistence log, date-grouped)
├── HANDOFF.md      type: Handoff
├── DECISIONS.md    type: Decisions
├── ARCHITECTURE.md type: Architecture
├── CONVENTIONS.md  type: Conventions
├── PITFALLS.md     type: Pitfalls
├── DOMAIN.md       type: Domain Notes
├── STATE.md        type: State
└── HISTORY.md      type: History Archive
```

Legacy files without frontmatter are tolerated (OKF conformance is
permissive, OKF-SPEC.md §11) but MUST receive the envelope the next time
the skill touches them — no big-bang migration is required.

**Active files** (must match current HEAD; no superseded entries):
HANDOFF.md, DECISIONS.md, ARCHITECTURE.md, CONVENTIONS.md, PITFALLS.md,
DOMAIN.md, STATE.md.

**Historical file** (chronological sink; superseded entries EXPECTED here):
HISTORY.md.

## Protocol

### 1. Discovery

- Start at `docs/ai/index.md` (OKF §8 progressive disclosure) if it
  exists; it lists what is present, including legacy files.
- Read all existing files in `docs/ai/` to understand what is
  already persisted. Files WITHOUT frontmatter are legacy-but-valid;
  any file you end up editing must first receive the OKF envelope
  (see [FILE-TEMPLATES.md](./FILE-TEMPLATES.md), "Frontmatter
  Envelope").
- If the directory does not exist, create it (with `index.md` and
  `log.md`).
- If a file does not exist, create it with the template in
  [FILE-TEMPLATES.md](./FILE-TEMPLATES.md).

### 2. Diff Against Session

- Review the full conversation history of the current session.
- For each knowledge file, identify facts, decisions, patterns, or status
  changes that emerged during this session and are NOT yet in the file.
- Ignore transient chatter, failed attempts that were fully superseded,
  and speculative discussion that did not lead to a conclusion.

### 3. Write Updates

- Append new entries to the appropriate file.
- If an existing entry is now outdated, MOVE it to HISTORY.md (do not
  leave superseded content in active files).
- Never duplicate an entry that already exists.
- Write only facts. One item per bullet. No preamble, no commentary,
  no summaries at the top of the file.

**Frontmatter maintenance (every touched file):**

- On any edit, update `generated.at` to the current run's ISO 8601
  UTC datetime (OKF §5.2).
- When you verified an entry against the current codebase/config
  before writing it, set `verified: { by: opencode/knowledge-persistence, at: <ISO> }`
  (machine-confirmed trust tier, OKF §5.3). Never fabricate a
  `human:` verification — only a human may add `by: human:<id>`.
- Set `sources` with the active GitHub issue when the entry
  references one (OKF §5.1); keep existing `sources` entries that
  remain relevant.
- Files are `status: stable` by default; per-entry lifecycle lives in
  the entry text (`[ACTIVE until #NNN]`, HISTORY relocation), not in
  the file-level `status` field.

### 3b. Prune Superseded Entries

For each active file being updated, scan for entries that no longer
match current reality:

- Entries contradicted by current code or configuration.
- Entries superseded by a later decision or implementation.
- Entries describing a reverted or removed change.

For each superseded entry found:

1. **Remove** it from the active file.
2. **Append** it to `HISTORY.md` with a header:
   `## YYYY-MM-DD (SUPERSEDED YYYY-MM-DD, origin: <FILE>, reason: <why or #NNN>): <Title>`
3. Include the original entry text below the header, plus one line
   noting the origin file and the reason it was superseded.
4. Leave a ONE-LINE pointer in the active file ONLY if a future reader
   would otherwise re-discover the same pitfall; otherwise delete
   cleanly.
5. Bump `generated.at` on the active file and on `HISTORY.md`.

**PITFALLS.md special case**: Distinguish between:
- **(a) Permanent non-obvious constraints** (e.g., "Room validates
  PRAGMA table_info, PK must be NOT NULL") — these stay in active
  PITFALLS.md.
- **(b) Bugs that were fixed** (e.g., "clearText+typeText race, fixed
  in #254") — these MOVE to HISTORY.md once the fix ships. Their value
  is historical, not advisory.

**Status-tag convention**: For active-file entries with a known
lifecycle (e.g., a workaround slated for removal), append an optional
trailing tag `[ACTIVE until #NNN]` so a future pruner knows to
relocate it.

### 4. Rewrite `ARCHITECTURE.md` (if structural changes occurred)

- Determine whether the session introduced any structural changes:
  new/removed/renamed commands, skills, knowledge files, or significant
  changes to data flows, dependencies, or component relationships.
- If no structural changes occurred, skip this step and leave
  `ARCHITECTURE.md` unchanged.
- If structural changes did occur, **overwrite** `docs/ai/ARCHITECTURE.md`
  with the current system snapshot using the template in
  [FILE-TEMPLATES.md](./FILE-TEMPLATES.md).
- Like STATE.md, this file is overwritten (not appended) because it
  represents a point-in-time structural map, not a chronological log.

### 5. Write `HANDOFF.md`

- Check the task list maintained during this session.
- If any tasks are still [PENDING] or [IN PROGRESS], write them to
  `docs/ai/HANDOFF.md` using the template in
  [FILE-TEMPLATES.md](./FILE-TEMPLATES.md).
- Include: the current branch, each open task with file paths and
  line numbers where applicable, and any context the next agent
  needs to avoid re-discovery.
- If all tasks are complete, clear the file body and write only:
  `No pending tasks. Last cleared: YYYY-MM-DD.`

#### Escalation Rule

- If an open task would require more than ~30 minutes of agent work,
  do NOT put it in HANDOFF.md alone.
- **GitHub-Projekte:** Create a GitHub issue:
  `gh issue create --title "<title>" --body "<body>"` — but only **after**
  the Duplicate Check from the `issue-workflow` skill reports no matching
  open issue (reuse that issue instead, and reference its number here). In
  HANDOFF.md, reference only the issue number:
  `1. [ ] See #42 — Refactor enrollment module to cursor pagination`
- **SVN-Projekte ohne Issue-System** (z. B. `~/svn/georg`, Deployed-Trees auf
  murl/claw): es existiert KEIN Issue-Tracking — solche Aufgaben bleiben
  vollständig in HANDOFF.md (mit Datei-/Pfad-Angabe); kein `gh`-Aufruf.
- This keeps HANDOFF.md small and actionable while large work is
  properly tracked (via issues in GitHub, via HANDOFF.md in SVN).

### 5b. Update `log.md` and regenerate `index.md`

- **`log.md`** (OKF §9): append one date-grouped entry at the top of
  the log (newest first) summarizing this run: for each updated file
  an `**Update**` / `**Creation**` / `**Deprecation**` line linking
  the concept. NO frontmatter in `log.md`.
- **`index.md`** (OKF §8): regenerate from the current directory
  state. Keep `okf_version: "0.2"` in the bundle-root frontmatter
  (the only frontmatter an `index.md` may carry). Entries include the
  concept's `description`. Skip files the run did not touch only to
  note them as unchanged — the index always lists ALL files.

### 6. Update `AGENTS.md`

- Ensure the project-level `AGENTS.md` (in project root or `.opencode/`)
  contains the bootstrap instruction block. If it does not, append it.

### 7. Comment on Active Issue (nur GitHub-Projekte; SVN: skip)

- **Anwendbarkeit:** nur für GitHub- (bzw. Git-)Projekte. In SVN-Projekten
  ohne Issue-System (`~/svn/georg` etc.) diesen Schritt still überspringen.
- If there is a known active GitHub issue for the current session, post a
  brief comment summarizing what knowledge was persisted (files updated,
  key additions). Example:
  `gh issue comment 42 --body "Knowledge persisted: added 3 entries to CONVENTIONS.md, updated STATE.md."`
- **NEVER close, reopen, or change the state of any issue.** This skill
  only adds comments for traceability.
- If no active issue is known, skip this step silently.

### 8. Commit and Push (mandatory)

- **Git-Projekte:** Stage the knowledge files and create a commit that
  references the active issue, e.g. `docs: persist knowledge (#42)`. Preserve
  the repository's commit-message style, keep the issue reference, then push to
  the trunk line. Never write an empty commit — if nothing changed, report
  "nothing to persist" and stop.
- If several commits are needed, that is fine; what is forbidden is leaving
  knowledge changes uncommitted or unpushed.
- **SVN-Projekte** (z. B. `~/svn/georg`, Deployed-Trees): Analogon ist ein
  `svn ci` mit klarer deutscher Commit-Message.
- The commit may land **after** an issue is closed (e.g. STATE.md/HANDOFF.md
  record the closed state) — the knowledge commit is the follow-up that carries
  those files to the trunk.
- This skill still NEVER closes, reopens, or changes the state of an issue
  (see step 7 and Constraints).

### 9. Confirmation

- After committing and pushing, list every file that was created or modified,
  and for each show the number of entries added, updated, or removed.
- Confirm the OKF state of `docs/ai/`: every concept file carries a
  parseable frontmatter with non-empty `type`; `index.md` was
  regenerated; `log.md` records this run (OKF-SPEC.md §11).
- State the commit hash and that it was pushed.

## File Templates and Content Rules

Templates and per-file content rules for `docs/ai/` are in
[FILE-TEMPLATES.md](./FILE-TEMPLATES.md). Use the template for a file when
creating or overwriting it.

## Constraints

- **Commit + push is part of persistence.** Every run ends on the trunk: a
  commit with the active issue reference, pushed (Git) or `svn ci` (SVN).
  Uncommitted/unpushed knowledge files violate this skill.
- Write only verified facts from the session. Do not speculate.
- Keep entries atomic: one fact, one bullet.
- Active files: merge new entries, but DELETE superseded entries by
  relocating them to HISTORY.md. Never leave stale content in active
  files.
- HISTORY.md: append-only. Never delete or modify existing entries.
- Overwrite files: STATE.md, ARCHITECTURE.md, and HANDOFF.md are
  overwritten on each persistence run (not appended).
- If unsure whether something belongs in DECISIONS vs CONVENTIONS,
  apply this test: "Is this a one-time choice (DECISIONS) or an
  ongoing rule to follow (CONVENTIONS)?"
- If unsure whether something belongs in DECISIONS vs ARCHITECTURE,
  apply this test: "Is this a chronological record of a choice
  (DECISIONS) or a structural description of the current system
  (ARCHITECTURE)?"
- If unsure whether an entry is still valid, apply this test:
  "Is this still true in the current codebase? If not, it belongs
  in HISTORY.md, not the active file."
- Active files stay lean through the prune protocol (step 3b); no
  hard line limit is needed.
- HISTORY.md is append-only and will grow over time. If it exceeds
  ~500 lines, archive entries older than 6 months into
  `HISTORY-archive.md` (also append-only, same header format).
- **Issue Safety**: This skill is a documentation-only operation. It
  must NEVER close, reopen, or change the state of any GitHub issue.
  Issue lifecycle management is the exclusive responsibility of the
  `issue-workflow` skill (continuous completion criteria or its `finish`
  override mode). When invoked standalone, this
  skill may only create new issues (Escalation Rule) or comment on
  existing ones. — gilt diesbezüglich nur für GitHub-Projekte;
  SVN-Projekte ohne Issue-System haben schlicht keine Issues (dann
  entfällt der ganze Mechanik still).
- **OKF Integrity**: `docs/ai/` is an OKF v0.2 bundle
  ([OKF-SPEC.md](./OKF-SPEC.md)). The reserved filenames `index.md`
  and `log.md` are never used for concept documents, `log.md` gets no
  frontmatter, and frontmatter `type` is always present and non-empty.
  Unknown extra frontmatter keys are allowed (producers may extend).
- **No fabricated trust**: never write a `human:<id>` `verified` entry
  on your own — machine-verified is the maximum an agent may claim.
