#!/usr/bin/env bash
# Self-test for skills/knowledge-persistence/scripts/okf-check.
# Covers the seven acceptance cases from opencode-helpers#141 plus the
# --rules project-rules case and the --allow-missing LOCAL.md amendment. Runs entirely in tmpdir fixtures; stdlib-only
# checker, so it also runs under python3 -I.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECKER="$SCRIPT_DIR/okf-check"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
fails=0
t0=$SECONDS

# assert_exit <expected-exit> <expected-substring> <cmd...>
assert() {
    local want_exit="$1" want_sub="$2"
    shift 2
    local out rc
    out="$("$@" 2>&1)"
    rc=$?
    if [ "$rc" != "$want_exit" ]; then
        echo "FAIL: exit $rc != $want_exit: $*"
        echo "$out"
        fails=$((fails + 1))
        return
    fi
    if ! grep -qF -- "$want_sub" <<<"$out"; then
        echo "FAIL: output missing '$want_sub': $*"
        echo "$out"
        fails=$((fails + 1))
        return
    fi
    echo "ok: case '$want_sub' (exit $rc)"
}

# ---------------------------------------------------------------- fixtures
# Case 1: concept file without frontmatter
mkdir -p "$TMP/c1"
printf '# Just a heading\n\nBody text.\n' > "$TMP/c1/nofm.md"

# Case 2: frontmatter with empty type
mkdir -p "$TMP/c2"
printf -- '---\ntype: ""\ntitle: x\n---\n\nBody.\n' > "$TMP/c2/empty-type.md"

# Case 3: bundle-root index.md without okf_version (no extra keys either)
mkdir -p "$TMP/c3"
printf '# Bundle index\n\n- [a](a.md)\n' > "$TMP/c3/index.md"
printf -- '---\ntype: overview\ntitle: a\n---\n\nBody.\n' > "$TMP/c3/a.md"
# Case 3b (contrast): index.md with extra frontmatter keys must fail
mkdir -p "$TMP/c3b"
printf -- '---\ntitle: bundle\n---\n\n# Bundle index\n' > "$TMP/c3b/index.md"
printf -- '---\ntype: overview\ntitle: a\n---\n\nBody.\n' > "$TMP/c3b/a.md"

# Case 4: log.md with frontmatter
mkdir -p "$TMP/c4"
printf -- '---\ntype: log\n---\n\n## 2026-11-26\n\nEntry.\n' > "$TMP/c4/log.md"
printf -- '---\ntype: overview\ntitle: a\n---\n\nBody.\n' > "$TMP/c4/a.md"

# Case 5: broken link
mkdir -p "$TMP/c5"
printf -- '---\ntype: overview\ntitle: a\n---\n\nSee [missing](nope.md).\n' \
    > "$TMP/c5/a.md"

# Case 6: --preserve-from with a lost line (exit 4)
mkdir -p "$TMP/c6/old" "$TMP/c6/new"
printf -- '---\ntype: overview\ntitle: a\n---\n\nFirst line.\n' \
    > "$TMP/c6/old/a.md"
printf -- '---\ntype: overview\ntitle: a\n---\n\nOther line.\n' \
    > "$TMP/c6/new/a.md"

# Case 7: host lint on/off. Bundle WITHOUT hosts/ dir but with a
# host-tagged bullet; --hosts enables the lint, --no-placement-lint or no
# --hosts skips it. Bundle WITH hosts/<host>/ derives the host itself.
mkdir -p "$TMP/c7"
printf -- '---\ntype: overview\ntitle: a\n---\n\n- [think] something hosty\n' \
    > "$TMP/c7/a.md"
mkdir -p "$TMP/c7b/hosts/elite"
printf -- '---\ntype: overview\ntitle: a\n---\n\n- [elite] something hosty\n' \
    > "$TMP/c7b/a.md"

# Case 8 (--rules): project-specific required frontmatter keys per type
mkdir -p "$TMP/c8"
printf -- '---\ntype: Foliensatz\ntitle: f\n---\n\nBody.\n' \
    > "$TMP/c8/f1.md"
printf '{"Foliensatz": ["title", "quellen", "pdf_seiten"]}' \
    > "$TMP/c8/rules.json"

# Case 9 (--allow-missing): gitignored local-only files (e.g. LOCAL.md).
# (a) index.md links a missing LOCAL.md without the flag -> broken-link
# error; (b) with --allow-missing LOCAL.md -> LOCAL: info line, exit 0;
# (c) --allow-missing for a file that DOES exist -> checked normally.
mkdir -p "$TMP/c9"
printf -- '---\nokf_version: "0.2"\n---\n\n# Bundle index\n\n- [a](a.md)\n- [local](LOCAL.md)\n' \
    > "$TMP/c9/index.md"
