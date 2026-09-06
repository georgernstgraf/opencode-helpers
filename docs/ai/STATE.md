# Project State

Current status as of 2026-09-06 (evening).

## Current Focus

`unterricht` skill: first real cross-repo run (GRG-PMM) completed and its
learnings persisted back into the skill. Skill registered in README and
committed as first version.

## Completed (this cycle)

- [x] `unterricht` skill created (`skills/unterricht/SKILL.md`) and
      first-run-hardened during a live session on GRG-PMM:
      - Task A now carries a **Konformitäts-Check** (checklist answering
        "is the repo fully set up, does the skill still need to run?")
      - Gegenstand is read from repo docs, no hardcoded expansions
      - Task B fetch chain replaced: NOR-Kopf one-line amendment check
        instead of `GeltendeFassung.wxe` (>5 MB, webfetch fails)
      - New section **"RIS-Praxiswissen"** with subject-independent RIS
        patterns (ELI pages, BgblAuth PDFs, pdftotext+rg, Novelle §-numbering,
        Inkrafttreten pattern, PDF naming, evidence line for METADATA.md)
        plus a persist-back rule for future generic findings
- [x] README.md: `unterricht` registered in skill tables + trigger phrases
- [x] ARCHITECTURE.md: `unterricht` added to skills table
- [x] `~/AGENTS.md`: new section "OpenCode Skills & Agents-Files" — skills
      are symlinked (`~/.config/opencode/skills` → opencode-helpers/skills),
      walk the chain before edits, commit skills in this repo, generic
      knowledge persists into skills not project docs

## Pending

- [ ] dell (offline) replication — see HANDOFF.md

## Blockers

None

## Next Session Suggestion

None — skill updated, committed, and live via symlink.
