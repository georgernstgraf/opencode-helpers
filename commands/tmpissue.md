---
description: Create a GitHub issue from /tmp/issue.md following the issue-workflow skill, then remove the file
---
Create a GitHub issue from `/tmp/issue.md`, **following the `issue-workflow`
skill end to end**. Do not invent a parallel procedure: load that skill and use
its "Duplicate Check", "Issue Creation Guidance" and "Sub-Issues" sections.

## Pre-flight Checks

1. **Verify `/tmp/issue.md` exists** - If not, fail with an error message and stop.
2. **Verify current directory is Git-tracked** - Run `git rev-parse --is-inside-work-tree`. If it fails or returns nothing, fail with an error message and stop.
3. **Resolve the repository scope** - `gh repo view --json nameWithOwner --jq .nameWithOwner`. All searches stay inside this repo.

## Parse the File

1. Read `/tmp/issue.md`
2. The first line must be a single `#` heading (the issue title):
   - Strip the leading `# ` to get the title
   - If the first line doesn't start with `# `, fail with an error
3. The remaining lines form the issue body (may be empty)

## Duplicate Check (mandatory gate — no `gh issue create` before it passes)

Run the skill's gate in full, in this repository:

1. Derive **2–4 discriminating terms** from the title and body (module name,
   feature noun, error string, file name) — never the whole sentence. If the
   tracker is mixed-language, search German *and* English synonyms.
2. Search, in parallel:
   - `gh issue list --repo <owner>/<repo> --state open --limit 50 --search "<terms>" --json number,title,labels,updatedAt`
   - `gh search issues --repo <owner>/<repo> --state open "in:title,body <terms>" --json number,title,updatedAt`
   - `gh search prs --repo <owner>/<repo> --state open "<terms>" --json number,title`
3. No hit → repeat once with the single broadest term (the feature noun).
4. Read every promising hit with `gh issue view <N> --json title,body,comments`.
   Titles alone are not evidence; the body decides.

Apply the skill's decision matrix — do not shortcut it:

| Finding | Action |
|---|---|
| 0 plausible candidates | create the new issue |
| 1 open issue covers the goal | **do not create** — comment the planned scope there, keep `/tmp/issue.md`, report the issue number and stop |
| 1 open issue covers part of it | **do not duplicate** — work under it; a separate sub-issue only if it needs independent tracking, then link it formally |
| ≥2 plausible candidates, or unclear | **stop and ask the user** — number, title, `updatedAt`, one-line rationale per candidate |
| only closed issues match | create the new issue and name the closed one in the body as a regression/repeat |

Tie-breaker: when in doubt, comment on the existing issue instead of opening a
new one.

## Create the Issue

Use `gh issue create` with:
- `--title` = the extracted title (without the `# `)
- `--body-file` = the extracted body (via a temp file to avoid shell quoting)

Append the audit trace line as the last block of the body:

```
Duplicate check (YYYY-MM-DD): no matching open issue. Checked: #12, #34, search "backup restore".
```

If the work belongs to a parent epic (stated in the file, or known from the
session), link the new issue as a sub-issue per the skill: fetch the child's
database id with `gh api repos/<owner>/<repo>/issues/<N> --jq .id`, then
`gh api --method POST /repos/<owner>/<repo>/issues/<PARENT>/sub_issues --input -`
with `{"sub_issue_id": <id>}` (integer, never `-f`). Link multiple sub-issues
sequentially, not in parallel. Ask before inventing a parent that nobody named.

Announce the issue number and title ("Working under issue #<N>: <title>") and
output the created issue URL.

## Cleanup

Delete `/tmp/issue.md` only after the issue was created successfully.

Leave the file intact when a step fails, when the user must be asked, or when
the content was merged into an existing issue as a comment — so a retry stays
possible.
