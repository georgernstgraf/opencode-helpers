#!/usr/bin/env bash
#
# test-repo-sync.sh - self-test for repo-sync.sh.
#
# Builds throwaway bare remotes and clones in a temp dir, then checks the pull
# decisions the skill makes: uptodate, behind -> fast-forward, diverged ->
# rebase, dirty -> skip, no upstream -> skip, and pull disabled. Nothing outside
# the temp dir is touched.
#
# Usage: scripts/test-repo-sync.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_SYNC="$SCRIPT_DIR/repo-sync.sh"
[ -x "$REPO_SYNC" ] || { printf 'not executable: %s\n' "$REPO_SYNC" >&2; exit 2; }
command -v git >/dev/null 2>&1 || { printf 'git is required\n' >&2; exit 2; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Isolate from the user's git config and never depend on a real identity.
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=test@example.com
export GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=test@example.com

PASS=0
FAIL=0
ok()  { PASS=$((PASS + 1)); printf '  ok   %s\n' "$1"; }
bad() { FAIL=$((FAIL + 1)); printf '  FAIL %s\n' "$1"; }

# assert <label> <extended-regexp> - match against the last run's report
assert() {
    if grep -qE "$2" "$TMP/out"; then
        ok "$1"
    else
        bad "$1"
        printf '       pattern not found: %s\n' "$2"
        sed 's/^/       | /' "$TMP/out"
    fi
}

# assert_no_error <label> - the last run must not contain an ERROR line
assert_no_error() {
    if grep -q '^ERROR' "$TMP/out"; then
        bad "$1"
        sed 's/^/       | /' "$TMP/out"
    else
        ok "$1"
    fi
}

# run_sync <root> [extra-config-json] - run the skill against a temp config
run_sync() {
    local root="$1" extra="${2:-}"
    printf '{"roots":[{"type":"git","path":"%s","max_depth":2}]%s}\n' "$root" "$extra" \
        > "$TMP/config.json"
    REPO_SYNC_CONFIG="$TMP/config.json" REPO_SYNC_LOG_DIR="$TMP/log" \
        "$REPO_SYNC" > "$TMP/out" 2>&1 || true
}

# new_case <name> - create bare remote + clone; sets CASE, REMOTE, WORK.
# The bare remote lives outside the scanned root so only the clone is reported.
new_case() {
    local name="$1"
    CASE="$TMP/cases/$name"
    REMOTE="$TMP/remotes/$name.git"
    WORK="$CASE/repo"
    mkdir -p "$CASE"
    git -c init.defaultBranch=main init -q --bare "$REMOTE"
    git -c init.defaultBranch=main init -q "$WORK"
    git -C "$WORK" remote add origin "$REMOTE"
    printf 'base\n' > "$WORK/file.txt"
    git -C "$WORK" add file.txt
    git -C "$WORK" commit -qm init
    git -C "$WORK" push -q -u origin main
    git -C "$REMOTE" symbolic-ref HEAD refs/heads/main
}

# remote_commit <name> <filename> <text> - advance the remote via a second clone
remote_commit() {
    local name="$1" f="$2" t="$3"
    local other="$TMP/others/$name"
    git clone -q "$TMP/remotes/$name.git" "$other"
    printf '%s\n' "$t" > "$other/$f"
    git -C "$other" add "$f"
    git -C "$other" commit -qm "remote: $t"
    git -C "$other" push -q origin main
}

printf '== uptodate ==\n'
new_case uptodate
run_sync "$CASE"
assert "uptodate: pull=uptodate"  'pull=uptodate'
assert "uptodate: behind=0"       'behind=0'
assert "uptodate: fetched=origin" 'fetched=origin'

printf '== behind -> fast-forward ==\n'
new_case ff
remote_commit ff b.txt remote-b
run_sync "$CASE"
assert "ff: pull=ff(1)"  'pull=ff\(1\)'
assert "ff: behind=0"    'behind=0'
[ -f "$WORK/b.txt" ] && ok "ff: pulled file present" || bad "ff: pulled file present"

printf '== diverged -> rebase ==\n'
new_case rebase
printf 'local\n' > "$WORK/local.txt"
git -C "$WORK" add local.txt
git -C "$WORK" commit -qm "local work"
remote_commit rebase r.txt remote-r
run_sync "$CASE"
assert "rebase: diverged=true"        'diverged=true'
assert "rebase: pull=rebase(1)"       'pull=rebase\(1\)'
assert "rebase: behind=0"             'behind=0'
assert "rebase: ahead=1"              'ahead=1'
if git -C "$WORK" merge-base --is-ancestor origin/main HEAD 2>/dev/null \
   && [ -f "$WORK/local.txt" ] && [ -f "$WORK/r.txt" ]; then
    ok "rebase: local commit on top of remote, both files present"
else
    bad "rebase: local commit on top of remote, both files present"
fi

printf '== dirty -> skip ==\n'
new_case dirty
remote_commit dirty d.txt remote-d
printf 'edit\n' >> "$WORK/file.txt"
run_sync "$CASE"
assert "dirty: pull=skipped(dirty)" 'pull=skipped\(dirty\)'
assert "dirty: behind=1"            'behind=1'

printf '== no upstream -> skip ==\n'
new_case noupstream
git -C "$WORK" checkout -q -b feature
run_sync "$CASE"
assert "noupstream: pull=skipped(no-upstream)" 'pull=skipped\(no-upstream\)'

printf '== pull disabled ==\n'
new_case disabled
remote_commit disabled x.txt remote-x
run_sync "$CASE" ',"pull":{"enabled":false}'
assert "disabled: pull=disabled"    'pull=disabled'
assert "disabled: behind stays 1"   'behind=1'

printf '== dead secondary remote -> removed, still synced ==\n'
new_case multi
remote_commit multi m.txt remote-m
git -C "$WORK" remote add fork "$TMP/does-not-exist.git"
run_sync "$CASE"
assert          "multi: dead fork removed"      'removed dead remote fork'
assert          "multi: upstream still pulled"  'pull=ff\(1\)'
assert          "multi: behind=0"               'behind=0'
assert_no_error "multi: no ERROR line"
if git -C "$WORK" remote | grep -qx fork; then
    bad "multi: dead fork removed from config"
else
    ok "multi: dead fork removed from config"
fi

printf '== dead ONLY remote -> kept, upstream is ERROR ==\n'
new_case onlyremote
git -C "$WORK" remote set-url origin "$TMP/does-not-exist.git"
run_sync "$CASE"
assert "onlyremote: upstream dead is ERROR" '^ERROR: .*git fetch origin failed'
if git -C "$WORK" remote | grep -qx origin; then
    ok "onlyremote: sole remote kept"
else
    bad "onlyremote: sole remote kept"
fi

printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
