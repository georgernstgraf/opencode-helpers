# Global Agent Instructions

These instructions apply to ALL opencode sessions on every host. They are
versioned in `georgernstgraf/opencode-helpers` and linked as
`~/.config/opencode/AGENTS.md`. They override the opencode default policy
"never commit changes unless the user explicitly asks you to" for the
workflows below.

## Continuous Issue Awareness

- At any point in a session, the agent must know which GitHub issue it is
  currently working under.
- Before starting work, resolve the current issue: search open issues first
  (`gh issue list` / `gh issue view <N> --json title,body,comments`) for one
  matching the task.
- If no existing issue matches and the task is clearly a new topic, create a
  new issue immediately and without user interaction, then announce it.
- If the assignment is ambiguous (several candidate issues, or unclear whether
  a new one is needed), ask the user before touching code.
- Announce the resolved issue to the user at the start of the work
  (e.g., "Working under issue #123: <title>").
- Exception: repositories without an issue system (e.g., pure SVN working
  copies) — skip issue resolution entirely and work with clear commit
  messages only.

## Proactive Commit and Push

- After each completed, self-contained unit of work, commit and push — do not
  wait for the user to request it. This overrides the opencode default
  "never commit unless asked" for this workflow.
- **Green commits only:** run the repository's tests/lint for the affected
  area first. Commit only when they pass. If verification fails, fix or
  report — never push a broken state.
- Every commit message must reference the issue number with a hashtag
  (e.g., `feat: add report export (#123)`), preserving the repository's
  existing commit-message style. Never fabricate issue numbers.
- No empty commits. If there is nothing to commit, say so instead.
- Trunk-based: commit and push directly to the tracked trunk line (`main`);
  no feature branches or PRs — unless the repository follows the
  `fork-policy` skill (then that policy wins).
- SVN working copies: the analogue is frequent, clear `svn ci` with a
  descriptive German commit message.

## Observed Drift

When an observation in a session contradicts a statement in `docs/ai/` or
`AGENTS.md` (a host's command output, a file that is not where the docs say,
a documented command that returns nothing or something else), fix it or file
a HANDOFF task **in the same session**. It never stays only in the chat or in
agent-private memory. The `knowledge-persistence` skill describes the how
(section "2b. Observed Drift"); a single observation is enough for a task,
not necessarily for a replacement statement.

## Headless Agent Jobs

- Any unattended opencode run (systemd timer, cron, CI, scripted
  `opencode run`) MUST pin its model explicitly:
  `opencode run --model <provider>/<model>[#variant] …`.
- Never rely on the configured default or on opencode's fallback: without an
  explicit `--model`, opencode V2 uses the **newest available catalog model**,
  which drifts silently on every catalog update (cost and quality risk).
  Verified 2026-10-11: the offers job ran on `opencode-go/claude-haiku-5-5`
  purely because it was the newest entry (KI-Kustodiat issue #33).
- The `#variant` (e.g. `#high`) can only be set on the command line — the root
  `model` config key cannot retain one.
- Pin the agent too (`--agent <id>`) when the job depends on a specific system
  prompt or permission set.

## Context Economy (Subagent Delegation)

- **Measured, not theoretical (2026-11-13/14, `polished-recognition` epic
  #158).** 4 sub-issues + review + docs wave = 7 commits, 10 sub-agents,
  closed at **~12 % of the window**: one report in, one filtered
  verification out per unit — never a diff, never a test log, never
  inline debugging.
- **Trigger.** More than one file, more than one verification cycle, or a
  read whose value is a summary → load the `orchestration` skill, run it in
  waves with a spec file per unit (`/tmp/opencode/specs/<issue>-<wave>.md`).
- The main session's context is the scarcest resource. Delegate
  context-heavy, well-specified units to a fresh subagent instead of
  running them inline — large file reads, verbose verification, batch
  conversions of similar items, research that ends in a summary
  anyway. Before a big inline read, ask: "Would a subagent absorb
  this?"
- Work orders are self-contained: the subagent starts with zero
  history. Include (or link) the full spec — a spec file works — with
  exact paths, the reference pattern, verification steps and their
  expected results, and the boundaries (e.g. off-limits files, who
  commits).
- Reports are signal-dense, not just short: verdicts plus anomalies
  verbatim, plus pointers (paths, line numbers) to what deserves a
  look. Echoing bulk (full file contents, raw logs) stays in the
  subagent — a report that hides the evidence behind its own verdict
  is a failed report.
- The report navigates the verification gate, it never replaces it:
  spot-check claims before acting on them, and continue the
  subagent's session for detail instead of re-doing its work inline.
- **A cached green is not a green.** Force test execution before a wave
  counts: `BUILD SUCCESSFUL in 2s` over an `UP-TO-DATE` task verified
  nothing.
- Known-up-front work (N items, M done): prepare the shared spec and
  parameterized scripts once, centrally — then each item is one short
  prompt plus one short report.

## Issue Completion

- When the agent believes the issue's goal is fully implemented, it **closes
  the issue autonomously** — no need to ask first — and reports the closure,
  naming the issue number, in its final message to the user.
- It may close only when ALL of these hold:
  - the implementation covers the issue goal completely,
  - verification (tests/lint) is green,
  - the issue has no open sub-issues (always check via the `issue-workflow`
    sub-issues API first),
  - the user has not signalled anything that contradicts completion.
- If any criterion is not met, report the status, state what is missing, and
  ask.

## Scope Exclusions (read-only stays read-only)

The proactive commit/push and auto-close rules DO NOT apply when:

- running grading or read-only skills (`homework`, `grading-shared`,
  `projectgrade`) — those skills forbid committing and must never be
  overridden,
- `knowledge-assessment`, `knowledge-exam` and `repograde` are the exceptions:
  they create and commit their files inside the private `<subject>-T` repo
  (never in a public repo and never in student repositories), and `repograde`
  still never commits a student repository,
- working inside student repositories (grading targets stay untouched),
- the user explicitly asks to hold changes back,
- the session is a non-coding personal agent without a repository work
  order (e.g. `coach`, workspace `~/coach`) — the issue-awareness,
  proactive commit/push, and issue-completion rules never apply to such
  agents; they never commit and work only in their own memory
  directories.

Knowledge files (`docs/ai/`) updates are part of the normal workflow and are
committed like any other change under the rules above.
