---
name: repo-report
description: Analyze a Git repository to generate a comprehensive activity report
license: MIT
compatibility: opencode
metadata:
  category: analysis
  scope: execution
---
# Repo-Report Skill

## Purpose

This skill scans a Git repository, traverses all relevant branches, and processes every commit in enough detail to assess both activity and diligence. The report must go beyond commit messages: it must inspect the actual content of each commit so it can determine which technical topics the student worked on and whether the work is substantively related to the class material.

The report must cover:

- Topics and content themes derived from the actual commit content and supported by commit messages
- Technical relevance of each commit to class subjects such as SQL, CSS, programming fundamentals, control flow, loops, functions, data structures, or framework-specific work
- Evidence that the student engaged substantively with a topic instead of making only superficial edits
- Commit frequency per week
- Gaps longer than one week with no commits

The output is written to `report.md` in the repository root and is not committed.

## Protocol

1. **Discovery**
   - Identify all branches (`git branch -a`).
   - Enumerate commits from all relevant branches while avoiding duplicate processing of the same SHA.
   - Collect commit metadata for each commit: SHA, author, date, branch context, and message.

2. **Per-Commit Content Inspection**
   - For every commit, inspect the actual changes with `git show --stat --summary <sha>` and `git show --format=fuller --unified=3 <sha>`.
   - Record changed files, file types, insertion/deletion volume, and the code or text fragments that reveal the real topic of the work.
   - Use the diff content, not just filenames, to identify what the student worked on. Examples:
     - SQL: queries, joins, filters, table creation, schema changes, `SELECT`, `INSERT`, `UPDATE`, `DELETE`
     - CSS: selectors, layout, spacing, responsive rules, color systems, animations
     - Programming: variables, functions, methods, conditionals, loops, arrays, objects, classes, error handling
     - Web or framework topics: routing, templates, components, forms, API calls, state handling
   - Distinguish substantive work from superficial work. A commit counts as substantive only when the diff shows meaningful implementation, refactoring, debugging, or extension of a topic. Renames, whitespace-only edits, trivial formatting, or tiny wording changes should be marked as low-evidence unless the surrounding diff proves otherwise.

3. **Topic Extraction and Relevance Analysis**
   - Derive topics primarily from commit content and use the commit message only as supporting evidence.
   - Assign one or more topic labels per commit based on what actually changed.
   - Evaluate the technical relevance of each commit to the class topics. The skill should explicitly answer: which subject areas are present, how strongly they are represented in the diff, and whether the commit demonstrates real engagement with the material.
   - When possible, classify each commit with a qualitative diligence signal such as `high`, `medium`, or `low`, based on the depth and specificity of the work shown in the diff.
   - Provide short evidence notes per commit or per grouped topic that explain the classification.

4. **Activity Analysis**
   - Count commits per calendar week.
   - Detect weeks with zero commits between the first and last commit dates.
   - Highlight bursts of activity, long inactive periods, and whether activity is steady or irregular.

5. **Report Generation**
   - Format the findings into Markdown sections that are detailed enough for teaching evaluation. At minimum include:
     - Repository Overview
     - Topic Coverage
     - Per-Commit Technical Analysis
     - Diligence Assessment
     - Activity Over Time
     - Gaps
     - Final Evaluation
   - In `Per-Commit Technical Analysis`, include for each commit at least the SHA short form, date, message, detected topics, relevance to class content, and a short evidence-based note from the diff.
   - In `Diligence Assessment`, summarize whether the student's work appears sustained, substantive, and technically relevant.
   - Write to `report.md` in the repository root.

6. **Non-Commit**
   - Do not modify repository history or create commits.

## Constraints

- The skill must not modify repository history or commit changes.
- Commit messages alone are insufficient evidence. The skill must inspect the content of every analyzed commit.
- The skill should prefer evidence-based topic detection from diffs over speculative interpretation.
- It should handle repositories with up to 300 commits efficiently; for larger histories, it may summarize clearly while still preserving per-commit evidence for the analyzed range.
- If the repository contains a large number of branches, the skill may limit to the default branch and closely related branches, but it must state the scope limitation in the report.
- The report should help a teacher judge diligence, not just repository activity, so it must explicitly separate superficial activity from substantial work.

## Usage

Run the skill via the opencode CLI: `opencode run skill repo-report`.

---
