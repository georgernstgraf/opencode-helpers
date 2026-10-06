#!/usr/bin/env bash
#
# repo-sync.sh - sync the state of all configured working repositories.
#
# Every git repo: fetch all remotes, then fast-forward or rebase the checked-out
# branch onto its upstream when that is clean; dirty or conflicting repos are
# left untouched and reported. Every svn working copy: `svn up`.
# The script deliberately does NOT commit, does NOT push and does NOT restart
# anything - those stay agent decisions, see skills/repo-sync/SKILL.md.
#
# The optional host steps (opencode upgrade, service restart) live behind
# config.json "host_steps" and default to false. When enabled they run last and
# only if no earlier step failed. A service restart ends the calling opencode
# session, so it is never part of a default run.
#
# Usage:  repo-sync.sh
# Config: ${REPO_SYNC_CONFIG:-<skill dir>/config.json}
# Logs:   ${REPO_SYNC_LOG_DIR:-$HOME/.local/state/repo-sync}/<timestamp>.log
#
# Report format: a "## <type> <path>" header per repository, followed by
# key=value lines (branch, upstream, ahead, behind, diverged, dirty, fetched,
# pruned, pull, remote) and an optional "--- status ---" block. Plain text on
# purpose, so both the agent and the test suite can parse it without a JSON
# toolchain.
#
# Exit codes: 0 = every configured repository was collected cleanly
#             1 = at least one repository failed (see ERROR lines)
#             2 = the run could not start (bad config, missing tool)

set -u

# A sync must never block on an interactive credential prompt or an editor.
export GIT_TERMINAL_PROMPT=0
export GIT_EDITOR=true
export GIT_SEQUENCE_EDITOR=true

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${REPO_SYNC_CONFIG:-$SKILL_DIR/config.json}"
LOG_DIR="${REPO_SYNC_LOG_DIR:-$HOME/.local/state/repo-sync}"

die() { printf 'ERROR: %s\n' "$1" >&2; exit 2; }

[ -f "$CONFIG" ] || die "config not found: $CONFIG"
command -v python3 >/dev/null 2>&1 || die "python3 is required to read $CONFIG"
command -v git >/dev/null 2>&1 || die "git is required"

# Read a dotted path out of config.json. Scalars print on one line, lists one
# element per line, and roots print as tab-separated "type<TAB>path<TAB>depth".
cfg() {
    python3 - "$CONFIG" "$1" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    cfg = json.load(fh)

path = sys.argv[2]
node = cfg
for part in path.split("."):
    node = node.get(part) if isinstance(node, dict) else None
    if node is None:
        break

if node is None:
    pass
elif isinstance(node, list):
    if node and isinstance(node[0], dict):
        for item in node:
            print("\t".join(str(item.get(k, "")) for k in ("type", "path", "max_depth")))
    else:
        for item in node:
            print(item)
elif isinstance(node, bool):
    print("true" if node else "false")
else:
    print(node)
PY
}

expand() {
    case "$1" in
        "~")    printf '%s' "$HOME" ;;
        "~/"*)  printf '%s' "$HOME/${1#\~/}" ;;
        *)      printf '%s' "$1" ;;
    esac
}

# Strip credentials before anything reaches the log or the report. Covers
# https://user:token@host and bare ghp_/gho_/github_pat_ tokens.
redact() {
    printf '%s' "$1" | sed -E -e 's#(://[^:/@]+):[^@]*@#\1:***@#g' \
                              -e 's/(ghp|gho|ghs|github_pat)_[A-Za-z0-9_]+/\1_***/g'
}

# Owner is the second-to-last path segment of a hosted remote:
#   git@github.com:acme/tool.git          -> acme
#   https://github.com/acme/tool.git      -> acme
# For a non-hosted path (a local bare repo used as origin) the same shape
# yields the containing directory, which is the best available answer.
remote_owner() {
    [ -n "$1" ] || return 0
    printf '%s' "$1" | sed -E 's#^[^:]+://[^/]+/##; s#^[^:]+:##; s#/$##; s#\.git$##; s#[^/]+$##; s#/$##'
}

