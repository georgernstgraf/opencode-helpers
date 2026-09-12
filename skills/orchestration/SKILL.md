---
name: orchestration
description: Coordinate large work as a pure orchestrator: decompose into sub-issues and delegate implementation to sub-agents behind a hard verification gate. Use when the work spans more than one session, needs more than one sub-issue, or touches multiple dependent files/concerns; do not use it for a single focused change.
license: MIT
---

# Orchestration

Large work — more than one agent session can hold, or several sub-issues with
dependencies — is coordinated, not implemented inline. The main agent plans,
decomposes, delegates, and verifies; its context stays on the plan rather than
on diffs and debugging.

## When to coordinate vs. act directly

- **Coordinate** (this skill): the work spans more than one session, needs more
  than one sub-issue, touches multiple files/concerns, or has dependencies
  between parts.
- **Act directly**: a single focused change (one file, one concern). Delegation
  would cost more context than the change itself.

## Non-default behaviors

1. **Keep the coordinator's context clean.** For coordinated work the main agent
   does not author code: it reads, plans, decomposes, delegates, and verifies.
   Implementing inline pollutes the context that has to hold the whole plan.
2. **Hard verification gate.** No sub-issue is done until its full test suite
   passes. If a sub-agent reports failing or missing tests, reject the work and
   re-delegate with the failure details. Never start a dependent sub-issue on a
   red gate.

## Delegation

One sub-issue per sub-agent. Run sub-agents sequentially unless their
sub-issues touch disjoint file sets. Each delegation prompt carries a **context
pointer** to the sub-issue plus only what the sub-agent cannot look up itself:

- the sub-issue number (for the commit reference),
- the files to touch and the neighbouring pattern to follow,
- the relevant `docs/ai/` conventions and pitfalls,
- the exact verification/test command.

Require the sub-agent to return: files changed, the exact commands run, and
pass/fail per suite — or an explicit blocker.

## Pointers

- `issue-workflow` owns the issue lifecycle: creating issues, sub-issue linking,
  commits and their issue references, and closing. Do not duplicate its API
  commands here.
- `knowledge-persistence` owns the `docs/ai/` bootstrap order and the knowledge
  files. Read that order once at session start; do not restate it here.
- `code-review` reviews the aggregate diff before the parent issue is closed.

## Constraints

- Trunk-based: commit directly to the tracked trunk line; no long-lived
  branches. See `issue-workflow` for the per-VCS variants (Git `pull`, SVN
  `up`, and the SVN case with no issue system).
- Never fabricate issue numbers.
- Never create empty commits.
- Escalate to the user when a blocker is fundamental (a design decision is
  needed, or a dependency is missing).
