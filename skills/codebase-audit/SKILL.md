---
name: codebase-audit
description: One-shot, interactive assessment of a whole codebase (a Git repository) across four axes: security (in depth), structure and clean layers, coupling and entanglement (Wartbarkeit), and architecture (deep modules). Fans out parallel sub-agents, lets the user steer scope and importance, then files one epic with formally linked sub-issues. Use when the user asks for a full repo audit, workflow health check, whole-project security review, maintainability assessment, or says "audit the codebase", "codebase audit", "assess this repo".
license: MIT
compatibility: opencode
metadata:
  category: workflow
  scope: codebase
slash: true
---

# Codebase Audit

One-shot, interactive assessment of a whole codebase, ending in a GitHub **epic with sub-issues**. The report itself lives only in chat.

The four axes:

1. **Security (in depth)** - secrets, injection, authn/authz, deserialization, crypto, SSRF, path traversal, dependency CVEs, dangerous config.
2. **Structure & clean layers** - layering violations, boundary leaks, misplaced responsibilities.
3. **Coupling & entanglement** - cycles, fan-in/fan-out hubs, god modules, change coupling. This is the *Wartbarkeit* axis.
4. **Architecture & deep modules** - shallow modules, pass-throughs, seams, testability (the `codebase-design` vocabulary).

Core principle: **deterministic tools compress, the agent synthesizes.** Structure and coupling are graph-computable and therefore exhaustive even on huge repos; security and architecture need reading and are therefore risk-weighted, never claimed exhaustive. Say this in the report.

## Preconditions

- Run from the root of the repository to audit. If the working directory is not a Git repo, confirm the directory with the user first.
- A GitHub issue tracker is assumed (epic + sub-issues). If the repo has none, run the audit and present findings in chat only.
- This skill is **read-only on the audited code**. Its only side effects: (a) finding files in the OS temp dir, (b) GitHub issues.

## Process

### 1. Recon (facts, no user questions)