printf -- '---\ntype: overview\ntitle: a\n---\n\nBody.\n' > "$TMP/c9/a.md"

# ------------------------------------------------------------------- cases
# 1: missing frontmatter -> conformance error
assert 1 "nofm.md: missing frontmatter block" \
    python3 -I "$CHECKER" --root "$TMP/c1"

# 2: empty type -> conformance error
assert 1 "empty-type.md: frontmatter has no non-empty type" \
    python3 -I "$CHECKER" --root "$TMP/c2"

# 3: index.md without okf_version (and without extra keys) is allowed
#    (OKF-SPEC.md §8: a bundle-root index.md MAY carry okf_version)
assert 0 "OK: 1 concept(s)" \
    python3 -I "$CHECKER" --root "$TMP/c3"
# 3b: index.md with frontmatter other than okf_version -> error
assert 1 "index.md may only carry okf_version, found title" \
    python3 -I "$CHECKER" --root "$TMP/c3b"

# 4: log.md with frontmatter -> error
assert 1 "log.md must not carry frontmatter" \
    python3 -I "$CHECKER" --root "$TMP/c4"

# 5: broken link -> error
assert 1 "broken link nope.md" \
    python3 -I "$CHECKER" --root "$TMP/c5"

# 6: lost line -> exit 4
assert 4 "LOST: 1 of 5 non-empty lines no longer present" \
    python3 -I "$CHECKER" --root "$TMP/c6/new" \
    --preserve-from "$TMP/c6/old"

# 7a: no hosts/ dir and no --hosts -> lint skipped with warning, exit 0
assert 0 "no hosts/ directory in bundle and no --hosts: placement lint skipped" \
    python3 -I "$CHECKER" --root "$TMP/c7"
# 7b: --hosts override -> lint active, host bullet warned
assert 0 "a.md:6 looks host-specific" \
    python3 -I "$CHECKER" --root "$TMP/c7" --hosts think
# 7c: --no-placement-lint -> no warning even with --hosts
out="$(python3 -I "$CHECKER" --root "$TMP/c7" --hosts think --no-placement-lint 2>&1)"
if grep -q "host-specific" <<<"$out"; then
    echo "FAIL: --no-placement-lint still warned"
    fails=$((fails + 1))
else
    echo "ok: case '--no-placement-lint silences host lint'"
fi
# 7d: hosts/ dir present -> host derived from it, lint active
assert 0 "a.md:6 looks host-specific" \
    python3 -I "$CHECKER" --root "$TMP/c7b"

# 8: --rules requires the listed keys for that type -> error; supplied -> ok
assert 1 "type 'Foliensatz' requires frontmatter key 'quellen'" \
    python3 -I "$CHECKER" --root "$TMP/c8" --rules "$TMP/c8/rules.json"
printf -- '---\ntype: Foliensatz\ntitle: f\nquellen:\n  - a\npdf_seiten: 3\n---\n\nBody.\n' \
    > "$TMP/c8/f1.md"
assert 0 "OK: 1 concept(s)" \
    python3 -I "$CHECKER" --root "$TMP/c8" --rules "$TMP/c8/rules.json"

# 9a: missing LOCAL.md link without --allow-missing -> broken-link error
assert 1 "index.md: broken link LOCAL.md" \
    python3 -I "$CHECKER" --root "$TMP/c9"
# 9b: with --allow-missing LOCAL.md -> info line instead of error, exit 0
assert 0 "index.md: link to local-only file: LOCAL.md" \
    python3 -I "$CHECKER" --root "$TMP/c9" --allow-missing LOCAL.md
# 9b': the flag is repeatable and comma-separated
assert 0 "link to local-only file: LOCAL.md" \
    python3 -I "$CHECKER" --root "$TMP/c9" \
    --allow-missing OTHER.md --allow-missing "LOCAL.md,ALSO.md"
# 9c: --allow-missing for a file that exists -> checked normally
printf 'local-only.\n' > "$TMP/c9/LOCAL.md"
out="$(python3 -I "$CHECKER" --root "$TMP/c9" --allow-missing LOCAL.md 2>&1)"
if grep -q "local-only file" <<<"$out"; then
    echo "FAIL: --allow-missing downgraded an existing file"
    fails=$((fails + 1))
else
    echo "ok: case '--allow-missing with existing file checked normally'"
fi
rm "$TMP/c9/LOCAL.md"

# ------------------------------------------------------------------ result
elapsed=$((SECONDS - t0))
if [ "$fails" -ne 0 ]; then
    echo "FAILED: $fails assertion(s), ${elapsed}s"
    exit 1
fi
echo "PASS: all cases, ${elapsed}s"
