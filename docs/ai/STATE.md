# Project State

Current status as of 2026-09-12.

## Current Focus

`writing-for-agents` audit across the skill set (remove no-op content,
extract reference material, sharpen triggers). P1/P2/P3a are shipped;
P4 remains.

## Completed (this cycle)

- [x] P1 fixes: `orchestration` slimmed to a scope-gated policy (367→63
      lines), `telegram-send` skill removed, `projectgrade` follows the
      `grading-shared` missing-email protocol, `AGENTS.md` bootstrap list
      adds `HISTORY.md` (`c4cff84`)
- [x] P2 SSOT consolidation: shared German blocks reference `grading-shared`,
      address table removed from `projectgrade`, class list from
      `knowledge-exam`, point totals only in `knowledge-exam`, `searxng`
      duplicate API table removed (`dbc9bde`)
- [x] P3a progressive disclosure: 8 sibling reference files extracted
      (`grading-shared/EMAIL-EXAMPLES.md`,
      `knowledge-persistence/FILE-TEMPLATES.md`,
      `lehrplan/{KLASSEN-ZUORDNUNG,SPENGERGASSE-KLASSEN,RIS-PRAXIS,ERLAEUTERUNGS-QUALITAET}.md`,
      `repograde/REPORT-FORMAT.md`, `projectgrade/REPORT-FORMAT.md`);
      normative rules stayed inline; `tests/test_skill_links.py` link guard
      added (`070961a`)
- [x] Upstream-skill sync check: no content changes on the 6 transplanted
      skills
- [x] docs/ai updated this session: CONVENTIONS "Single Source of Truth" rule,
      ARCHITECTURE test + sibling references, DECISIONS P3a
- [x] Repo-managed `agents/` directory with `lehrplan-annotator`, symlinked
      via `~/.config/opencode/agents` (prior cycle; still current)

## Pending

- [ ] P4 of the audit: Completion Criteria ("Done when …") + frontmatter
      description trigger branches across `skills/*`
- [ ] dell replication: repo sync, `agents/` directory + `~/.config/opencode/agents`
      symlink (see HANDOFF.md task 2)

## Blockers

None

## Next Session Suggestion

Start with P4: for each skill, add a short "Done when" completion criterion and
split the frontmatter `description` into clear trigger branches, without
re-introducing moved reference material. Keep the link guard green
(`python3 -m unittest discover -s tests -v`).