- Detect languages and build tooling (`package.json`, `pyproject.toml`, `go.mod`, `pom.xml`/`build.gradle`, `Cargo.toml`, ...), plus the test and lint commands.
- Read the project's own guidance: `AGENTS.md`/`CLAUDE.md`, `GLOSSARY.md`/`CONTEXT.md`, ADRs (`docs/adr/`), `CODING_STANDARDS.md`, `CONTRIBUTING.md`.
- Map the top-level module structure (directories/packages) and the entrypoints.
- Measure size: file count, LOC, number of packages/modules.
- Find churn hotspots: `git log --oneline` and the co-change counts from [TOOLS.md](./TOOLS.md), to weight attention (the same hot-spot heuristic as `improve-codebase-architecture`).
- Pick a **tier** from the size (see [Scaling to large codebases](#scaling-to-large-codebases)).
- Summarize recon in chat in a few lines.

Create the scratch dir (`codebase-audit-<timestamp>/`) under the OS temp dir: resolve `$TMPDIR`, falling back to `/tmp`. All tool output and finding files land there, never in the repo.

### 2. Steer (interactive, grilling)

Run the `grilling` loop: ask the frontier in rounds, each question with a recommended answer. The decisions:

- **Target** - this repo, or a subtree?
- **Axes + weighting** - all four by default; which to emphasize?
- **Tier + scope** - whole repo vs. churn hotspots; how deep (top-K subsystems)?
- **Tool policy** - install missing scanners? (default: yes when the network is available)
- **Severity threshold / max tickets** - how many issues are actually useful?
- **Epic** - a new issue, or attach to an existing number?
- **Output** - dry-run (chat only) or file the epic + sub-issues?

Do not start scanning until the user confirms this round.

### 3. Tools (detect, install, run)

Detect the scanners relevant to the detected stack (see [TOOLS.md](./TOOLS.md)). Install missing ones when the user allowed it and the network is up. If installation fails or the network is down, **degrade gracefully**: fall back to bounded hotspot reading and record the degradation for the final report.

Run the scanners and save raw output to `<scratch>/tool-output/`. These outputs, not the agents, are the primary source for structure, coupling, and the mechanical part of security.

### 4. Fan out (one sub-agent per axis)

Spawn **parallel sub-agents**, one per approved axis, each in its own context (one axis must not see another's findings; that independence is the point, exactly as in `code-review`). Each sub-agent gets:

- the recon summary,
- the relevant tool outputs,
- its axis brief from [AXES.md](./AXES.md),
- the finding schema below.

Each writes `<scratch>/findings/<axis>.md`. Cap the number of findings per axis and require evidence for every one.

**Large tier:** do not hand an axis agent the whole repo. Use hierarchical fan-out: the recon map (step 1) → one auditor sub-agent per subsystem (aim for <= ~40-60 files or ~15k LOC each) → a **boundary agent** per axis that reads only the subsystems' exported interfaces plus the tool graph, for cross-subsystem issues (cycles, layering, duplicated concepts) that no single subsystem agent can see. The main agent never loads subsystem source into its own context.

### 5. Synthesize & rank (interactive)

- Read all finding files (files, not transcripts, so the main context stays small).
- Deduplicate: the same root cause surfaced by two axes (a cycle seen by both coupling and architecture) becomes one finding.
- Sort by severity x confidence. Present the ranked list **in chat** (the report is chat-only).
- Let the user steer: promote, drop, merge, raise or lower the threshold. Re-round with `grilling` if a finding needs reshaping.

### 6. Ticket plan (interactive)

Turn the surviving findings into **tracer-bullet tickets** (semantics from `to-tickets`): each ticket is atomic, agent-ready, and verifiable on its own; related findings may group into one ticket. Show a numbered plan (title, what it fixes, blocked-by). Confirm before filing.

### 7. File the epic and sub-issues

- Search open issues first and drop any finding already tracked.
- Create the **epic** issue: title `Codebase audit <YYYY-MM-DD>: <repo>`, body = scope, the four axes, the tier, the tool set used, and a summary table of findings. This is the parent.
- Create each **sub-issue** and link it to the epic using the Sub-Issues API protocol in `issue-workflow` (the formal parent-child link, never a text mention). Apply the triage label (`ready-for-agent` unless told otherwise).
- If the user chose dry-run, stop after presenting the plan.

### 8. Report

State: the epic number, each child number, the findings dropped as duplicates or below threshold, and any degradation (tools not installed, network down).

## Finding schema

Each finding is a block in the axis file:

```
## <SEVERITY> <short title>
- **Evidence:** path:line, path:line
- **Confidence:** high | medium | low
- **Why it matters:** one or two sentences
- **Suggested ticket:** title + one-line scope
```

Severity: `critical | high | medium | low`.

## Scaling to large codebases

| Tier | Trigger (rough) | Strategy |
|------|-----------------|----------|
| Small | <= 20k LOC | Single pass; axis agents read the repo directly. |
| Medium | <= 200k LOC | Tools first; one axis agent each; fan out over top-level packages. |
| Large | > 200k LOC | Tools only for structure/coupling (exhaustive); churn-weighted hotspots; hierarchical per-subsystem fan-out; deep-dive top-K only. |

Honest limit, always stated in the report: at large scale, structure and coupling are exhaustive (graph-computable), while security and architecture are risk-weighted, not a per-file guarantee.

## Done when

- [ ] Recon summarized and the steering round confirmed by the user.
- [ ] Tools run, or graceful degradation recorded.
- [ ] Each approved axis produced a findings file with evidence.
- [ ] Findings deduplicated, ranked, and steered by the user.
- [ ] An epic was filed with formally linked sub-issues (or a dry-run plan presented).
- [ ] The final report names the epic, the children, dropped findings, and degradations.

## References

- [AXES.md](./AXES.md) - the four axis briefs handed to the sub-agents.
- [TOOLS.md](./TOOLS.md) - per-language scanner detection, installation, and invocation.
- Skills this composes: `grilling` (steering), `issue-workflow` (sub-issue protocol), `codebase-design` (architecture vocabulary).