# True when a fetch failure means the repository is gone (permanent), as opposed
# to offline/auth (transient). Matches GitHub/GitLab "Repository not found" and
# git's "does not appear to be a git repository" for a missing path/ssh target.
is_dead_remote_error() {
    printf '%s' "$1" | grep -qiE 'repository not found|does not appear to be a git repository'
}

mkdir -p "$LOG_DIR" || die "cannot create log dir: $LOG_DIR"

# Validate the config once, loudly. A config that cannot be parsed must not
# degrade into an empty report that looks like "nothing to do".
if ! cfg roots >/dev/null 2>&1; then
    die "cannot parse $CONFIG (invalid JSON, or roots is not a list of objects)"
fi

# Sync policy. Missing keys fall back to these defaults, so an older config that
# predates fetch/pull keys keeps working.
ALL_REMOTES="$(cfg fetch.all_remotes)";  [ -n "$ALL_REMOTES" ] || ALL_REMOTES=true
REMOVE_DEAD="$(cfg fetch.remove_dead_remotes)"; [ -n "$REMOVE_DEAD" ] || REMOVE_DEAD=true
PULL_ENABLED="$(cfg pull.enabled)";      [ -n "$PULL_ENABLED" ] || PULL_ENABLED=true
ON_DIVERGED="$(cfg pull.on_diverged)";   [ -n "$ON_DIVERGED" ] || ON_DIVERGED=rebase
ON_CONFLICT="$(cfg pull.on_conflict)";   [ -n "$ON_CONFLICT" ] || ON_CONFLICT=abort-and-report

LOG="$LOG_DIR/$(date +%Y%m%d-%H%M%S).log"
ln -sfn "$LOG" "$LOG_DIR/latest.log"
exec > >(tee -a "$LOG") 2>&1

FAILURES=0
note_error() {
    printf 'ERROR: %s\n' "$1"
    FAILURES=$((FAILURES + 1))
}

# A root that does not exist on this host is a fact about the host, not a sync
# failure - this skill is meant to run anywhere, and a root configured for a
# different host should not turn every run red.
warn_missing_root() {
    printf 'WARN: %s root does not exist on this host, skipped: %s\n' "$1" "$2"
}

