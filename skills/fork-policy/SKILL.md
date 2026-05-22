---
name: fork-policy
description: Enforce clean-main branch policy on forked repositories
license: MIT
compatibility: opencode
metadata:
  category: policy
  scope: git
---

# Fork Policy Skill

## Purpose

Enforce a strict clean-main policy on forked repositories. When active, no
commits may land on `main` or `master` — all work happens on feature branches.

## Core Rule

**NEVER commit directly to `main` or `master` on a forked repository.**

All changes must be made on a feature branch. This keeps the fork's main
branch clean for syncing with upstream and allows multiple feature branches
to coexist without conflicts.

## Rationale

- Forks often need to rebase or merge changes from the upstream repository.
  A dirty main branch makes this significantly harder.
- Multiple feature branches may be in progress simultaneously. Each branch
  should be independently reviewable and mergeable via pull request.
- A clean main branch provides a known-good baseline at all times.

## Branch Naming Convention

Feature branches must follow this pattern:

```
feat/issue-N-short-description
fix/issue-N-short-description
chore/issue-N-short-description
```

Examples:

- `feat/issue-42-add-login-page`
- `fix/issue-17-null-pointer-handling`
- `chore/issue-8-update-dependencies`

The issue number **must** be included in the branch name. If no issue exists
yet, create one first before branching.

## Fork Detection

A repository is treated as a fork if it has **more than one remote**.

```bash
remote_count=$(git remote | wc -l)
```

If `remote_count` is greater than 1 (typically `origin` + `upstream`), the
policy applies. No further analysis needed.

## Safety Check

Before **every** commit, the agent must verify:

1. The current branch is **not** `main` or `master`.
2. If the repo is detected as a fork and the current branch is `main`/`master`,
   the agent must **abort** and inform the user.

The check sequence:

```bash
# Determine current branch
current_branch=$(git branch --show-current)

# If on main/master and repo is a fork, abort
if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
  echo "ABORT: fork-policy forbids commits on $current_branch"
  echo "Create a feature branch first: git checkout -b feat/issue-N-description"
  exit 1
fi
```

## Integration with Issue Workflow

When both `fork-policy` and `issue-workflow` are active:

- When the agent recognizes an issue start intent (natural language), it must
  create an appropriately named feature branch before beginning any implementation work.
- Before committing (issue commit checkpoint), the agent must verify the branch
  policy is satisfied.
- When finishing an issue, the agent must push the feature branch and create or
  update a pull request rather than merging to main directly.

## Activation

This skill is loaded on demand. To activate it for a project, reference it
from the project's `AGENTS.md`:

```markdown
## Active Policies

- **fork-policy**: This is a forked repository. Always use feature branches.
  Never commit to main/master.
```

Or load it explicitly via a skill invocation.
