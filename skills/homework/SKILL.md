---
name: homework
description: Generate per-lesson homework files from recent class Git history and teaching material
license: MIT
compatibility: opencode
metadata:
  category: education
  output: homework-file
---

# Homework Skill

## Purpose

This skill generates a per-lesson `Hausübung.md` homework file inside the
current lesson directory of a class folder. The user invokes it from inside the
class folder (e.g., `~/gitm/2ahwii/`) at the end of a lesson. No arguments
are needed.

## Invocation Context

- The user sits inside a class folder that is part of a Git repository.
- The class folder contains lesson directories named `<ISO-date>_<topic>`
  (e.g., `2026-03-21_promises`, `2026-04-01_async-await`).
- The skill auto-detects the current lesson directory from recent Git activity.
- No slash command is required. The user tells the agent to "generate homework"
  or similar, and the agent loads this skill directly.

## Protocol

### 1. Discover Current Lesson Directory

- Run `git log --since="24 hours ago" --name-only --diff-filter=A` and
  `git diff --name-only` to find recently created or modified directories.
- Look for directories matching the pattern `<YYYY-MM-DD>_<topic>`.
- Select the most recently created or modified matching directory.
- If no matching directory is found, check for uncommitted directories with
  the same pattern.
- If multiple candidates exist or none is found, list the candidates and ask
  the user which lesson directory to target.

### 2. Discover Sources

- Read all files inside the identified lesson directory: `README.md`, code
  examples, exercise sheets, and any other content files.
- Scan all source files for web URLs. Fetch and read each URL to extract
  relevant topic content.
- Include uncommitted changes — the teacher may have just created or edited
  files during class.
- Also check for files in the class folder root (e.g., a shared `README.md`)
  if they provide context for the lesson topic.
- Look for typical file patterns: `README.md`, `*.md`, `*.js`, `*.java`,
  `*.html`, `*.css`, `*.sql`, and any files with "übung" or "aufgabe" in
  the name.

### 3. State Plan

Before writing, display the following to the user:

- **Lesson directory**: the path identified (e.g., `2026-03-21_promises/`)
- **Sources found**: list of files read, commits analyzed, and URLs fetched
- **Topics deduced**: the teaching topics logically inferred from the sources,
  with a brief explanation of how each topic was derived
- **Target file**: the full path of the `Hausübung.md` to be created or updated

Then proceed immediately without waiting for confirmation.

### 4. Generate or Update Homework File

- Create `<lesson-dir>/Hausübung.md` if it does not exist.
- If it already exists, read it and enrich rather than overwriting.
- Write 2-4 focused, practical exercises that reinforce the key concepts
  covered in the lesson.
- Each exercise should be specific enough that a student can complete it
  independently, referencing the lesson material where appropriate.
- Format as clean Markdown with a topic heading and numbered exercises.
- Write in natural German with proper UTF-8 umlauts.

### 5. Confirm

- Show the user what was created or updated.
- Report the file path and the number of exercises added or changed.

## Homework Evidence

Only create homework entries when repository evidence supports that an
assignment is appropriate. Concrete examples of valid evidence:

- The lesson README or notes mention "Hausübung", "Übung", "Aufgaben", or
  "homework"
- Exercise files with starter code, TODO comments, or incomplete
  implementations were created during the lesson
- The teacher's notes or commit messages reference an assignment
- The lesson material covers a topic with clear practice exercises that
  naturally follow from what was taught

If the source material reveals the lesson topic but nothing suggests an
assignment was intended, omit the homework entry and report this to the user.

## Constraints

- Never create, update, or reference `Hausübungen.md` (plural/cumulative).
  This skill only produces per-lesson `Hausübung.md` files.
- Never commit generated changes. Leave files on disk for the user to review.
- Preserve existing homework entries when enriching an existing file.
- Write natural German. Do not replace umlauts with transliterations (`ae`,
  `oe`, `ue`) unless the source material explicitly requires that form.
- Group commits from the same teaching session into one homework entry.
- Do not fabricate dates, details, or exercises not supported by the source
  material.

## Output Expectations

- A created or updated `Hausübung.md` inside the target lesson directory.
- 2-4 exercises written in German.
- A plan summary displayed to the user showing sources, deduced topics, and
  target file.
- Confirmation of what was written.
