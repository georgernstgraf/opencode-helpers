# Current State (2026-03-07)

Project status snapshot. This file is overwritten on every save.

## Current Focus

Template repository with refined knowledge exam and assessment workflows, updated scoring model, and improved feedback tone.

## Completed (this cycle)

- [x] Fixed AGENTS.md header (was incorrectly referencing "AI Transcribe")
- [x] Fixed knowledge-persistence skill paths (`.opencode/knowledge/` → `_agents/`)
- [x] Added .gitignore for `*_solutions.md` files
- [x] Wrote comprehensive README.md
- [x] Updated _agents/ templates with meaningful content
- [x] Refactored knowledge exam and assessment workflows into thin commands plus dedicated skills
- [x] Standardized command wording and skill documentation structure
- [x] Added class-based German salutation rules and fallback guidance to the knowledge-assessment skill
- [x] Documented the intended `/save` knowledge-persistence outputs in `AGENTS.md` and `README.md`
- [x] Added OpenCode YAML frontmatter metadata to all existing skills
- [x] Updated scoring model to 10 MC questions (4 points each) and 3 free-text questions (15 points each)
- [x] Removed Austrian school grading references, replaced with point-based scoring
- [x] Refined assessment tone to be warm, respectful, and encouraging
- [x] Updated sign-off formulas for formal and informal contexts
- [x] Added requirement for structured, detailed individual feedback with clear paragraph spacing
- [x] Added note in email bodies about solutions file uploaded to Git repository

## Pending

- [ ] Add more example commands as needs arise
- [ ] Consider adding utility scripts
- [ ] Validate skill loading from the linked `.config/OpenCode/Skills` environment

## Blockers

None

## Next Session Suggestion

Validate linked skill discovery in OpenCode and continue refining teaching workflow automation as needed.
