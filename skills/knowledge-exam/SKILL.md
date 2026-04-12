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

## Output Language: MANDATORY GERMAN

The generated exam and solution files MUST be written in natural German with 
proper UTF-8 umlauts (ä, ö, ü, ß). 
Never use English for the exam questions or solutions.

## Inputs

- `class`: target class folder name.
- `weeks`: number of weeks of Git history to analyze.
- `exam-date`: (mandatory) the planned exam date, must be either:
  - An ISO date (YYYY-MM-DD format).
  - The literal `today`.
  - The literal `tomorrow`.
- `mc-count`: (optional) number of multiple-choice questions, default 10.
- `free-count`: (optional) number of free-text questions, default 3.

## Protocol

### 1. Validate Inputs

- **Mandatory exam-date parameter**: If `exam-date` is not provided, abort
  immediately with an error message explaining that this parameter is required.
- Confirm that a folder matching `class` exists in the current working tree.
- If the folder does not exist, stop immediately and report that the class name
  appears to be invalid.
- **Resolve exam-date to ISO format**:
  - If `exam-date` is an ISO date (YYYY-MM-DD), use it as-is.
  - If `exam-date` is `today`, compute today's ISO date.
  - If `exam-date` is `tomorrow`, compute tomorrow's ISO date.
  - Store this resolved date as `<isodate>` for output filenames.
- The following classes are addressed informally in related communication:
  `2ahwii`, `3ahwii`, `5ahwii`, `4aaif`.
- All other classes use formal address in related communication.

### 2. Resolve Question Counts

- Default values: 10 multiple-choice questions, 3 free-text questions.
- If `mc-count` is not provided, set `mc-count = 10`.
- If `free-count` is not provided, set `free-count = 3`.
- If neither `mc-count` nor `free-count` was provided by the user:
  - Before generating, ask the user: "Sollen 10 MC-Fragen und 3 Freitext-Fragen generiert werden? (j/n)"
  - If the user confirms, proceed with defaults.
  - If the user declines, ask for specific counts before continuing.
- Do NOT ask for confirmation when at least one count was explicitly provided.

### 3. Inspect Source Material

- Analyze Git commits from the last `weeks` weeks that changed files inside the
  class folder.
- Treat minimal commits as lecture anchors rather than complete coverage; infer
  the broader classroom context from the changed material in those commits.
- Review the changed files as needed to understand the topics that were likely
  taught.

### 4. Generate Exam Files

- Create `knowledge_<class>_<isodate>.md` inside the class folder.
- Include exactly `mc-count` multiple-choice questions.
- Each multiple-choice question must have exactly 4 answer options.
- Each multiple-choice question is worth 4 points total.
- Make the questions as unambiguous as possible, put enough context in.
- Score multiple-choice questions per option: award 1 point for each option that
  is handled correctly, whether it was correctly checked or correctly left
  blank.
- For every multiple-choice question, explicitly allow students to mark `-`
  and briefly explain why they consider the answer ambiguous or
  context-dependent.
- Include exactly `free-count` free-form questions.
- Each free-form question is worth 15 points.
- Put a friendly "Gutes Gelingen" footer at the bottom.

### 5. Generate Solution File

- Create `knowledge_<class>_<isodate>_solutions.md` in the same folder.
- Keep the student-facing exam and the solution file separate.
- Do not include the solutions in the student-facing exam file.

### 6. Constraints

- Do not commit any generated files, EVER. The teacher will add them manually
  after the exam is over.
- Preserve existing files unless the task explicitly requires replacement.
- Write both generated Markdown files in German.
- UTF-8 is explicitly allowed and preferred in generated Markdown files.
- Do not replace German umlauts with transliterations such as `ae`, `oe`, or
  `ue` unless the surrounding source material explicitly requires that form.

## Output Expectations

- Student exam file in German with the required question counts and scoring.
- Separate teacher solution file in German.
- Filenames must include the class name and the exam date in ISO format
  (resolved from the mandatory `exam-date` parameter).
