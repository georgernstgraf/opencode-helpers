---
name: repo-sync
description: "Sync all working repositories: pull, let the agent decide what uncommitted work to commit and what to push, and optionally upgrade opencode and restart the server. Use when the user says 'repo sync', 'morning sync', 'Morgen-Sync', 'Tagesstart', 'sync everything', 'pull all repos', 'commit and push everything', or wants the daily sync routine."
license: MIT
compatibility: opencode
metadata:
  category: infrastructure
  scope: multi-repo
---

# Repo Sync

Synchronize every configured working repository, with the **agent making the
commit and push decisions**. The bundled script only gathers facts; it never
commits, never pushes, never restarts anything.

```
collect facts  ->  judge each repo  ->  commit / push  ->  report
   (script)          (agent)             (agent)          (agent)
```

## The one rule

**The script reports. The agent decides.** `scripts/repo-sync.sh` is a fact
collector: dirty counts, ahead/behind, branches, upstreams, SVN status. It
exits non-zero if any repository failed, and that is the only thing it decides.

## Config

`config.json` next to this file is the versioned source of truth:

| Key | Meaning |
|---|---|
| `roots[]` | `{type, path, max_depth}` — `git` roots are scanned for `.git`, `svn` roots for `.svn`. `~` is expanded. |
| `push.allow_owners[]` | Remote owners (second-to-last path segment) that may be pushed to. |
| `push.deny_paths[]` | Roots that are never pushed, regardless of owner. |
| `push.require_upstream` | When true, a repo with no upstream is never pushed. |
| `commit.never_commit_globs[]` | Hard secrets that must never be staged. |
| `commit.max_review_files` | Above this many changed files, do not commit blindly. |
| `host_steps.*` | `opencode_upgrade`, `restart_service` — both `false` by default. |

`max_depth` is the depth **of the VCS directory**, not the repository: for
`~/repos/<owner>/<repo>/.git` that is `3`, for `~/svn/<wc>/.svn` it is `2`.

## Phase A — Collect

```sh
"$HOME/.config/opencode/skills/repo-sync/scripts/repo-sync.sh"
```

Resolves through the symlink; `~/repos/georgernstgraf/opencode-helpers/skills/repo-sync/scripts/repo-sync.sh`
works too. Full output is also written to
`~/.local/state/repo-sync/latest.log` — read it if the in-session output was cut
short by a restart.

**If the script reported any `ERROR:` line, do not commit and do not push.** A
failed fetch or `svn up` means the local view is stale, and a push on top of a
stale view is how force-push accidents happen. Report the errors instead.

The report format is one `## <type> <path>` block per repository, then
`key=value` lines (`owner`, `branch`, `upstream`, `ahead`, `behind`, `dirty`,
`remote`) and, if anything changed, a `--- status ---` block.

## Phase B — Commit judgment

Only for repositories with `dirty > 0`. Read the status block, then decide per
repository.

**Commit** when the change is coherent, self-explanatory, and recognizable as
finished work:

- one logical unit — all changed files serve a single purpose
- recognizable as completed agent or author work: a new dated lesson folder, a
  documentation update, a rename that replaces an older folder
- no half-finished debugging, no stray scratch files, no secrets

Write a commit message in the repository's existing style. Do not invent issue
numbers. If the repository tracks issues, link the real one.

**Leave it, and say why** in the report, when:

- the change mixes unrelated concerns and cannot be split without judgment
- more than `commit.max_review_files` files changed — report, do not bulk-add
- a file matches `commit.never_commit_globs` (secrets) — never stage those
- the content is genuinely ambiguous: unfinished, or unclear what it is for

Content types that are **not** a reason to hold back, when the repository
already tracks them: PDFs, student submissions, CatchLog files, generated
output. `matura-diplom-koll` tracks 110 PDFs and commits them deliberately —
matching the repository's existing practice is the correct default.

## Phase C — Push judgment

Push a repository only when **all** of these hold:

1. its `owner` is in `push.allow_owners`
2. its path is not under `push.deny_paths`
3. `require_upstream` is satisfied — a repo without an upstream has nowhere to go
4. the `fork-policy` skill does not apply to it (forks stay on feature branches)
5. it is green: the repository's tests and lint pass, if it has any

A `fetch` error in Phase A blocks this phase entirely.

`deny_paths` exists for two shapes of repository: a **pull-only foreign
upstream** (`mattpocock/skills` — pushing there would corrupt a checkout the
user only mirrors) and **local-only clones** (`no-remote/`, `non-git/`).

Non-default branches are not a reason to hold back. If the owner is allowed and
the branch has an upstream, the branch is the user's own work and is pushed.

## Phase D — Report

Always close with a table, then a "left alone" section listing every
repository you deliberately did not touch, with the reason. Silent omission
makes a partial sync look like a complete one.

```
| Repository | Action | Commit | Push |
|---|---|---|---|
| georgernstgraf/GRG-WMC | committed | 1a2b3c4 | yes |
| georgernstgraf/matura-diplom-koll | committed | 5d6e7f8 | yes |
| someorg/repo | left alone | — | no — 40+ files changed, needs review |
```

Name the log path so the user can read the raw report afterwards.

## Optional host steps

`host_steps` are **off** by default. Enable them per run, or permanently in
`config.json`, only when the user asks for the full workstation routine.

- `opencode_upgrade` — `opencode upgrade`
- `restart_service` — `systemctl --user restart opencode.service`

**A service restart ends the calling opencode session.** The tool call is killed
as the service cgroup is torn down. That is why it is not a default step, and
why the script still gates it: it runs only when every earlier step succeeded,
so a failed sync leaves the session alive to report the error. Full output is in
`~/.local/state/repo-sync/latest.log` precisely because the in-session output is
lost across a restart.

## Pitfalls

- **The script must stay commit-free.** Once a script can commit, the judgment
  is gone and the report no longer describes what happened.
- **Never log an unredacted remote URL.** The script masks
  `https://user:token@host` and `ghp_`/`gho_` tokens before anything reaches the
  log. Do not print remotes yourself outside that path.
- **Credentials belong in the credential store, not in the URL.** `git@github.com:`
  is the house style for 20 of 20 remotes; `https://user:token@` leaves the token
  in `.git/config`.
- **`~/bin` is not on the agent's PATH** (only `.bash_aliases` adds it in
  interactive shells), so absolute paths are required for anything in there.
- **Do not reintroduce `~/bin/svnkack.sh`.** It commits with an empty message
  (`svn commit -mm`), never checks errors, and 3 of its 5 paths no longer exist.
  SVN commits are an agent decision, same as Git.
