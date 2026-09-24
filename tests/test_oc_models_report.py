"""Hermetic tests for scripts/oc-models-report.

A fake `opencode` executable (temp shell script) emits a fixed two-model dump
and logs each invocation, so no run ever touches the network or the live
opencode installation. The cache dir, max age and collect command are steered
via OC_MODELS_REPORT_* environment variables.
"""

import contextlib
import importlib.machinery
import importlib.util
import io
import os
import stat
import tempfile
import time
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "oc-models-report")

DUMP = """\
fake/free-model
{
  "id": "free-model",
  "providerID": "fake",
  "name": "Free Model",
  "family": "free",
  "cost": {"input": 0, "output": 0},
  "limit": {"context": 128000},
  "capabilities": {"reasoning": true, "toolcall": true, "temperature": true,
                   "attachment": false,
                   "input": {"text": true}, "output": {"text": true}}
}
fake/paid-model
{
  "id": "paid-model",
  "providerID": "fake",
  "name": "Paid Model",
  "family": "paid",
  "cost": {"input": 3, "output": 9.5},
  "limit": {"context": 1000000},
  "capabilities": {"reasoning": false, "toolcall": true, "temperature": false,
                   "attachment": true,
                   "input": {"text": true, "image": true},
                   "output": {"text": true}}
}
"""

MULTI_DUMP = """\
alpha/alpha-one
{
  "id": "alpha-one",
  "providerID": "alpha",
  "name": "Alpha One",
  "family": "one",
  "cost": {"input": 1, "output": 2},
  "limit": {"context": 128000},
  "capabilities": {"reasoning": true, "toolcall": true, "temperature": true,
                   "attachment": false,
                   "input": {"text": true}, "output": {"text": true}}
}
alpha/alpha-two
{
  "id": "alpha-two",
  "providerID": "alpha",
  "name": "Alpha Two",
  "family": "two",
  "cost": {"input": 0, "output": 0},
  "limit": {"context": 32000},
  "capabilities": {"reasoning": false, "toolcall": true, "temperature": true,
                   "attachment": false,
                   "input": {"text": true}, "output": {"text": true}}
}
beta/beta-one
{
  "id": "beta-one",
  "providerID": "beta",
  "name": "Beta One",
  "family": "one",
  "cost": {"input": 5, "output": 10},
  "limit": {"context": 200000},
  "capabilities": {"reasoning": true, "toolcall": false, "temperature": false,
                   "attachment": true,
                   "input": {"text": true, "image": true},
                   "output": {"text": true}}
}
"""


def load_script():
    loader = importlib.machinery.SourceFileLoader("oc_models_report", SCRIPT)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


mod = load_script()


def make_fake(tmp, succeed=True, name="fake-opencode"):
    """Create a fake collect command; return (cmd, invocations_log)."""
    log = os.path.join(tmp, name + ".log")
    fake = os.path.join(tmp, name)
    with open(fake, "w") as fh:
        fh.write("#!/bin/sh\n")
        fh.write(f"echo invoked >> {log}\n")
        if succeed:
            fh.write("cat <<'EOF'\n" + DUMP + "EOF\n")
        else:
            fh.write("echo 'boom: fake failure' >&2\n")
            fh.write("exit 1\n")
    os.chmod(fake, os.stat(fake).st_mode | stat.S_IXUSR)
    return fake, log


def invocations(log):
    if not os.path.isfile(log):
        return 0
    with open(log) as fh:
        return sum(1 for line in fh if line.strip())


class OcModelsReportTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cachedir = os.path.join(self.tmp.name, "cache")
        self.cachefile = os.path.join(self.cachedir, "models-verbose.txt")

    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                rc = mod.main(argv)
            except SystemExit as exc:
                rc = exc.code
        return rc, out.getvalue(), err.getvalue()

    def env(self, cmd, **extra):
        e = {
            "OC_MODELS_REPORT_CACHE_DIR": self.cachedir,
            "OC_MODELS_REPORT_CMD": cmd,
            "OC_MODELS_REPORT_MAX_AGE": str(12 * 3600),
        }
        e.update(extra)
        return mock.patch.dict(os.environ, e, clear=False)

    def test_missing_cache_generates(self):
        fake, log = make_fake(self.tmp.name)
        with self.env(fake):
            rc, out, _ = self.run_main(["free"])
        self.assertEqual(rc, 0)
        self.assertEqual(invocations(log), 1)
        self.assertTrue(os.path.isfile(self.cachefile))
        with open(self.cachefile) as fh:
            self.assertEqual(fh.read(), DUMP)
        self.assertIn("collected info of 2 models", out)
        self.assertIn("fake/free-model", out)
        self.assertIn("free", out)
        self.assertIn("128k", out)
        self.assertNotIn("paid-model", out)
        self.assertIn("1 match(es) for: free", out)

    def test_fresh_cache_skips_collect(self):
        fake, log = make_fake(self.tmp.name)
        with self.env(fake):
            self.run_main(["paid"])
            rc, out, _ = self.run_main(["paid"])
        self.assertEqual(rc, 0)
        self.assertEqual(invocations(log), 1)
        self.assertNotIn("collected info", out)
        self.assertIn("fake/paid-model", out)
        self.assertIn("3/9.5", out)
        self.assertIn("1m", out)

    def test_stale_cache_regenerates(self):
        fake, log = make_fake(self.tmp.name)
        with self.env(fake):
            self.run_main(["free"])
            stale = time.time() - 13 * 3600
            os.utime(self.cachefile, (stale, stale))
            rc, out, _ = self.run_main(["free"])
        self.assertEqual(rc, 0)
        self.assertEqual(invocations(log), 2)
        self.assertIn("collected info of 2 models", out)

    def test_refresh_flag_forces_regen(self):
        fake, log = make_fake(self.tmp.name)
        with self.env(fake):
            self.run_main(["free"])
            rc, out, _ = self.run_main(["--refresh", "free"])
        self.assertEqual(rc, 0)
        self.assertEqual(invocations(log), 2)
        self.assertIn("collected info of 2 models", out)

    def test_file_bypasses_cache(self):
        fake, log = make_fake(self.tmp.name)
        dump = os.path.join(self.tmp.name, "custom.txt")
        with open(dump, "w") as fh:
            fh.write(DUMP)
        with self.env(fake):
            rc, out, _ = self.run_main(["--file", dump, "paid"])
        self.assertEqual(rc, 0)
        self.assertEqual(invocations(log), 0)
        self.assertFalse(os.path.isfile(self.cachefile))
        self.assertNotIn("collected info", out)
        self.assertIn("fake/paid-model", out)

    def test_failed_regen_falls_back_to_stale(self):
        good, log = make_fake(self.tmp.name)
        with self.env(good):
            self.run_main(["free"])
        bad, _ = make_fake(self.tmp.name, succeed=False,
                           name="fake-opencode-bad")
        stale = time.time() - 13 * 3600
        os.utime(self.cachefile, (stale, stale))
        with self.env(bad):
            rc, out, err = self.run_main(["free"])
        self.assertEqual(rc, 0)
        self.assertIn("warning:", err)
        self.assertIn("fake/free-model", out)
        self.assertNotIn("collected info", out)

    def test_failed_regen_without_cache_exits_2(self):
        bad, _ = make_fake(self.tmp.name, succeed=False)
        with self.env(bad):
            rc, out, err = self.run_main(["free"])
        self.assertEqual(rc, 2)
        self.assertIn("error:", err)
        self.assertEqual(out, "")

    def test_no_match_exits_1(self):
        fake, _ = make_fake(self.tmp.name)
        with self.env(fake):
            rc, out, err = self.run_main(["nosuchmodel"])
        self.assertEqual(rc, 1)
        self.assertIn("no models match", err)

    def write_dump(self, content, name="multi.txt"):
        path = os.path.join(self.tmp.name, name)
        with open(path, "w") as fh:
            fh.write(content)
        return path

    def test_provider_only_lists_all_of_provider(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "--provider", "alpha"])
        self.assertEqual(rc, 0)
        self.assertIn("alpha/alpha-one", out)
        self.assertIn("alpha/alpha-two", out)
        self.assertNotIn("beta/beta-one", out)
        self.assertIn("2 match(es) for: provider alpha", out)

    def test_provider_plus_filter_intersects(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "--provider", "alpha", "two"])
        self.assertEqual(rc, 0)
        self.assertIn("alpha/alpha-two", out)
        self.assertNotIn("alpha/alpha-one", out)
        self.assertNotIn("beta/beta-one", out)
        self.assertIn("1 match(es) for: two (provider alpha)", out)

    def test_provider_is_case_insensitive(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "--provider", "ALPHA"])
        self.assertEqual(rc, 0)
        self.assertIn("alpha/alpha-one", out)
        self.assertIn("2 match(es) for: provider ALPHA", out)

    def test_provider_must_match_exactly(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, err = self.run_main(["--file", dump, "--provider", "alph"])
        self.assertEqual(rc, 2)
        self.assertIn("unknown provider: alph", err)
        self.assertEqual(out, "")

    def test_unknown_provider_exits_2(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, err = self.run_main(["--file", dump, "--provider", "gamma"])
        self.assertEqual(rc, 2)
        self.assertIn("unknown provider: gamma", err)
        self.assertEqual(out, "")

    def test_provider_filter_no_match_exits_1(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, err = self.run_main(["--file", dump, "--provider", "alpha", "zzz"])
        self.assertEqual(rc, 1)
        self.assertIn("no models match: zzz (provider alpha)", err)
        self.assertEqual(out, "")

    def test_neither_provider_nor_filter_exits_2(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, err = self.run_main(["--file", dump])
        self.assertEqual(rc, 2)
        self.assertIn("at least one substring or --provider", err)
        self.assertEqual(out, "")

    def test_filter_matches_free_cost(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "free"])
        self.assertEqual(rc, 0)
        self.assertIn("alpha/alpha-two", out)
        self.assertNotIn("alpha/alpha-one", out)
        self.assertNotIn("beta/beta-one", out)
        self.assertIn("1 match(es) for: free", out)

    def test_filter_matches_free_cost_within_provider(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "--provider", "alpha", "free"])
        self.assertEqual(rc, 0)
        self.assertIn("alpha/alpha-two", out)
        self.assertNotIn("alpha/alpha-one", out)
        self.assertNotIn("beta/beta-one", out)
        self.assertIn("1 match(es) for: free (provider alpha)", out)


if __name__ == "__main__":
    unittest.main()
