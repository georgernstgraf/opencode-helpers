---
description: Create a GitHub issue from /tmp/issue.md and remove the file
---
Create a GitHub issue from `/tmp/issue.md`.

## Pre-flight Checks

1. **Verify `/tmp/issue.md` exists** - If not, fail with an error message and stop.
2. **Verify current directory is Git-tracked** - Run `git rev-parse --is-inside-work-tree`. If it fails or returns nothing, fail with an error message and stop.

## Parse the File

1. Read `/tmp/issue.md`
2. The first line must be a single `#` heading (the issue title):
   - Strip the leading `# ` to get the title
   - If the first line doesn't start with `# `, fail with an error
3. The remaining lines form the issue body (may be empty)

## Create the Issue

Use `gh issue create` with:
- `--title` = the extracted title (without the `# `)
- `--body` = the remaining content (or `--body-file` if preferred)

Output the created issue URL to confirm success.

## Cleanup

After the issue is created successfully, delete `/tmp/issue.md`.

If any step fails, leave the file intact so the user can retry.