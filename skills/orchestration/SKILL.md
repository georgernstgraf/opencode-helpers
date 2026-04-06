---
name: orchestration
description: Orchestrate sub-agents to decompose, delegate, and deliver work via issue-driven task decomposition
license: MIT
compatibility: opencode
metadata:
  category: workflow
  scope: project-management
dependencies:
  - issue-workflow
  - knowledge-persistence
---

# Orchestration Skill

## Purpose

This skill defines the role of the main agent as a pure orchestrator that
**never writes code**. Its sole responsibilities are:

1. Bootstrap project context before starting any task.
2. Decompose work into well-scoped sub-issues.
3. Delegate each sub-issue to a Task agent for implementation.
4. Collect results, verify correctness, and advance to the next sub-issue.

Use this skill whenever the main agent is coordinating multiple sub-tasks,
managing an epic with sub-issues, or acting as a dispatcher for Task agents.

## Core Principle

> The main agent must not create any code. It reads, plans, decomposes,
> delegates, verifies, and persists. All implementation belongs to Task agents.

## Dependencies

This skill works alongside two companion skills. It does not duplicate their
content — invoke them directly when needed:

- **`issue-workflow`** — For all GitHub issue lifecycle operations: creating
  issues, committing with issue references, posting progress comments, and
  closing issues. Use its `start`, `commit`, and `finish` modes.
- **`knowledge-persistence`** — For persisting session context into the
  structured `docs/ai/` knowledge files. Invoke after meaningful changes or
  when wrapping up a session.

## Knowledge Bootstrap Protocol

Before starting any task, the main agent must read project knowledge files in
order. This ensures the agent operates with full context and does not repeat
discovery work already done by previous sessions.

### Reading Order

1. `docs/ai/HANDOFF.md` — **Read first.** If it contains open tasks, complete
   them before starting any new work unless the user explicitly overrides.
2. `docs/ai/CONVENTIONS.md` — Coding rules and patterns to enforce.
3. `docs/ai/DECISIONS.md` — Chronological record of past choices.
4. `docs/ai/ARCHITECTURE.md` — Current structural map of the system.
5. `docs/ai/PITFALLS.md` — Known failure modes and non-obvious constraints.
6. `docs/ai/STATE.md` — Current project status and completed work.
7. `docs/ai/DOMAIN.md` — Business logic rules (if task involves domain logic).
8. `docs/ai/ONBOARDING.md` — Development environment setup (if relevant).

### Bootstrap Rules

- Read all files before taking any action. Decisions made without full context
  often conflict with established conventions or repeat past mistakes.
- If a file does not exist, skip it silently. Do not create it here — that is
  the responsibility of `knowledge-persistence`.
- The bootstrap reads are for the main agent only. Task agents receive their
  context through the delegation prompt (see below).

## Work Decomposition

### When to Decompose

Decompose work into sub-issues when:

- The user requests a feature or fix that spans multiple files or concerns.
- A single issue would require more than ~30 minutes of agent work.
- The work has natural boundaries (e.g., per-screen, per-component, per-layer).
- Dependencies exist between parts (one must complete before another starts).

Do NOT decompose when:

- The task is a single focused change (one file, one concern).
- Decomposition would create overhead without clarity gain.
- The user explicitly asks for a single atomic change.

### Decomposition Patterns

#### Pattern 1: Epic with Dependency-Ordered Sub-Issues

Use for large features or refactoring efforts where sub-tasks have dependencies.

```
Epic Issue
├── Sub-Issue A (no deps — do first)
├── Sub-Issue B (no deps — do first, parallel with A)
├── Sub-Issue C (depends on A)
├── Sub-Issue D (depends on B)
└── Sub-Issue E (depends on C + D)
```

The epic body must document:
- A **dependency graph** showing execution order.
- **Parallelism opportunities** (which sub-issues can run concurrently).
- A **one-liner per sub-issue** describing its deliverable.
- The **execution chain** (e.g., "A/B parallel → C/D parallel → E").

#### Pattern 2: Parent Issue with Bug Sub-Issues

Use for bug-fix batches where each bug is independent.

```
Parent Issue: Fix various bugs
├── Bug 1: Short description
├── Bug 2: Short description
└── Bug 3: Short description
```

Each bug sub-issue body should contain:
- `## Problem` — User-visible symptom.
- `## Root Cause` — Technical analysis of the underlying issue.
- `## Fix` — Specific code changes with file paths and line numbers.
- `## Files` — List of files to modify.
- `## Verification` — Manual or automated test steps.

#### Pattern 3: Feature with Sequential Sub-Issues

Use for features that can be sliced into sequential deliverables.

```
Feature Issue
├── Sub-Issue 1: Foundation (models, data layer)
├── Sub-Issue 2: Core logic (business rules)
├── Sub-Issue 3: UI integration
└── Sub-Issue 4: Polish (transitions, edge cases)
```

#### Pattern 4: Meta-Issue with Planning

Use when a significant effort requires upfront planning before sub-issues
can be defined. The meta-issue body documents the overall plan, and
sub-issues are created as the plan crystallizes.

### Sub-Issue Body Template

Every sub-issue should contain these sections:

```markdown
## Summary
<one-sentence description of what to implement>

## Tasks
- [ ] <specific code change 1>
- [ ] <specific code change 2>

## Context
Parent: #<epic-number>
<why this sub-issue exists and how it fits the larger goal>

## Files
- `path/to/file1` — <what to change>
- `path/to/file2` — <what to change>

## Verification
- <how to confirm the change works>
```

