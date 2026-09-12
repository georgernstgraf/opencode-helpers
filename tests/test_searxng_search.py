"""Hermetic tests for skills/searxng/searxng-search.sh.

The real script is copied to a temp file whose instance chain points at a local
mock server, so these tests never touch the network or the live instance.
"""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import searxng_mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "searxng" / "searxng-search.sh"


class SearxngSearchTest(unittest.TestCase):
    def _mock(self, **kwargs):
        mock = searxng_mock.MockSearxng(**kwargs).start()
        self.addCleanup(mock.stop)
        return mock

    def _script_for(self, *urls):
        patched = searxng_mock.patch_script_instances(SCRIPT.read_text(), list(urls))
        handle = tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False)
        handle.write(patched)
        handle.close()
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return handle.name

    def _run(self, script, *args):
        proc = subprocess.run(
            ["bash", script, *args], capture_output=True, text=True, timeout=60
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout)

    def test_weak_results_trigger_fallback_and_merge(self):
        mock = self._mock()
        script = self._script_for(mock.url)

        out = self._run(script, "weakcase")

        self.assertTrue(out["fallback_used"])
        self.assertEqual(out["fallback_reason"], "weak")
        # Primary results first, Brave appended, duplicate URL collapsed.
        self.assertEqual(
            [r["url"] for r in out["results"]],
            ["https://example.com/a", "https://example.com/b", "https://example.com/new"],
        )
        self.assertEqual({r["engine"] for r in out["results"]}, {"mwmbl", "braveapi"})
        self.assertEqual(len(mock.requests), 2)
        self.assertEqual(mock.requests[0]["engines"], "")
        self.assertEqual(mock.requests[1]["engines"], "braveapi")

    def test_empty_results_trigger_fallback(self):
        mock = self._mock()
        script = self._script_for(mock.url)

        out = self._run(script, "emptycase")

        self.assertTrue(out["fallback_used"])
        self.assertEqual(out["fallback_reason"], "empty")
        self.assertEqual(
            [r["url"] for r in out["results"]],
            ["https://example.com/a", "https://example.com/new"],
        )
        self.assertEqual({r["engine"] for r in out["results"]}, {"braveapi"})

    def test_google_results_skip_fallback(self):
        mock = self._mock()
        script = self._script_for(mock.url)

        out = self._run(script, "googlecase")

        self.assertFalse(out["fallback_used"])
        self.assertNotIn("fallback_reason", out)
        self.assertEqual(len(out["results"]), 3)
        self.assertEqual({r["engine"] for r in out["results"]}, {"google"})
        self.assertEqual(len(mock.requests), 1)

    def test_single_google_result_skips_fallback(self):
        mock = self._mock()
        script = self._script_for(mock.url)

        out = self._run(script, "onegoogle")

        self.assertFalse(out["fallback_used"])
        self.assertEqual(len(out["results"]), 1)
        self.assertEqual(len(mock.requests), 1)

    def test_explicit_engines_bypass_fallback_and_category(self):
        mock = self._mock()
        script = self._script_for(mock.url)

        out = self._run(script, "weakcase", "en", "1", "general", "wikipedia")

        self.assertFalse(out["fallback_used"])
        self.assertEqual(len(mock.requests), 1)
        self.assertEqual(mock.requests[0]["engines"], "wikipedia")
        # Search engines override the category - it must not be sent alongside.
        self.assertEqual(mock.requests[0]["categories"], "")

    def test_non_general_category_skips_fallback(self):
        mock = self._mock()
        script = self._script_for(mock.url)

        out = self._run(script, "weakcase", "en", "1", "news")

        self.assertFalse(out["fallback_used"])
        self.assertEqual(len(mock.requests), 1)
        self.assertEqual(mock.requests[0]["categories"], "news")

    def test_fallback_preserves_time_range_safesearch_language(self):
        mock = self._mock()
        script = self._script_for(mock.url)

        out = self._run(script, "weakcase", "de", "1", "general", "", "week", "1")

        self.assertTrue(out["fallback_used"])
        self.assertEqual(len(mock.requests), 2)
        for req in mock.requests:
            self.assertEqual(req["time_range"], "week")
            self.assertEqual(req["safesearch"], "1")
            self.assertEqual(req["language"], "de")

    def test_instance_chain_falls_through_on_broken_empty(self):
        broken = self._mock(scenarios={"chaincase": []}, unresponsive=["google"])
        healthy = self._mock(
            scenarios={
                "chaincase": [searxng_mock.result_item("Google 1", "https://g.com/1", "google")]
            }
        )
        script = self._script_for(broken.url, healthy.url)

        out = self._run(script, "chaincase")

        self.assertEqual(out["instance"], healthy.url)
        self.assertFalse(out["fallback_used"])
        self.assertEqual(len(broken.requests), 1)
        self.assertEqual(len(healthy.requests), 1)

    def test_fallback_uses_primary_instance_only(self):
        primary = self._mock()
        secondary = self._mock()
        script = self._script_for(primary.url, secondary.url)

        out = self._run(script, "weakcase")

        self.assertTrue(out["fallback_used"])
        self.assertEqual(out["instance"], primary.url)
        self.assertEqual(len(primary.requests), 2)
        self.assertEqual(len(secondary.requests), 0)


if __name__ == "__main__":
    unittest.main()
