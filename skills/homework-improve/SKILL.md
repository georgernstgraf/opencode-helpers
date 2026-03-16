---
name: homework-improve
description: Enrich German class homework files from class-folder Git history
license: MIT
compatibility: opencode
metadata:
  category: education
  output: homework
---

# Homework Improve Skill

## Purpose

This skill improves the homework documentation for a specific class folder by
analyzing recent Git history and turning terse assignment notes into a clearer,
student-facing `Hausübungen.md` file in German.

## Inputs

- `class`: target class folder name

## Protocol

### 1. Validate Inputs

- Confirm that a folder matching `class` exists in the current working tree.
- If the folder does not exist, stop immediately and report that the class name
  appears to be invalid.
- Use `Hausübungen.md` inside the class folder as the output file.
- Keep all generated Markdown in German.

### 2. Inspect Existing Homework File

- If `Hausübungen.md` already exists, read it first.
- Treat the existing file as the source of truth for what has already been
  covered.
- Make the workflow re-entrant: avoid recreating homework sections that are
  already documented.
- Preserve the ordering rule that the newest homework entry must appear at the
  top of the file.

### 3. Inspect Source Material

- Analyze Git commits that changed files inside the class folder.
- Use the commit history as a teaching timeline and infer the likely homework
  context from the touched files, especially `README.md` and related lesson
  material in the same class folder.
- When multiple commits belong to the same teaching unit or homework date,
  synthesize them into one coherent homework entry instead of repeating them.
- When an existing `Hausübungen.md` already contains older entries, it is not
  necessary to crawl further back than the most recent documented homework.

### 4. Generate or Update Homework File

- Create `Hausübungen.md` if it does not exist.
- Add or update homework sections using German Markdown headings such as:
  - `## Hausübung vom 16. März`
  - `### Thema: async / await zur Erleichterung bei Promise-Programmierung`
- Expand terse homework notes into explicit, student-friendly instructions.
- Reference the relevant topic, expected outcome, and any useful context from
  the corresponding class material.
- Keep the writing concise but clearer and more actionable than the source
  notes.
- Maintain newest-on-top ordering across the full file.

### 5. Constraints

- Do not commit any generated changes.
- Preserve existing homework entries unless they need a minimal consistency
  update for structure or ordering.
- Write natural German and prefer proper UTF-8 spelling, including umlauts.
- Do not fabricate precise dates or details when the Git history does not
  support them; in that case, use the best defensible phrasing based on the
  available repository evidence.

## Output Expectations

- A created or updated `Hausübungen.md` inside the target class folder.
- Homework entries written in German.
- Clearer, more explicit homework descriptions than those found in terse source
  notes.
- Re-entrant behavior that avoids duplicating already documented homework.