### Sub-Issue Linking

Use the GitHub Sub-Issues REST API to create parent-child relationships.
See the `issue-workflow` skill for the exact API commands. Key rules:

- Use the database `id` (not the issue `number`) when linking.
- Link sub-issues sequentially, not in parallel, to avoid priority conflicts.
- Each sub-issue can be closed independently; closing all does not auto-close
  the parent.

## Task Agent Delegation Protocol

### Delegation Rules

1. **One sub-issue per Task agent.** Each Task agent handles exactly one
   sub-issue. This keeps the agent focused and the result verifiable.
2. **Provide all necessary context.** The delegation prompt must include:
   - The full sub-issue body (summary, tasks, files, verification steps).
   - Relevant conventions and pitfalls from `docs/ai/` that apply to this
     specific task.
   - File paths and line numbers where changes should occur.
   - Patterns to follow from neighboring code or existing implementations.
   - The issue number for commit message reference.
3. **Specify the expected output.** Tell the Task agent what to return:
   - Files modified and a summary of changes.
   - Whether the build passes.
   - Any blockers or unexpected findings.
4. **Do not micromanage.** State what needs to happen, not line-by-line how.
   Trust the Task agent to read the codebase and apply idiomatic patterns.

### Delegation Prompt Structure

When invoking a Task agent for a sub-issue, use this structure:

```
Implement sub-issue #<number>: <title>

## Summary
<from sub-issue body>

## Tasks
<checkbox list from sub-issue>

## Context
<from sub-issue body, plus any additional notes>

## Files
<from sub-issue body>

## Conventions to Follow
- <relevant convention 1>
- <relevant convention 2>

## Pitfalls to Avoid
- <relevant pitfall 1>

## Verification
<from sub-issue body>

After completing the implementation:
1. Ensure the build passes.
2. Report which files were modified and what changed.
3. Report any blockers or unexpected issues encountered.
```

### Result Collection

After a Task agent completes:

1. **Verify the result.** Check that the reported changes match the sub-issue
   tasks. If the Task agent reported a blocker, assess whether it can be
   resolved or requires user escalation.
2. **Commit the changes.** Use the `issue-workflow` skill's `commit` or
   `finish` mode to commit with the sub-issue number.
3. **Verify CI.** Run `gh run list --limit 3` to confirm CI passes. Do not
   proceed to dependent sub-issues on a red CI.
4. **Update progress.** Comment on the parent issue with completion status.
5. **Proceed to the next sub-issue** in dependency order.

## Dependency Execution Rules

### Sequential Execution

When sub-issues have dependencies, execute strictly in order:
- Sub-issue B that depends on A must wait for A to complete AND pass CI.
- Do not start B until A's CI is green.

### Parallel Execution

When sub-issues have no dependencies on each other:
- They MAY be delegated to separate Task agents concurrently.
- However, concurrent delegation increases risk of merge conflicts in
  trunk-based development. Prefer sequential execution unless the sub-issues
  touch completely disjoint file sets.

### Blocker Handling

If a Task agent encounters a blocker:

1. **Assess severity.** Can the blocker be worked around? Is it a
   misunderstanding of the requirements or a genuine technical limitation?
2. **Resolve locally** if possible by adjusting the sub-issue scope and
   re-delegating.
3. **Escalate to the user** if the blocker is fundamental (e.g., a design
   decision is needed, or a dependency is missing).
4. **Update the issue** with a comment describing the blocker and current
   status. Use the `issue-workflow` skill.
5. **Continue with independent sub-issues** if possible. Do not stall the
   entire epic because one sub-issue is blocked, unless it is on the critical
   path.

## Completion Criteria

Work is not considered complete until ALL of the following are true:

1. **All sub-issues are implemented** and their individual task checklists
   are complete.
2. **The project builds successfully.** Run the standard build command for
   the project (e.g., `./gradlew build`).
3. **CI is green.** Verify with `gh run list --limit 3` and `gh run view <id>`.
   Do not assume CI passes after a push — always check.
4. **Knowledge is persisted.** Invoke the `knowledge-persistence` skill to
   update `docs/ai/` files with any new conventions, decisions, pitfalls,
   or architectural changes discovered during the session.
5. **The parent issue is closed.** Use the `issue-workflow` skill's `finish`
   mode to close the epic/parent issue with a final summary.

## Safety Constraints

- **Trunk-based development.** Commit directly to `main`. No branches, no PRs.
- **Never create empty commits.** If there are no changes, do not commit.
- **Never fabricate issue numbers.** Every issue reference must be a real,
  existing GitHub issue.
- **Always reference the issue number** in commit messages (e.g.,
  `feat: add session cards (#32)`).
- **Always verify CI after pushing.** A broken pipeline can go unnoticed for
  many commits if not explicitly checked.
- **Do not push or close issues** if a step fails. Resolve the failure first.
- **Do not delegate unclear requirements.** If the sub-issue description is
  ambiguous, clarify with the user before creating a Task agent prompt.

## Output Expectations

At the end of the orchestration workflow, report:

- The parent issue number and title.
- Each sub-issue: number, status (completed/blocked/skipped), and commit SHA.
- Whether CI is green.
- Whether knowledge persistence was run and which files were updated.
- Any blockers or items requiring user attention.
