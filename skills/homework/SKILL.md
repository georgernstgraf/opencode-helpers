---
name: homework
description: Generate short homework assignment suggestions from recent class Git history
license: MIT
compatibility: opencode
metadata:
  category: education
  output: suggestion
---

# Homework Skill

## Purpose

This skill generates a short homework assignment suggestion for a specific class
based on Git commits from the last 24 hours. Use it when asked to propose
homework for today's lesson.

## Inputs

- `class`: target class folder name

## Protocol

### 1. Validate Inputs

- Confirm that a folder matching `class` exists in the current working tree.
- If the folder does not exist, stop immediately and report that the class name
  appears to be invalid.
- The following classes are addressed informally in related communication:
  `2ahwii`, `3ahwii`, `5ahwii`, `4aaif`.
- All other classes use formal address in related communication.

### 2. Inspect Source Material

- Analyze Git commits from the last 24 hours that changed files inside the
  class folder.
- Treat minimal commits as lecture anchors rather than complete coverage; infer
  the broader classroom context from the changed material in those commits.
- Review the changed files as needed to understand the topics that were likely
  taught.

### 3. Generate Homework Suggestion

- Output a short homework assignment directly to the user.
- Include 2-4 focused exercises related to the day's material.
- Each exercise should be practical and reinforce the key concepts covered.
- Format the suggestion as Markdown ready for the user to copy.

### 4. Constraints

- **Do NOT create, modify, or write any files.** Output the suggestion directly.
- Preserve existing files.
- Write the suggestion in German.
- UTF-8 is explicitly allowed and preferred.
- Do not replace German umlauts with transliterations such as `ae`, `oe`, or
  `ue` unless the surrounding source material explicitly requires that form.

## Output Expectations

- A short homework suggestion in German with 2-4 exercises.
- Output directly to the user, not to a file.
- Clear formatting for easy copying.
