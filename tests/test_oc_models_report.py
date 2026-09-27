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

    def order(self, out):
        return [line.split()[0] for line in out.splitlines()
                if line.startswith(("alpha/", "beta/"))]

    def test_default_sort_is_model_id(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "a"])
        self.assertEqual(rc, 0)
        self.assertEqual(
            self.order(out),
            ["alpha/alpha-one", "alpha/alpha-two", "beta/beta-one"],
        )

    def test_sort_by_input_price(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "a", "--sort", "in"])
        self.assertEqual(rc, 0)
        self.assertEqual(
            self.order(out),
            ["alpha/alpha-two", "alpha/alpha-one", "beta/beta-one"],
        )

    def test_sort_by_output_price(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "a", "--sort", "out"])
        self.assertEqual(rc, 0)
        self.assertEqual(
            self.order(out),
            ["alpha/alpha-two", "alpha/alpha-one", "beta/beta-one"],
        )

    def test_sort_by_total_cost(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "a", "--sort", "cost"])
        self.assertEqual(rc, 0)
        self.assertEqual(
            self.order(out),
            ["alpha/alpha-two", "alpha/alpha-one", "beta/beta-one"],
        )

    def test_sort_cost_aliases(self):
        dump = self.write_dump(MULTI_DUMP)
        expected = ["alpha/alpha-two", "alpha/alpha-one", "beta/beta-one"]
        for alias in ("$", "mtok", "price"):
            rc, out, _ = self.run_main(["--file", dump, "a", "--sort", alias])
            self.assertEqual(rc, 0, alias)
            self.assertEqual(self.order(out), expected, alias)

    def test_sort_by_context(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "a", "--sort", "ctx"])
        self.assertEqual(rc, 0)
        self.assertEqual(
            self.order(out),
            ["alpha/alpha-two", "alpha/alpha-one", "beta/beta-one"],
        )

    def test_sort_by_provider(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "a", "--sort", "provider"])
        self.assertEqual(rc, 0)
        self.assertEqual(
            self.order(out),
            ["alpha/alpha-one", "alpha/alpha-two", "beta/beta-one"],
        )

    def test_reverse_flips_active_key(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, _ = self.run_main(["--file", dump, "a", "--sort", "ctx", "-r"])
        self.assertEqual(rc, 0)
        self.assertEqual(
            self.order(out),
            ["beta/beta-one", "alpha/alpha-one", "alpha/alpha-two"],
        )

    def test_sort_invalid_key_exits_2(self):
        dump = self.write_dump(MULTI_DUMP)
        rc, out, err = self.run_main(["--file", dump, "a", "--sort", "bogus"])
        self.assertEqual(rc, 2)
        self.assertIn("invalid --sort key: bogus", err)
        self.assertEqual(out, "")


PARAMS_JSON = """\
{
  "aliases": {"alpha-one": "alpha-1"},
  "models": {
    "alpha-1": {"total": 7},
    "alpha-two": {"total": 0.65, "estimated": true},
    "beta-one": {"total": 2400, "active": 95, "source": "https://example.com/beta"}
  }
}
"""


class OcModelsReportParamsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dump = self.write("multi.txt", MULTI_DUMP)
        self.params = self.write("params.json", PARAMS_JSON)

    def write(self, name, content):
        path = os.path.join(self.tmp.name, name)
        with open(path, "w") as fh:
            fh.write(content)
        return path

    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                rc = mod.main(argv)
            except SystemExit as exc:
                rc = exc.code
        return rc, out.getvalue(), err.getvalue()

    def order(self, out):
        return [line.split()[0] for line in out.splitlines()
                if line.startswith(("alpha/", "beta/"))]

    def test_params_key_strips_free_and_takes_last_segment(self):
        self.assertEqual(mod.params_key("openrouter/openai/gpt-oss-120b"),
                         "gpt-oss-120b")
        self.assertEqual(mod.params_key("openrouter/x/y:free"), "y")
        self.assertEqual(mod.params_key("ollama/gemma4:12b"), "gemma4:12b")

    def test_lookup_resolves_alias(self):
        params = mod.load_params(self.params)
        self.assertEqual(params[0]["alpha-one"], "alpha-1")
        self.assertEqual(mod.lookup_params(params, "alpha/alpha-one")["total"], 7)

    def test_fmt_params_variants(self):
        self.assertEqual(mod.fmt_params({"total": 70}), "70B")
        self.assertEqual(mod.fmt_params({"total": 0.65}), "650m")
        self.assertEqual(mod.fmt_params({"total": 2400, "active": 95}), "2.4T/95B")
        self.assertEqual(mod.fmt_params({"total": 275, "estimated": True}), "~275B")
        self.assertEqual(mod.fmt_params({"note": "router"}), "–")
        self.assertEqual(mod.fmt_params(None), "–")

    def test_column_shows_counts_and_estimated(self):
        rc, out, _ = self.run_main(["--file", self.dump, "a",
                                    "--params", self.params])
        self.assertEqual(rc, 0)
        self.assertIn("7B", out)
        self.assertIn("~650m", out)
        self.assertIn("2.4T/95B", out)
        self.assertIn("PARAM", out)

    def test_sort_params_ascending_and_unknown_last(self):
        rc, out, _ = self.run_main(["--file", self.dump, "a",
                                    "--params", self.params, "--sort", "params"])
        self.assertEqual(rc, 0)
        self.assertEqual(
            self.order(out),
            ["alpha/alpha-two", "alpha/alpha-one", "beta/beta-one"],
        )

    def test_sort_params_reverse_keeps_unknown_last(self):
        rc, out, _ = self.run_main(["--file", self.dump, "a",
                                    "--params", self.params,
                                    "--sort", "params", "-r"])
        self.assertEqual(rc, 0)
        self.assertEqual(
            self.order(out),
            ["beta/beta-one", "alpha/alpha-one", "alpha/alpha-two"],
        )

    def test_sort_params_unknown_last_only_partial(self):
        partial = self.write("partial.json", '{"models": {"alpha-one": {"total": 7}}}')
        rc, out, _ = self.run_main(["--file", self.dump, "a",
                                    "--params", partial, "--sort", "params"])
        self.assertEqual(rc, 0)
        self.assertEqual(self.order(out)[0], "alpha/alpha-one")
        self.assertEqual(self.order(out)[1:], ["alpha/alpha-two", "beta/beta-one"])

    def test_params_missing_lists_uncovered_keys(self):
        partial = self.write("partial.json", '{"models": {"alpha-one": {"total": 7}}}')
        rc, out, _ = self.run_main(["--file", self.dump, "a",
                                    "--params", partial, "--params-missing"])
        self.assertEqual(rc, 0)
        self.assertNotIn("alpha-one", out)
        self.assertIn("alpha-two", out)
        self.assertIn("beta-one", out)
        self.assertIn("2 missing key(s)", out)

    def test_params_missing_none(self):
        rc, out, _ = self.run_main(["--file", self.dump, "alpha-one",
                                    "--params", self.params, "--params-missing"])
        self.assertEqual(rc, 0)
        self.assertIn("no missing parameter entries", out)

    def test_missing_params_file_is_silent(self):
        rc, out, err = self.run_main(["--file", self.dump, "a",
                                      "--params", os.path.join(self.tmp.name, "nope.json")])
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertIn("–", out)

    def test_malformed_params_file_warns(self):
        bad = self.write("bad.json", "{ not json")
        rc, out, err = self.run_main(["--file", self.dump, "a", "--params", bad])
        self.assertEqual(rc, 0)
        self.assertIn("warning:", err)

    def test_params_env_override(self):
        with mock.patch.dict(os.environ, {"OC_MODELS_REPORT_PARAMS": self.params}):
            rc, out, _ = self.run_main(["--file", self.dump, "alpha-one"])
        self.assertEqual(rc, 0)
        self.assertIn("7B", out)

    def test_params_missing_allows_no_filter(self):
        partial = self.write("partial.json", '{"models": {"alpha-one": {"total": 7}}}')
        rc, out, _ = self.run_main(["--file", self.dump,
                                    "--params", partial, "--params-missing"])
        self.assertEqual(rc, 0)
        self.assertIn("missing key(s)", out)


if __name__ == "__main__":
    unittest.main()
