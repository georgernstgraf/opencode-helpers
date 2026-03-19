# Current State (2026-03-19)

Project status snapshot. This file is overwritten on every save.

## Current Focus

Education-focused commands and skills for German class workflows, with repository grading consolidated into `repograde`.

## Completed (this cycle)

- [x] Added `/homework` command (read-only homework suggestion generator)
- [x] Added `homework` skill for 24-hour commit analysis with 2-4 exercise suggestions
- [x] Skill outputs directly to user (no file modifications)
- [x] Created `skills/grading-shared/SKILL.md` with centralized configuration
- [x] Updated `knowledge-assessment` skill to reference shared config
- [x] Updated `repograde` command to reference shared config
- [x] Refactored `repograde` into a thin command plus dedicated `repograde` skill
- [x] Absorbed `repo-report` into `repograde`
- [x] Removed the obsolete `repograder` agent path
- [x] Updated issue #22 title/body and progress notes to reflect explicit single-repo path behavior and mandatory `grading-shared` usage in both modes
- [x] Switched `repograde` outputs to basename-derived artifact files instead of `INDIVIDUAL.md` / `CLASS.md`
- [x] Defined bulk mode so subagents write only per-repo artifacts and the master workflow creates shared `EMAIL.json` afterward
- [x] Updated `docs/ai/DOMAIN.md` with Central Configuration section
- [x] Updated `docs/ai/CONVENTIONS.md` to reference shared skill
- [x] Eliminated duplicated class lists and email formulas across grading workflows
- [x] Replaced batched execution with dynamic concurrency (4 concurrent, ~3s delay) in repograde

## Pending

- [ ] Add more example commands as needs arise
- [ ] Consider adding utility scripts
- [ ] Validate skill loading from the linked `.config/OpenCode/Skills` environment
- [ ] Test `repograde` single-repo and bulk workflows with real student repositories

## Blockers

None

## Next Session Suggestion

Test the `repograde` workflow with a real student repository in single-repo mode, then verify bulk mode against a folder of repositories.
