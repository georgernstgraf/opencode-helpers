---
name: morning-sync
description: "One-shot morning sync on the dell workstation: git-pull every repository under ~/repos, sync the SVN working copies with svnkack.sh, upgrade the opencode binary, then restart the opencode server. Use when the user says 'morning sync', 'Morgen-Sync', 'sync everything', 'pull all repos and restart opencode', 'Tagesstart', or wants the daily pull + upgrade + restart routine."
license: MIT
compatibility: opencode
metadata:
  category: infrastructure
  scope: workstation
---

# Morning Sync

One maintenance routine for the dell workstation, always in the same order:

**pull all Git repos → sync SVN → upgrade opencode → restart the server.**

The logic lives in a bundled script, so it also runs standalone (cron,
systemd timer, plain shell) outside opencode:

`scripts/morning-sync.sh`

## Run it

Run the script and let it finish:

```sh
"$HOME/.config/opencode/skills/morning-sync/scripts/morning-sync.sh"
```

The resolved path (`~/repos/georgernstgraf/opencode-helpers/skills/morning-sync/scripts/morning-sync.sh`)
works equally well.

## What it does

1. `allgits-pull` in `~/repos/` — recursive `git pull` for every repo found.
2. `~/bin/svnkack.sh` — `svn up` + commit across the SVN working copies.
3. `opencode upgrade` — updates the opencode binary explicitly.
4. `systemctl --user restart opencode.service` — restarts the server.

## Critical: the restart ends this session

Step 4 stops `opencode.service`, which is the server hosting *this* agent
session — the tool call is killed as the service cgroup is torn down. That is
intended, but it has two consequences:

- The script **only restarts when every earlier step succeeded.** If a Git
  pull, the SVN sync, or `opencode upgrade` fails, it exits non-zero *before*
  the restart, and the session stays alive so you can report the failure.
- Full output is appended to `~/.local/state/morning-sync/latest.log` (plus a
  timestamped file per run), because the in-session output is lost when the
  server restarts. Read that log if you need the result after a restart.

## Notes / pitfalls

- `~/bin` is **not** on the agent's PATH (only `.bash_aliases` adds it in
  interactive shells), so the script calls `allgits-pull` and `svnkack.sh` by
  absolute path. Do not replace them with bare command names.
- Keep the restart inside the script and gated. Running the restart as a
  separate step, or continuing past a failed sync, would kill the session and
  hide the error.
- `allgits-pull` only pulls (it does not push); `svnkack.sh` commits SVN
  changes. Pushing Git work is a separate action, not part of this routine.
