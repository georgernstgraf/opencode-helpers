---
name: knowledge-exam
description: Generate German knowledge-check exams and solution files from class Git history
license: MIT
compatibility: opencode
metadata:
  category: education
  output: exam
---

# Knowledge Exam Skill

## Purpose

This skill creates a German knowledge-check exam for a specific class folder
based on recent Git history. Use it when asked to generate a mini-exam from the
material covered in class.

## Inputs

- `class`: target class folder name
- `weeks`: number of weeks of Git history to analyze

## Protocol

### 1. Validate Inputs

- Confirm that a folder matching `class` exists in the current working tree.
- If the folder does not exist, stop immediately and report that the class name
  appears to be invalid.
- Compute today's ISO date for the output filenames.
- The following classes are addressed informally in related communication:
  `2ahwii`, `3ahwii`, `5ahwii`, `4aaif`.
- All other classes use formal address in related communication.

### 2. Inspect Source Material

- Analyze Git commits from the last `weeks` weeks that changed files inside the
  class folder.
- Treat minimal commits as lecture anchors rather than complete coverage; infer
  the broader classroom context from the changed material in those commits.
- Review the changed files as needed to understand the topics that were likely
  taught.

### 3. Generate Exam Files

- Create `knowledge_<class>_<isodate>.md` inside the class folder.
- Include exactly 10 multiple-choice questions.
- Each multiple-choice question must have exactly 4 answer options.
- Each multiple-choice question is worth 4 points total.
- Score multiple-choice questions per option: award 1 point for each option that
  is handled correctly, whether it was correctly checked or correctly left
  blank.
- For every multiple-choice question, explicitly allow students to mark `-`
  and briefly explain why they consider the answer ambiguous or
  context-dependent.
- Include exactly 3 free-form questions.
- Each free-form question is worth 15 points.

### 4. Generate Solution File

- Create `knowledge_<class>_<isodate>_solutions.md` in the same folder.
- Keep the student-facing exam and the solution file separate.
- Do not include the solutions in the student-facing exam file.

### 5. Constraints

- Do not commit any generated files.
- Preserve existing files unless the task explicitly requires replacement.
- Follow the repository convention that `**/*_solutions.md` stays git-ignored.
- Write both generated Markdown files in German.
- UTF-8 is explicitly allowed and preferred in generated Markdown files.
- Do not replace German umlauts with transliterations such as `ae`, `oe`, or
  `ue` unless the surrounding source material explicitly requires that form.

## Output Expectations

- Student exam file in German with the required question counts and scoring.
- Separate teacher solution file in German.
- Filenames must include the class name and today's ISO date.
