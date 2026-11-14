# Work Order (Template)

Full spec for a delegation larger than one file. The orchestrator writes it
to `/tmp/opencode/specs/<issue>-<wave>.md` and the dispatch prompt only
points at it. Unlike [delegation-brief.md](./delegation-brief.md) — which is
the prompt itself — the work order is the delegation medium: it carries
everything the sub-agent would otherwise re-derive. Fill the angle-bracket
placeholders, delete nothing, keep the section headings.

---

Repo: `<repo path>`. Issue: `<number>` (commit reference `<repo>#<number>`).
Goal: <one sentence — the requirement, not a file list>.

SCHRITT 0 (mandatory, first): `git -C <repo path> pull --ff-only`.
On divergence or failure: abort and report — change nothing.

## Read first

1. `<file>` — <why: the pattern to follow, the convention that binds>.
2. `<file>` — <why>.
   Pitfalls that apply: <name them and say what they mean here — a pointer
   without the content is read by nobody>.

## Measured facts (do not re-derive)

- <what the orchestrator already verified: exact commands and their output,
  test counts, file counts, line numbers, host/device names>.
- <known-broken or flaky thing, and the workaround>.
- <where the reference pattern lives — as evidence, not as a reading list>.

## Tasks

1. <task — one verifiable unit>. Done when: <criterion>.
2. <task>. Done when: <criterion>.

## Boundaries

- May change: <files/dirs>.
- May not change: <files/dirs, code outside the unit, CI, other skills>.
- <symlink, read-only-target or student-repo warnings that apply>.

## Verification (mandatory)

<exact commands + expected results; read output filtered>.
Red = no push — fix, or report an explicit blocker. Force re-execution when
the tool reports a cache hit (`UP-TO-DATE`): a cached green is not a green.

## Finish (atomic)

Commit (message style `<style>`, referencing `<issue reference>`) **and**
push — or report the blocker; never committed-but-unpushed. Kill any
server/process you started.

## Report back

- Verdict first: done / blocked, one line.
- Files changed, pushed SHA(s), pass/fail per verification.
- Anomalies **verbatim** — the surprising output, not its paraphrase.
- Where to look if the orchestrator wants to check: `path:line`.
- Open doubts, and what you judged but did not do.
- One screen. No file dumps, no raw logs, no diff pastes.
