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
sub-issues touch disjoint file sets. Delegation is a three-phase routine:
**pre-flight → brief → post-flight** (template: [delegation-brief.md](./delegation-brief.md)).

**Pre-flight (orchestrator, immediately before dispatch):**
- `git pull --ff-only` (SVN: `up`) in every target repo; resolve divergence
  **before** delegating, never through the sub-agent.
- Re-run the discovery scan **at dispatch time** (search pattern + expected
  file count). Never reuse an older scan — repos can move during the session
  (concurrent commits added quiz files nobody had on the list).

**Mandatory brief components (every delegation prompt):**
- Step 0: `git pull --ff-only` in the target repo; on divergence or failure
  **abort and report** — do not commit.
- **Self-discovery over a fixed file list:** search pattern + expected count;
  a list in the brief is a cross-check, not the truth.
- **Atomic finish:** commit **and** push — or an explicit blocker; never
  leave work committed-but-not-pushed.
- Kill any server/process the agent started; nothing keeps running.
- Report: files changed, exact commands, pushed SHAs, pass/fail per
  verification — or the blocker. Plus only what the sub-agent cannot look up
  itself: the sub-issue number (commit reference), the neighbouring pattern
  to follow, the relevant `docs/ai/` conventions and pitfalls, and the exact
  verification/test command.

**Post-flight sweep (after the wave, regardless of task status):**
- In every touched repo: `git status -sb` + `git log origin/main..HEAD`.
  **"Task cancelled" does not mean "nothing happened"** — a cancelled agent
  may already have committed (only not pushed). Check state, don't trust
  status.
- Find and kill stray processes (`ps`) — sub-agent verification servers.
- Run an independent aggregate verification **against the pushed state** —
  a green verification against a stale tree is worthless.

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
- Sub-agent commits follow the `issue-workflow` proactive commit/push policy
  (issue-linked, green commits only) — delegation prompts must include this
  requirement.
- Never fabricate issue numbers.
- Never create empty commits.
- Escalate to the user when a blocker is fundamental (a design decision is
  needed, or a dependency is missing).