# ---------------------------------------------------------------- git roots --
report_git() {
    local root="$1" depth="$2" repo dir
    [ -d "$root" ] || { warn_missing_root git "$root"; return; }

    while IFS= read -r repo; do
        dir="${repo%/.git}"
        printf '\n## git %s\n' "$dir"

        local branch upstream remote owner
        branch="$(git -C "$dir" rev-parse --abbrev-ref HEAD 2>/dev/null)" || {
            note_error "$dir: not a readable git work tree"
            continue
        }
        upstream="$(git -C "$dir" rev-parse --abbrev-ref '@{u}' 2>/dev/null || true)"
        remote="$(git -C "$dir" remote get-url origin 2>/dev/null || true)"
        owner="$(remote_owner "$remote")"

        # Fetch FIRST, so the ahead/behind below describe the remote as it is
        # now, not as of the previous run. A repo without any remote has nothing
        # to fetch. A failure of the upstream's remote is fatal for this repo (its
        # view is stale); a secondary remote whose repository no longer exists is
        # dead weight and gets removed; any other failure is only a WARN.
        local fetched="" pruned="" failed_remotes=" " r err remote_count
        local up_remote="${upstream%%/*}"
        remote_count="$(git -C "$dir" remote 2>/dev/null | wc -l | tr -d ' ')"
        if [ "$remote_count" -eq 0 ]; then
            printf -- '--- no remote: fetch skipped\n'
        else
            while IFS= read -r r; do
                [ -n "$r" ] || continue
                [ "$ALL_REMOTES" = "true" ] || [ "$r" = "origin" ] || continue
                # LC_ALL=C is scoped to this call only: it makes git's error
                # messages English (for the dead-remote match) without breaking
                # `svn up`, which cannot handle non-ASCII names under a C locale.
                if err="$(LC_ALL=C git -C "$dir" fetch --quiet "$r" 2>&1)"; then
                    fetched="${fetched:+$fetched,}$r"
                else
                    failed_remotes="$failed_remotes$r "
                    if [ -n "$up_remote" ] && [ "$r" = "$up_remote" ]; then
                        note_error "$dir: git fetch $r failed (offline, auth, or remote gone?)"
                    elif [ "$REMOVE_DEAD" = "true" ] && [ "$remote_count" -gt 1 ] \
                         && is_dead_remote_error "$err"; then
                        # The repository is gone and this is not the only remote,
                        # so drop the stale config entry. Its (redacted) URL stays
                        # in the log line for recovery.
                        local rurl
                        rurl="$(git -C "$dir" remote get-url "$r" 2>/dev/null || true)"
                        if git -C "$dir" remote remove "$r" 2>/dev/null; then
                            pruned="${pruned:+$pruned,}$r"
                            printf 'WARN: %s: removed dead remote %s (<%s>)\n' \
                                "$dir" "$r" "$(redact "$rurl")"
                        else
                            printf 'WARN: %s: git fetch %s failed - repository gone (remote could not be removed)\n' "$dir" "$r"
                        fi
                    else
                        printf 'WARN: %s: git fetch %s failed (offline, auth, or remote gone?)\n' "$dir" "$r"
                    fi
                fi
            done < <(git -C "$dir" remote 2>/dev/null)
        fi

        local ahead behind dirty
        ahead=0
        behind=0
        if [ -n "$upstream" ]; then
            ahead="$(git -C "$dir" rev-list --count "$upstream".."HEAD" 2>/dev/null || echo 0)"
            behind="$(git -C "$dir" rev-list --count "HEAD".."$upstream" 2>/dev/null || echo 0)"
        fi
        dirty="$(git -C "$dir" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"

        # Catch the checked-out branch up to its upstream, cleanly: fast-forward
        # when only behind, rebase the local-only commits when diverged. Anything
        # not cleanly resolvable (dirty tree, conflicts) is left untouched.
        local pull="uptodate" diverged="false"
        if [ -z "$upstream" ]; then
            pull="skipped(no-upstream)"
        elif [ "$PULL_ENABLED" != "true" ]; then
            pull="disabled"
        elif [[ "$failed_remotes" == *" $up_remote "* ]]; then
            pull="skipped(stale-view)"
        elif [ "$ahead" -gt 0 ] && [ "$behind" -gt 0 ]; then
            diverged="true"
            if [ "$dirty" -gt 0 ]; then
                pull="skipped(dirty)"
            elif [ "$ON_DIVERGED" != "rebase" ]; then
                pull="skipped(diverged)"
            elif git -C "$dir" rebase "$upstream" >/dev/null 2>&1; then
                pull="rebase($behind)"
                ahead="$(git -C "$dir" rev-list --count "$upstream".."HEAD" 2>/dev/null || echo 0)"
                behind="$(git -C "$dir" rev-list --count "HEAD".."$upstream" 2>/dev/null || echo 0)"
            else
                if [ "$ON_CONFLICT" = "abort-and-report" ]; then
                    git -C "$dir" rebase --abort >/dev/null 2>&1 || true
                fi
                pull="conflict"
                note_error "$dir: rebase onto $upstream conflicted and was left unchanged"
            fi
        elif [ "$behind" -gt 0 ]; then
            if [ "$dirty" -gt 0 ]; then
                pull="skipped(dirty)"
            elif git -C "$dir" merge --ff-only "$upstream" >/dev/null 2>&1; then
                pull="ff($behind)"
                behind="$(git -C "$dir" rev-list --count "HEAD".."$upstream" 2>/dev/null || echo 0)"
            else
                pull="failed"
                note_error "$dir: fast-forward to $upstream failed"
            fi
        fi

        printf 'owner=%s\n' "$owner"
        printf 'branch=%s\n' "$branch"
        printf 'upstream=%s\n' "$upstream"
        printf 'ahead=%s\n' "$ahead"
        printf 'behind=%s\n' "$behind"
        printf 'diverged=%s\n' "$diverged"
        printf 'dirty=%s\n' "$dirty"
        printf 'fetched=%s\n' "$fetched"
        printf 'pruned=%s\n' "$pruned"
        printf 'pull=%s\n' "$pull"
        printf 'remote=%s\n' "$(redact "$remote")"

        if [ "$dirty" -gt 0 ]; then
            printf -- '--- status ---\n'
            git -C "$dir" status --porcelain 2>/dev/null || note_error "$dir: git status failed"
        fi
    done < <(find "$root" -maxdepth "$depth" -type d -name .git 2>/dev/null | sort)
}

