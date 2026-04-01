---
name: issue-workflow
description: Manage issue-based start, checkpoint, and finish workflows with mandatory issue-linked commits
license: MIT
compatibility: opencode
metadata:
  category: workflow
  scope: github
---

# Issue Workflow Skill

## Purpose

This skill manages GitHub issue-centered work from start through progress
checkpoints to final completion. It standardizes how the agent discovers or
creates an issue, reports progress, commits work, and closes out delivery.

Use this skill whenever the user invokes an issue-oriented command such as
`/issue-start`, `/issue-commit`, or `/issue-finish`.

## Required Inputs

- `mode`: one of `start`, `commit`, or `finish`
- `issue`: optional issue identifier or `new`
- `context`: optional plain-language task summary, plan, or notes

## Core Rules

- Every commit created by this workflow must reference a GitHub issue number.
- Never create a commit without first identifying an existing issue or creating
  a new one.
- If no relevant issue exists and a commit is needed, create the issue first,
  then use its number in the commit message.
- Prefer keeping one clear issue per workstream; do not scatter related changes
  across multiple issues unless the user explicitly requests it.
- Use `gh` for all GitHub issue operations.
- Do not close an issue unless the workflow is running in `finish` mode and the
  implementation is actually complete.

## Commit Message Rule

- Any commit created by this workflow must include the issue reference, such as
  `feat: add report export (#123)` or `fix: handle empty inputs (#123)`.
- If the repository already uses a recognizable commit message style, preserve
  that style while still including the issue number.

## Mode Protocols

### 1. `start`

Use this mode to begin or resume work.

- If `issue` is an explicit issue number, fetch it with `gh issue view` and read
  the description plus comments.
- If `issue` is `new`, or if no usable issue exists for the current work,
  create a new issue from the provided context.
- If no issue is supplied, infer whether there is already a current issue for
  the work. If not, create one before proceeding.
- Assess the codebase against the issue. If the requested functionality is
  already complete, comment with the finding, close the issue, and stop.
- Resolve any blocking ambiguity with the user only after doing all safe local
  discovery work first.
- Update the issue description or add a progress comment with the current plan,
  scope, or todo list.
- Implement the requested changes.
- Do not commit in `start` mode unless the user explicitly asks for it.

### 2. `commit`

Use this mode when progress should be saved but the issue remains open.

- Ensure a current issue exists; create one if needed from the current context.
- Comment on the issue with a concise implementation report covering:
  - what was completed
  - what remains
  - known risks, blockers, or follow-ups
- Review git status and staged/unstaged changes.
- Create a commit that includes the issue number.
- Push the branch.
- Keep the issue open.

### 3. `finish`

Use this mode when the task is complete and the issue should be closed.

- Ensure a current issue exists; create one if somehow missing so the completed
  work still has a tracked issue reference.
- Comment on the issue with a final implementation report.
- Persist all newly acquired session knowledge by also using the
  `knowledge-persistence` skill before finalizing the workflow.
  Note: knowledge-persistence itself never closes issues. The issue
  closure below is owned exclusively by this `finish` mode.
- Review git status and remaining changes.
- Create the final commit including the issue number.
- Push the branch.
- Close the issue with a short closing comment if helpful.

## Issue Creation Guidance

When creating an issue:

- Write a short, outcome-oriented title.
- Include enough body detail for a future agent to understand scope and intent.
- If a plan already exists, use it as the issue body or convert it into a short
  checklist.

## Reporting Guidance

Issue comments should be compact but useful.

- Progress comments should mention completed work, current status, and next
  steps.
- Final comments should mention the shipped outcome and any noteworthy caveats.

## Safety Constraints

- Never fabricate issue numbers.
- Never create an empty commit when there are no changes.
- If there are no local changes in `commit` or `finish` mode, still update the
  issue comment as needed, but report that there was nothing to commit.
- Do not push or close issues if the relevant step fails.

## Output Expectations

At the end of the workflow, report:

- the issue number used or created
- whether a comment was added
- whether a commit was created, including its message
- whether knowledge persistence was run
- whether the issue remains open or was closed
