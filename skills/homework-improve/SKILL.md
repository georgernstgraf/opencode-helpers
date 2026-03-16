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
- Use the commit history as a teaching timeline, but do not treat commits as
  mere file-change events.
- Read the relevant changed material, especially `README.md` and related lesson
  files in the same class folder, until you understand what topic was being
  taught, which concepts were being practiced, and what a possible homework
  assignment would reinforce if one was actually given.
- Distinguish carefully between classroom content and actual homework.
- Do not assume that every lesson resulted in homework; some commits may only
  document in-class work or teaching material.
- Only create a homework entry when the repository evidence shows or strongly
  implies that an assignment was given.
- When multiple commits belong to the same teaching unit or homework date,
  synthesize them into one coherent homework entry instead of repeating them.
- When an existing `Hausübungen.md` already contains older entries, it is not
  necessary to crawl further back than the most recent documented homework.

### 4. Generate or Update Homework File

- Create `Hausübungen.md` if it does not exist.
- Add or update homework sections using German Markdown headings such as:
  - `## Hausübung vom 16. März`
  - `### Thema: async / await zur Erleichterung bei Promise-Programmierung`
- Base each homework entry on actual understanding of the topic and assignment,
  not on superficial paraphrasing of commit messages.
- Expand terse homework notes into explicit, student-friendly instructions.
- Reference the relevant topic, expected outcome, and any useful context from
  the corresponding class material.
- If the material clarifies the lesson topic but does not support that a real
  assignment was agreed, do not invent tasks or create a homework entry from
  that lesson alone.
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
- Do not invent homework assignments that are not supported by repository
  evidence.
- If the available material is enough to understand the lesson topic but not
  enough to prove that homework was actually assigned, prefer omission over
  speculation.

## Output Expectations

- A created or updated `Hausübungen.md` inside the target class folder.
- Homework entries written in German.
- Clearer, more explicit homework descriptions than those found in terse source
  notes.
- Re-entrant behavior that avoids duplicating already documented homework.
