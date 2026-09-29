# Delegation Brief (Template)

Fill-in template for delegation prompts to sub-agents. The mandatory
components from `SKILL.md` (§ Delegation) are already embedded — fill the
angle-bracket placeholders, delete nothing, keep the section headings.

---

Repo: `<repo path>`. Sub-issue: `<number>` (commit reference `<repo>#<number>`).
Goal: <one sentence — the requirement, not a file list>.

SCHRITT 0 (mandatory, first): `git -C <repo path> pull --ff-only`.
On divergence or failure: abort and report — change nothing.

Then read: <spec/reference file paths + relevant `docs/ai/` conventions and
pitfalls>.

AUFTRAG: <two or three sentences — what "done" means>.
Do NOT assume a file list — discover the targets yourself:
`<grep/find pattern>` → expected: `<N>` files (cross-check: <file list>).
<editing rules — what may and may not change; what stays untouched>.

Verifikation (mandatory): <exact commands + expected results>.
If verification fails: do NOT push — fix, or report an explicit blocker.

Finish: commit (German message, `<issue reference>`) **and** push — atomically;
or report the blocker. Kill any server/process you started.

Report back: files changed, <unit counts>, exact commands run, verification
results, pushed commit SHA(s), open doubts.
