---
description: Analyze commands and skills for inconsistencies and redundancies
---
Analyze this repository's commands and skills for quality issues.

Read every file in `commands/` and `skills/*/SKILL.md`, then produce a
structured report with the following sections. Display findings directly
to the user — do NOT edit any files.

## Analysis Checklist

### 1. Inconsistencies

Look for contradictory instructions across files:
- Parameter lists that differ between a command and its corresponding skill
- Numeric constants that disagree across files (concurrency limits, timeouts,
  scoring values)
- Behavioral rules that conflict between files
- Execution context requirements that contradict (e.g., "must be inside a repo"
  vs "must NOT be inside a repo")
- Wrong command names in usage examples
- Duplicate heading numbers or misnumbered sections

### 2. Redundancies

Look for blocks of text that appear in multiple files with only minor wording
differences:
- Multi-paragraph protocols duplicated across skills (homework discovery,
  repository analysis, email rules, etc.)
- Constraint lists repeated verbatim or near-verbatim
- Example blocks duplicated across files
- Boilerplate "use skill X for Y" paragraphs with identical structure

For each redundancy, estimate the number of duplicated lines and suggest
which shared file could host the canonical version.

### 3. Stale References

Look for references to deleted or renamed artifacts:
- Skill names that no longer exist as directories under `skills/`
- Command filenames referenced in documentation but not present in `commands/`
- Issue numbers or decisions that reference removed files

### 4. Structural Issues

- Frontmatter missing required fields (`name`, `description`)
- Sections that promise content but are empty (e.g., headers with no body)
- Files that contradict the conventions documented in `docs/ai/CONVENTIONS.md`

## Output Format

Present findings grouped by category. For each finding, include:
- **File(s)** involved (with line numbers where applicable)
- **Description** of the issue
- **Suggested fix** (one sentence)

If no issues are found in a category, state that explicitly.
