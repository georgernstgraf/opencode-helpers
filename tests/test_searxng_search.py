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
from searxng_mock import result_item

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "searxng" / "searxng-search.sh"

BRAVE = [result_item("Brave 1", "https://example.com/a", "brave")]
GOOGLE = [
    result_item("Google 1", "https://g.com/1", "google"),
    result_item("Google 2", "https://g.com/2", "google"),
    result_item("Google 3", "https://g.com/3", "google"),
]
FREE_TWO = [
    result_item("Mwmbl 1", "https://example.com/a", "mwmbl"),
    result_item("Mwmbl 2", "https://example.com/b", "mwmbl"),
]
FREE_THREE = FREE_TWO + [result_item("Mwmbl 3", "https://example.com/c", "mwmbl")]
API_RESULTS = [
    result_item("Brave API 1", "https://example.com/new", "braveapi"),
    result_item("Brave API 2", "https://example.com/a", "braveapi"),
]


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
            ["bash", script, *args], capture_output=True, text=True, timeout=90
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout)

    def _run_env(self, script, env_overrides, *args):
        import os

        env = {
            k: v for k, v in os.environ.items() if not k.startswith("SEARXNG_")
        }
        env.update(env_overrides)
        proc = subprocess.run(
            ["bash", script, *args],
            capture_output=True,
            text=True,
            timeout=90,
            env=env,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout)

    # --- Tier 1: brave ------------------------------------------------------
    def test_brave_results_stop_the_chain(self):
        mock = self._mock(engine_results={"brave": BRAVE, "google": GOOGLE})
        script = self._script_for(mock.url)

        out = self._run(script, "bravecase")

        self.assertEqual(out["engine_used"], "brave")
        self.assertFalse(out["fallback_used"])
        self.assertEqual(out["tried"], ["brave"])
        self.assertEqual([r["engine"] for r in out["results"]], ["brave"])
        self.assertEqual(len(mock.requests), 1)
        self.assertEqual(mock.requests[0]["engines"], "brave")

    def test_brave_suspended_falls_back_to_google(self):
        mock = self._mock(engine_results={"google": GOOGLE}, unresponsive=["brave"])
        script = self._script_for(mock.url)

        out = self._run(script, "suspendcase")

        self.assertEqual(out["engine_used"], "google")
        self.assertTrue(out["fallback_used"])
        self.assertEqual(out["tried"], ["brave", "google"])
        self.assertEqual({r["engine"] for r in out["results"]}, {"google"})
        self.assertEqual([r["engines"] for r in mock.requests], ["brave", "google"])
        self.assertEqual(out["unresponsive_engines"], [["brave", "Suspended: test"]])

    def test_brave_empty_falls_back_to_google(self):
        mock = self._mock(engine_results={"google": GOOGLE})
        script = self._script_for(mock.url)

        out = self._run(script, "emptybravecase")

        self.assertEqual(out["engine_used"], "google")
        self.assertEqual(len(mock.requests), 2)

    # --- Tier 3/4: free last resort and the token gate ----------------------
    def test_three_free_results_suppress_braveapi(self):
        mock = self._mock(engine_results={"mwmbl": FREE_THREE, "braveapi": API_RESULTS})
        script = self._script_for(mock.url)

        out = self._run(script, "freecase")

        self.assertEqual(out["engine_used"], "mwmbl")
        self.assertTrue(out["fallback_used"])
        self.assertEqual(out["tried"], ["brave", "google", "mwmbl", "searchmysite"])
        self.assertEqual(len(out["results"]), 3)
        # No braveapi request was made (token conserved).
        self.assertNotIn("braveapi", [r["engines"] for r in mock.requests])
        self.assertEqual(len(mock.requests), 3)

    def test_weak_free_result_triggers_braveapi_and_merges(self):
        mock = self._mock(
            engine_results={"mwmbl": FREE_TWO, "braveapi": API_RESULTS}
        )
        script = self._script_for(mock.url)

        out = self._run(script, "weakcase")

        self.assertEqual(out["engine_used"], "braveapi")
        self.assertTrue(out["fallback_used"])
        self.assertEqual(
            out["tried"], ["brave", "google", "mwmbl", "searchmysite", "braveapi"]
        )
        # Brave API first, then the free results, duplicate URL collapsed.
        self.assertEqual(
            [r["url"] for r in out["results"]],
            [
                "https://example.com/new",
                "https://example.com/a",
                "https://example.com/b",
            ],
        )
        self.assertEqual({r["engine"] for r in out["results"]}, {"braveapi", "mwmbl"})
        self.assertEqual(mock.requests[-1]["engines"], "braveapi")
        self.assertEqual(len(mock.requests), 4)

    def test_braveapi_failure_emits_free_result(self):
        mock = self._mock(
            engine_results={"mwmbl": FREE_TWO}, unresponsive=["braveapi"]
        )
        script = self._script_for(mock.url)

        out = self._run(script, "apifailcase")

        self.assertEqual(out["engine_used"], "mwmbl")
        self.assertTrue(out["fallback_used"])
        self.assertEqual(len(out["results"]), 2)
        self.assertIn("braveapi", out["tried"])
        self.assertIn(["braveapi", "Suspended: test"], out["unresponsive_engines"])

    def test_all_empty_uses_none(self):
        mock = self._mock()
        script = self._script_for(mock.url)

        out = self._run(script, "nothingcase")

        self.assertEqual(out["engine_used"], "none")
        self.assertEqual(out["results"], [])
        self.assertEqual(
            out["tried"], ["brave", "google", "mwmbl", "searchmysite", "braveapi"]
        )
        self.assertEqual(len(mock.requests), 4)

    def test_broken_free_tier_response_is_normalized(self):
        # The free tier answers with a non-JSON body (timeout/error): the script
        # must not crash and must still be able to escalate to braveapi.
        mock = self._mock(
            engine_results={"braveapi": API_RESULTS},
            unresponsive=["brave", "google"],
            broken_engines=["mwmbl", "searchmysite"],
        )
        script = self._script_for(mock.url)

        out = self._run(script, "brokenfreecase")

        self.assertEqual(out["engine_used"], "braveapi")
        self.assertEqual({r["engine"] for r in out["results"]}, {"braveapi"})

    def test_broken_free_tier_and_braveapi_emit_empty(self):
        mock = self._mock(
            unresponsive=["brave", "google"],
            broken_engines=["mwmbl", "searchmysite", "braveapi"],
        )
        script = self._script_for(mock.url)

        out = self._run(script, "brokenallcase")

        self.assertEqual(out["engine_used"], "none")
        self.assertEqual(out["results"], [])

    # --- Bypass paths -------------------------------------------------------
    def test_explicit_engines_bypass_the_chain(self):
        mock = self._mock(engine_results={"wikipedia": [result_item("W", "https://w.org", "wikipedia")]})
        script = self._script_for(mock.url)

        out = self._run(script, "weakcase", "en", "1", "general", "wikipedia")

        self.assertFalse(out["fallback_used"])
        self.assertEqual(out["engine_used"], "wikipedia")
        self.assertEqual(len(mock.requests), 1)
        self.assertEqual(mock.requests[0]["engines"], "wikipedia")
        # Search engines override the category - it must not be sent alongside.
        self.assertEqual(mock.requests[0]["categories"], "")

    def test_non_general_category_skips_the_chain(self):
        mock = self._mock()
        script = self._script_for(mock.url)

        out = self._run(script, "weakcase", "en", "1", "news")

        self.assertFalse(out["fallback_used"])
        self.assertEqual(len(mock.requests), 1)
        self.assertEqual(mock.requests[0]["categories"], "news")
        self.assertEqual(mock.requests[0]["engines"], "")

    # --- Fidelity -----------------------------------------------------------
    def test_chain_preserves_time_range_safesearch_language(self):
        mock = self._mock(engine_results={"google": GOOGLE}, unresponsive=["brave"])
        script = self._script_for(mock.url)

        out = self._run(script, "weakcase", "de", "1", "general", "", "week", "1")

        self.assertTrue(out["fallback_used"])
        self.assertEqual(len(mock.requests), 2)
        for req in mock.requests:
            self.assertEqual(req["time_range"], "week")
            self.assertEqual(req["safesearch"], "1")
            self.assertEqual(req["language"], "de")

    def test_tier_one_falls_through_the_instance_chain(self):
        broken = self._mock(unresponsive=["brave"])
        healthy = self._mock(engine_results={"brave": BRAVE})
        script = self._script_for(broken.url, healthy.url)

        out = self._run(script, "chaincase")

        self.assertEqual(out["instance"], healthy.url)
        self.assertEqual(out["engine_used"], "brave")
        self.assertFalse(out["fallback_used"])
        self.assertEqual(len(broken.requests), 1)
        self.assertEqual(len(healthy.requests), 1)

    def test_later_tiers_reuse_first_responsive_instance(self):
        primary = self._mock(engine_results={"google": [result_item("G", "https://g.com/1", "google")]})
        secondary = self._mock(engine_results={"google": [result_item("G", "https://g.com/2", "google")]})
        script = self._script_for(primary.url, secondary.url)

        out = self._run(script, "weakcase")

        self.assertEqual(out["instance"], primary.url)
        self.assertEqual(out["engine_used"], "google")
        self.assertEqual(len(primary.requests), 2)  # brave, then google
        self.assertEqual(len(secondary.requests), 1)  # brave tier only

    # --- SEARXNG_PRIMARY / SEARXNG_FALLBACK env override ----------------------
    def test_primary_env_replaces_instance_list(self):
        primary = self._mock(engine_results={"brave": BRAVE})
        secondary = self._mock(engine_results={"brave": BRAVE})
        env = {"SEARXNG_PRIMARY": primary.url, "SEARXNG_FALLBACK": secondary.url}

        out = self._run_env(str(SCRIPT), env, "bravecase")

        self.assertEqual(out["instance"], primary.url)
        self.assertEqual(out["engine_used"], "brave")
        self.assertEqual(len(primary.requests), 1)
        self.assertEqual(len(secondary.requests), 0)

    def test_fallback_env_used_when_primary_fails(self):
        primary = self._mock(unresponsive=["brave"])
        secondary = self._mock(engine_results={"brave": BRAVE})
        env = {"SEARXNG_PRIMARY": primary.url, "SEARXNG_FALLBACK": secondary.url}

        out = self._run_env(str(SCRIPT), env, "chaincase")

        self.assertEqual(out["instance"], secondary.url)
        self.assertEqual(out["engine_used"], "brave")
        self.assertEqual(len(primary.requests), 1)
        self.assertEqual(len(secondary.requests), 1)

    def test_explicit_empty_auth_sends_no_credentials(self):
        import base64

        mock = self._mock(engine_results={"brave": BRAVE})
        env = {
            "SEARXNG_PRIMARY": mock.url,
            "SEARXNG_PRIMARY_AUTH": "",
            "SEARXNG_AUTH": "user:pass",
        }

        out = self._run_env(str(SCRIPT), env, "bravecase")

        self.assertEqual(out["engine_used"], "brave")
        self.assertEqual(mock.requests[0]["authorization"], "")

    def test_shared_auth_reaches_primary_without_override(self):
        import base64

        mock = self._mock(engine_results={"brave": BRAVE})
        env = {
            "SEARXNG_PRIMARY": mock.url,
            "SEARXNG_AUTH": "user:pass",
        }

        out = self._run_env(str(SCRIPT), env, "bravecase")

        self.assertEqual(out["engine_used"], "brave")
        self.assertEqual(
            mock.requests[0]["authorization"],
            "Basic " + base64.b64encode(b"user:pass").decode(),
        )

    # --- SEARXNG_CHAIN=gregor profile -----------------------------------------
    def test_gregor_chain_starts_with_google(self):
        mock = self._mock(engine_results={"google": GOOGLE})
        env = {"SEARXNG_PRIMARY": mock.url, "SEARXNG_CHAIN": "gregor"}

        out = self._run_env(str(SCRIPT), env, "bravecase")

        self.assertEqual(out["engine_used"], "google")
        self.assertFalse(out["fallback_used"])
        self.assertEqual(out["tried"], ["google"])
        self.assertEqual(len(mock.requests), 1)
        self.assertEqual(mock.requests[0]["engines"], "google")

    def test_gregor_chain_falls_back_to_brave_then_braveapi(self):
        mock = self._mock(engine_results={"braveapi": API_RESULTS})
        env = {"SEARXNG_PRIMARY": mock.url, "SEARXNG_CHAIN": "gregor"}

        out = self._run_env(str(SCRIPT), env, "weakcase")

        self.assertEqual(out["engine_used"], "braveapi")
        self.assertTrue(out["fallback_used"])
        self.assertEqual(out["tried"], ["google", "brave", "braveapi"])
        # No free-tier request: the gregor profile skips mwmbl/searchmysite.
        self.assertNotIn(
            "mwmbl", [r["engines"] for r in mock.requests]
        )
        self.assertEqual(len(mock.requests), 3)


if __name__ == "__main__":
    unittest.main()
