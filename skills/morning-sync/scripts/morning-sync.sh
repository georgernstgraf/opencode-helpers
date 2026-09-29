#!/usr/bin/env bash
#
# morning-sync.sh - one-shot morning sync for the dell workstation.
#
#   1. git pull every repository under ~/repos (via allgits-pull)
#   2. sync the SVN working copies (via svnkack.sh)
#   3. upgrade the opencode binary (opencode upgrade)
#   4. restart the opencode server
#
# Step 4 terminates opencode.service and therefore the agent session that
# invoked this script. It is deliberately gated: any earlier failure aborts
# before the restart so the session survives to report the error.
#
# Usage: morning-sync.sh
# Logs:  ~/.local/state/morning-sync/<timestamp>.log (also latest.log)

set -u

HOME_DIR="${HOME:?HOME is not set}"
ALLGITS="$HOME_DIR/bin/allgits-pull"
SVNKACK="$HOME_DIR/bin/svnkack.sh"
OPENCODE="$HOME_DIR/.opencode/bin/opencode"
REPOS="$HOME_DIR/repos"
SERVICE="opencode.service"

LOG_DIR="$HOME_DIR/.local/state/morning-sync"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$(date +%Y%m%d-%H%M%S).log"
ln -sfn "$LOG" "$LOG_DIR/latest.log"

exec > >(tee -a "$LOG") 2>&1

step() { printf '\n==> [%s] %s\n' "$1" "$2"; }
die()  { printf 'ERROR: %s\n' "$1" >&2; exit 1; }

step 1/4 "git pull across $REPOS"
[ -d "$REPOS" ]    || die "$REPOS does not exist"
[ -x "$ALLGITS" ]  || die "$ALLGITS not found or not executable"
( cd "$REPOS" && "$ALLGITS" ) || die "allgits-pull reported a failure; aborting before restart"

step 2/4 "svn sync via $SVNKACK"
[ -x "$SVNKACK" ] || die "$SVNKACK not found or not executable"
"$SVNKACK" || die "svnkack.sh reported a failure; aborting before restart"

step 3/4 "upgrade opencode"
[ -x "$OPENCODE" ] || die "$OPENCODE not found or not executable"
"$OPENCODE" upgrade || die "opencode upgrade failed; skipping restart"

step 4/4 "restarting $SERVICE (this ends the current opencode session)"
systemctl --user restart "$SERVICE"
