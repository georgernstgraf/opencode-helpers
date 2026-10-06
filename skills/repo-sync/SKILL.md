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

Synchronize every configured working repository. The goal of a run: **when it
ends, every repository is on the state of its upstream** — fast-forwarded or
rebased where that is clean. The bundled script does the fetch and the clean
catch-up; the **agent makes the commit and push decisions**. The script never
commits, never pushes, never restarts anything.

```
fetch + catch up  ->  judge each repo  ->  commit / push  ->  report
   (script)             (agent)             (agent)          (agent)
```

## The one rule

**The script fetches and catches up; the agent decides commits and pushes.**
`scripts/repo-sync.sh` fetches every remote, fast-forwards or rebases clean
checkouts onto their upstream, and reports dirty counts, ahead/behind, branches
and upstreams. It exits non-zero if any repository failed — a conflict, a failed
fetch, or a failed pull. What to commit and what to push stays an agent decision.

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
| `fetch.all_remotes` | Fetch every remote of a repo, not just `origin`. |
| `pull.enabled` | When true (default), clean behind/diverged checkouts are caught up automatically. |
| `pull.on_diverged` | `rebase` (default) replays the local-only commits onto the upstream; any other value leaves a diverged repo untouched. |
| `pull.on_conflict` | `abort-and-report` (default) aborts a conflicting rebase and leaves the repo unchanged. |
| `host_steps.*` | `opencode_upgrade`, `restart_service` — both `false` by default. |

`max_depth` is the depth **of the VCS directory**, not the repository: for
`~/repos/<owner>/<repo>/.git` that is `3`, for `~/svn/<wc>/.svn` it is `2`.

## Phase A — Fetch & catch up

```sh
"$HOME/.config/opencode/skills/repo-sync/scripts/repo-sync.sh"
```

Resolves through the symlink; `~/repos/georgernstgraf/opencode-helpers/skills/repo-sync/scripts/repo-sync.sh`
works too. Full output is also written to
`~/.local/state/repo-sync/latest.log` — read it if the in-session output was cut
short by a restart.

For each git repository the script:

1. fetches **every** remote (not just `origin`), so `fork`/`upstream` are current
   too — with `GIT_TERMINAL_PROMPT=0`, a credential prompt can never block the run;
2. measures `ahead`/`behind` against the branch's upstream **after** that fetch;
3. catches the checked-out branch up **cleanly**:
   - clean and only behind → `git merge --ff-only <upstream>` → `pull=ff(n)`
   - clean and diverged → `git rebase <upstream>`, replaying the local-only
     commits on top → `pull=rebase(n)`
   - dirty → left untouched, `pull=skipped(dirty)` (the agent commits first)
   - no upstream / pull disabled → `pull=skipped(no-upstream)` / `pull=disabled`
   - rebase conflict → `git rebase --abort`, repo unchanged, `pull=conflict` + `ERROR`

SVN working copies get `svn up` — the same catch-up.

An `ERROR:` line (failed fetch of the **upstream's** remote, a rebase conflict,
a failed pull) blocks **that repository only** — no commit, no push for it. A
**secondary** remote that no longer resolves (e.g. a deleted fork) is only a
`WARN:` and never stops the catch-up, because it does not affect the tracked
branch. The other repositories in the run are unaffected and must still be
synced; one unreachable remote must not stall the other 74.

Two errors are **not** per-repository and do stop everything:

- exit code **2** — the script could not start (unparsable config, missing tool).
  Fix the configuration before doing anything else.
- a `WARN: … root does not exist` line — that host simply has no such root;
  the remaining roots still run.

The report format is one `## <type> <path>` block per repository, then
`key=value` lines plus, if anything changed, a `--- status ---` block:

| Key | Meaning |
|---|---|
| `owner`, `branch`, `upstream`, `remote` | identity of the checkout |
| `ahead`, `behind` | counts **after** the catch-up above |
| `diverged` | `true` if the branch was ahead **and** behind when collected |
| `dirty` | number of changed paths (the `--- status ---` block lists them) |
| `fetched` | remotes fetched this run, comma-separated |
| `pull` | `uptodate` \| `ff(n)` \| `rebase(n)` \| `skipped(<reason>)` \| `disabled` \| `conflict` \| `failed` |

**A run is done only when nothing is left behind.** After Phase A every repo
should show `behind=0`. A repo that still shows `behind>0` could not be caught up
cleanly — it was dirty or conflicted. Handle it in Phase B; if the report is
unclear about what a repo needs, **ask the user instead of guessing.**

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

- **another process is writing into the repository right now** — see below
- the change mixes unrelated concerns and cannot be split without judgment
- more than `commit.max_review_files` files changed — report, do not bulk-add
- a file matches `commit.never_commit_globs` (secrets) — never stage those
- the content is genuinely ambiguous: unfinished, or unclear what it is for

### Check for a concurrent writer first

The single most damaging commit this skill can make is one that snapshots work
another agent is halfway through. Before committing a dirty repository, check
whether it is still being written to:

```sh
find <repo> -newermt '-30 minutes' -not -path '*/.git/*' -printf '%TH:%TM %p\n'
ps aux | grep -E 'opencode (attach|serve)|claude|codex' | grep -v grep
```

Fresh mtimes are normal for a repository you just worked on yourself, so compare
against your own timeline rather than treating any recent file as suspect. But
if a **second** opencode/agent session is running against the same tree, the
changed files are work in progress: leave the repository alone and name it in the
report. A half-written lesson that is missing its `praesentation.html` is worse
in history than uncommitted — it is a broken artifact everyone will trust.

This is a real occurrence, not a hypothetical: a concurrent `opencode attach`
was generating GRG-PMM lessons while the sync ran, and the incomplete
`KM7-02-chi-quadrat-test/` had to be skipped.

Content types that are **not** a reason to hold back, when the repository
already tracks them: PDFs, student submissions, CatchLog files, generated
output. `matura-diplom-koll` tracks 110 PDFs and commits them deliberately —
matching the repository's existing practice is the correct default.

After committing, a repo that Phase A skipped with `pull=skipped(dirty)` may
still be behind its upstream. Catch it up now — re-run the script, or run
`git pull --ff-only` / `git pull --rebase` in that repo — so the run ends with
`behind=0` before you move on.

## Phase C — Push judgment

Push a repository only when **all** of these hold:

1. its `owner` is in `push.allow_owners`
2. its path is not under `push.deny_paths`
3. `require_upstream` is satisfied — a repo without an upstream has nowhere to go
4. the `fork-policy` skill does not apply to it (forks stay on feature branches)
5. it is green: the repository's tests and lint pass, if it has any

A `fetch` error in Phase A blocks **that repository**, not the run.

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

## Self-test

`scripts/test-repo-sync.sh` builds throwaway bare remotes and clones in a temp
dir and checks every pull decision (uptodate, behind → ff, diverged → rebase,
dirty → skip, no upstream, pull disabled). Run it after any change to the fetch
or pull logic; it must stay green and it never touches a real repository.

## Pitfalls

- **The script fetches and catches up, but must stay commit- and push-free.**
  A fast-forward/rebase of a clean checkout is mechanical; deciding what to
  commit and what to push is not — that judgment stays with the agent.
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
