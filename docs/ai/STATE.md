# Project State

Current status as of 2026-09-10.

## Current Focus

Global agents are now repo-managed: new top-level `agents/` directory as
single global agent source, linked via `~/.config/opencode/agents`
(mirror of the skills symlink pattern). First agent: `lehrplan-annotator`
(ported from WI-Fachgruppe-Informatik; repo-local copy removed there).

## Completed (this cycle)

- [x] `agents/lehrplan-annotator.md` created (subagent, `opencode-go/glm-5.3`
      non-flash — explanation authoring needs the strongest language model);
      improved repo-agnostic prompt based on the Fachgruppe original
- [x] Symlink `~/.config/opencode/agents` → `agents/` set
- [x] AGENTS.md: new "Agent Source Rule" (flat `<name>.md`, one .md per
      agent — loader glob `{agent,agents}/**/*.md` makes every .md an agent)
- [x] ARCHITECTURE.md: agents section added, "no agents/ dir" statement removed
- [x] DECISIONS.md / PITFALLS.md: agent-source decision + symlink chain documented
- [x] WI-Fachgruppe-Informatik: `.opencode/agent/lehrplan-annotator.md` removed,
      knowledge files re-pointed to global source

## Pending

- [ ] dell (offline) replication — see HANDOFF.md (also replicate the new
      `agents/` directory + symlink there)

## Blockers

None