# ---------------------------------------------------------------- svn roots --
report_svn() {
    local root="$1" depth="$2" wc
    [ -d "$root" ] || { warn_missing_root svn "$root"; return; }

    while IFS= read -r wc; do
        printf '\n## svn %s\n' "$wc"

        local url modified unversioned
        url="$(svn info "$wc" 2>/dev/null | sed -n 's/^URL: //p' | head -1)"
        if ! svn up "$wc" >/dev/null 2>&1; then
            note_error "$wc: svn up failed"
        fi
        # svn status line 1: '?' = unversioned, '!' = missing, else a real change.
        modified="$(cd "$wc" && svn status 2>/dev/null | grep -vc '^?')"
        unversioned="$(cd "$wc" && svn status 2>/dev/null | grep -c '^?')"

        printf 'url=%s\n' "$(redact "$url")"
        printf 'modified=%s\n' "$modified"
        printf 'unversioned=%s\n' "$unversioned"

        if [ "$modified" -gt 0 ] || [ "$unversioned" -gt 0 ]; then
            printf -- '--- status ---\n'
            (cd "$wc" && svn status 2>/dev/null)
        fi
    done < <(find "$root" -maxdepth "$depth" -type d -name .svn 2>/dev/null | sort | sed 's#/\.svn$##')
}

# --------------------------------------------------------------------- main --
printf 'repo-sync report (config: %s)\n' "$CONFIG"
printf 'log: %s\n' "$LOG"

while IFS=$'\t' read -r rtype rpath rdepth; do
    [ -n "${rtype:-}" ] || continue
    rpath="$(expand "$rpath")"
    rdepth="${rdepth:-1}"
    printf '\n== root %s: %s (max_depth %s)\n' "$rtype" "$rpath" "$rdepth"
    case "$rtype" in
        git) report_git "$rpath" "$rdepth" ;;
        svn) report_svn "$rpath" "$rdepth" ;;
        *)   note_error "unknown root type '$rtype'" ;;
    esac
done < <(cfg roots)

printf '\n== summary ==\n'
printf 'failures=%s\n' "$FAILURES"
[ "$FAILURES" -eq 0 ] || exit 1

# --------------------------------------------------------- optional host steps --
# Off by default. A service restart ends the calling opencode session, so it is
# only ever reached when explicitly enabled AND every sync step succeeded.
if [ "$(cfg host_steps.opencode_upgrade)" = "true" ]; then
    printf '\n==> opencode upgrade\n'
    OPENCODE="$HOME/.opencode/bin/opencode"
    if [ -x "$OPENCODE" ]; then
        "$OPENCODE" upgrade || note_error "opencode upgrade failed"
    else
        note_error "$OPENCODE not found or not executable"
    fi
fi

if [ "$(cfg host_steps.restart_service)" = "true" ]; then
    printf '\n==> restarting opencode.service (this ends the current opencode session)\n'
    systemctl --user restart opencode.service || note_error "service restart failed"
fi

[ "$FAILURES" -eq 0 ] || exit 1
exit 0
