# Current State (2026-03-21)

Project status snapshot. This file is overwritten on every save.

## Current Focus

Education-focused commands and skills for German class workflows, with repository grading consolidated into `repograde`.

## Completed (this cycle)

- [x] Fixed execution context terminology: local folder vs Git repository distinction
- [x] Added Execution Context section to `repograde` skill with explicit no-cloning rule
- [x] Added Pre-Grading Verification with `git pull` and `git status` checks
- [x] Added constraint: uncommitted changes = stop immediately
- [x] Fixed `Hausübungen.md` location clarification (CWD, not inside repo)
- [x] Added Execution Context section to `knowledge-assessment` skill
- [x] Clarified `vacuum.db` must exist at start, error if missing
- [x] Updated `repograde` and `knowledge-assess` commands with execution context warnings
- [x] Updated `grading-shared` skill with vacuum.db pre-existence requirement

## Pending

- [ ] Test revised grading workflow with real student repositories
- [ ] Consider adding utility scripts
- [ ] Validate skill loading from the linked `.config/OpenCode/Skills` environment

## Blockers

None

## Next Session Suggestion

Test the revised `repograde` workflow with a real student repository to verify execution context rules and second-person address work correctly.