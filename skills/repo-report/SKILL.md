---
name: repo-report
description: Analyze a Git repository to generate a comprehensive activity report
license: MIT
compatibility: opencode
metadata:
  category: analysis
  scope: execution
  invoked_by:
    - standalone
    - repograder agent
---
# Repo-Report Skill

## Purpose

This skill scans a Git repository, traverses all relevant branches, and processes every commit in enough detail to assess both activity and diligence. The report must go beyond commit messages: it must inspect the actual content of each commit so it can determine which technical topics the student worked on and whether the work is substantively related to the class material.

This skill is **homework-agnostic** - it analyzes repository content without knowledge of specific assignments. It can be used standalone or invoked by the RepoGrader agent.

## Input

- `$1`: Path to the repository to analyze
- `$2`: (optional) Output filename. Default: `report.md`

## Output

Write the report to `$2` in the repository root (or `report.md` if `$2` is not specified).

## Protocol

### 1. Discovery

- Identify all branches (`git branch -a`)
- Enumerate commits from all relevant branches while avoiding duplicate processing of the same SHA
- Collect commit metadata for each commit: SHA, author, date, branch context, and message

### 2. Per-Commit Content Inspection

For every commit, inspect the actual changes with `git show --stat --summary <sha>` and `git show --format=fuller --unified=3 <sha>`.

Record changed files, file types, insertion/deletion volume, and the code or text fragments that reveal the real topic of the work.

Use the diff content, not just filenames, to identify what the student worked on.

### 3. Topic Detection

Identify topics from diff content. General patterns by language/technology:

| Language | Patterns to Detect |
|----------|-------------------|
| **JavaScript** | functions, arrow functions, async/await, promises, modules (import/export), DOM manipulation, event handlers, fetch API, callbacks, template literals, destructuring, spread operators, Node.js patterns |
| **Java** | classes, interfaces, inheritance (extends/implements), generics, collections (List, Map, Set), streams API, exception handling (try/catch, throws), annotations (@Override, @Autowired), constructors, access modifiers |
| **C#** | classes, properties, LINQ queries, async/await, delegates, events, attributes, using statements, namespaces, constructors, access modifiers, Entity Framework patterns |
| **SQL** | SELECT, INSERT, UPDATE, DELETE, JOIN, WHERE, GROUP BY, ORDER BY, subqueries, schema changes (CREATE/ALTER TABLE), indexes, constraints |
| **CSS** | selectors, flexbox, grid, spacing (margin/padding), responsive rules (media queries), color systems, animations/transitions, positioning |
| **HTML** | semantic elements, forms, input types, attributes, accessibility features |
| **General Programming** | variables, functions/methods, loops (for, while, foreach), conditionals (if/else, switch), data structures (arrays, objects, dictionaries), error handling, algorithms, refactoring patterns |

Distinguish substantive work from superficial work:
- **Substantive**: meaningful implementation, refactoring, debugging, feature extension, bug fixes with logic changes
- **Superficial**: renames, whitespace-only edits, trivial formatting, tiny wording changes, auto-generated code without modification

### 4. Topic Extraction and Relevance Analysis

- Derive topics primarily from commit content; use commit message only as supporting evidence
- Assign one or more topic labels per commit based on what actually changed
- Evaluate technical relevance: which subject areas are present, how strongly represented, whether the commit demonstrates real engagement
- Classify each commit with a diligence signal: `high`, `medium`, or `low`
- Provide short evidence notes per commit or grouped topic explaining the classification

### 5. Branch Analysis

- Primary focus: commits on the `main` branch
- **Non-main branch detection**: Identify commits on branches other than `main`
- If significant activity exists on other branches, prepare a dedicated section with:
  - Branch names
  - Commit counts per branch
  - Summary of work performed on each branch
  - Whether branches were merged or remain open

### 6. Activity Analysis

- Count commits per calendar week
- Detect weeks with zero commits between the first and last commit dates
- Highlight bursts of activity, long inactive periods, and whether activity is steady or irregular

### 7. Report Generation

Format findings into Markdown sections. Include at minimum:

- **Repository Overview**: summary of branches, total commits, date range
- **Topic Coverage**: which technologies/languages were worked on, with frequency
- **Per-Commit Technical Analysis**: for each commit - SHA (short), date, message, detected topics, relevance, diligence rating, evidence-based note
- **Non-Main Branch Activity**: (if applicable) branches, commit counts, work summary
- **Activity Over Time**: commits per week, timeline visualization (text-based)
- **Gaps**: weeks with no activity between first and last commit
- **Diligence Assessment**: summary of whether work is sustained, substantive, technically relevant
- **Final Evaluation**: overall assessment for teaching purposes

Write to the specified output file (default: `report.md`).

### 8. Non-Commit

- Do not modify repository history or create commits

## Constraints

- The skill must not modify repository history or commit changes
- Commit messages alone are insufficient evidence - inspect the content of every analyzed commit
- Prefer evidence-based topic detection from diffs over speculative interpretation
- Handle repositories with up to 300 commits efficiently; for larger histories, summarize while preserving per-commit evidence for the analyzed range
- If the repository contains many branches, limit to the default branch and closely related branches, but state the scope limitation in the report
- Separate superficial activity from substantial work - help teachers judge diligence, not just activity

## Usage

**Standalone:**
```
opencode run skill repo-report /path/to/repo [output_filename.md]
```

**Invoked by RepoGrader Agent:**
The agent passes the repository path and a grading-specific output filename (e.g., `<basename>_grading.md`).
