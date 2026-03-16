# Current State (2026-03-16)

Project status snapshot. This file is overwritten on every save.

## Current Focus

Template repository with refined skill-backed workflows, issue lifecycle reuse, knowledge persistence integration, and a new homework-improvement workflow.

## Completed (this cycle)

- [x] Fixed AGENTS.md header (was incorrectly referencing "AI Transcribe")
- [x] Fixed knowledge-persistence skill paths (`.opencode/knowledge/` → `_agents/`)
- [x] Added .gitignore for `*_solutions.md` files
- [x] Wrote comprehensive README.md
- [x] Updated _agents/ templates with meaningful content
- [x] Refactored knowledge exam and assessment workflows into thin commands plus dedicated skills
- [x] Standardized command wording and skill documentation structure
- [x] Added class-based German salutation rules and fallback guidance to the knowledge-assessment skill
- [x] Documented the intended `/knowledge-persist` knowledge-persistence outputs in `AGENTS.md` and `README.md`
- [x] Added OpenCode YAML frontmatter metadata to all existing skills
- [x] Updated scoring model to 10 MC questions (4 points each) and 3 free-text questions (15 points each)
- [x] Removed Austrian school grading references, replaced with point-based scoring
- [x] Refined assessment tone to be warm, respectful, and encouraging
- [x] Updated sign-off formulas for formal and informal contexts
- [x] Added requirement for structured, detailed individual feedback with clear paragraph spacing
- [x] Added note in email bodies about solutions file uploaded to Git repository
- [x] Reviewed repeated content across teaching-related skills
- [x] Removed accidental duplicate parsing instructions from `skills/knowledge-assessment/SKILL.md`
- [x] Tightened `skills/knowledge-exam/SKILL.md` while keeping it fully standalone for skill loading
- [x] Tightened `skills/knowledge-assessment/SKILL.md` while keeping it fully standalone for skill loading
- [x] Avoided shared sidecar skill context because `skill` loading should not depend on adjacent helper files
- [x] Renamed `/save` to `/knowledge-persist`
- [x] Updated `/issue-finish` to include knowledge persistence
- [x] Refactored issue commands into thin wrappers around a new `issue-workflow` skill
- [x] Documented that issue-workflow commits must include a GitHub issue number
- [x] Added `/homework-improve` as a thin command wrapper for class homework enrichment
- [x] Added standalone `homework-improve` skill for re-entrant `Hausübungen.md` generation from class Git history
- [x] Confirmed the intended homework output filename is `Hausübungen.md`

## Pending

- [ ] Add more example commands as needs arise
- [ ] Consider adding utility scripts
- [ ] Validate skill loading from the linked `.config/OpenCode/Skills` environment
- [ ] Review non-teaching skills for safe wording cleanup without introducing cross-file dependencies
- [ ] Consider adding an explicit `/issue-comment` command if issue-only status updates become common

## Blockers

None

## Next Session Suggestion

Validate linked skill discovery in OpenCode and confirm the new `homework-improve` workflow is ergonomic in practice.
