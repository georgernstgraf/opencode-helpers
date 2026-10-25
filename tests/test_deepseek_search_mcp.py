"""Tests for the deepseek-search MCP server.

Protocol tests need no network. Integration tests copy the server into a temp
skill layout next to a mock-pointed copies of `searxng-search.sh`, so both the
DeepSeek API and the SearXNG fallback are served by in-process mocks.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import deepseek_search_mock
import searxng_mock

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "skills" / "deepseek-search" / "scripts" / "opencode-deepseek-search"
SEARXNG_SCRIPT = ROOT / "skills" / "searxng" / "searxng-search.sh"
KEY = "sk-test-not-a-real-key"


class DeepSeekSearchTest(unittest.TestCase):
    def setUp(self):
        self.searxng = searxng_mock.MockSearxng(
            engine_results={
                "bing": [searxng_mock.result_item("Bing hit", "https://b.example/1", "bing")],
                "wikipedia": [searxng_mock.result_item("Wiki hit", "https://w.example/1", "wikipedia")],
            },
            unresponsive=[],
        ).start()
        self.addCleanup(self.searxng.stop)

    # -- helpers ---------------------------------------------------------

    def _layout(self, searxng_url=None):
        """Temp skill layout: deepseek-search beside a patched searxng script."""
        tmp = Path(tempfile.mkdtemp(prefix="deepseek-skill-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        (tmp / "skills" / "deepseek-search" / "scripts").mkdir(parents=True)
        (tmp / "skills" / "searxng").mkdir(parents=True)

        server = tmp / "skills" / "deepseek-search" / "scripts" / "opencode-deepseek-search"
        shutil.copy2(SERVER, server)

        target = tmp / "skills" / "searxng" / "searxng-search.sh"
        shutil.copy2(SEARXNG_SCRIPT, target)
        target.write_text(
            searxng_mock.patch_script_instances(
                SEARXNG_SCRIPT.read_text(), [searxng_url or self.searxng.url]
            )
        )
        return server

    def _env(self, api_base=None, key=KEY, providers=None, searxng_primary="default",
             extra=None):
        env = {
            name: value
            for name, value in os.environ.items()
            if not name.startswith(("DEEPSEEK_SEARCH_", "SEARXNG_"))
        }
        if api_base:
            env["DEEPSEEK_SEARCH_API_BASE"] = api_base
        if key:
            env["DEEPSEEK_SEARCH_API_KEY"] = key
        if providers:
            env["DEEPSEEK_SEARCH_PROVIDERS"] = providers
        if searxng_primary is not None:
            env["SEARXNG_PRIMARY"] = (
                self.searxng.url if searxng_primary == "default" else searxng_primary
            )
        env.update(extra or {})
        return env

    def _call(self, server, messages, env):
        payload = "\n".join(json.dumps(m) for m in messages) + "\n"
        proc = subprocess.run(
            [sys.executable, str(server)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]

    def _search(self, server, env, **arguments):
        out = self._call(
            server,
            [
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": "search", "arguments": arguments},
                }
            ],
            env,
        )
        self.assertIn("result", out[0], out)
        return json.loads(out[0]["result"]["content"][0]["text"])

    def _deepseek(self, **kwargs):
        mock = deepseek_search_mock.MockDeepSeek(**kwargs).start()
        self.addCleanup(mock.stop)
        return mock

    # -- protocol --------------------------------------------------------

    def test_protocol_initialize_and_tools_list(self):
        out = self._call(
            SERVER,
            [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            ],
            self._env(),
        )
        by_id = {m["id"]: m for m in out}
        self.assertEqual(by_id[1]["result"]["serverInfo"]["name"], "deepseek")

        tool = by_id[2]["result"]["tools"][0]
        self.assertEqual(tool["name"], "search")
        properties = tool["inputSchema"]["properties"]
        for name in ("query", "count", "need_content", "language", "time_range",
                     "site", "after", "before", "engines", "category"):
            self.assertIn(name, properties)
        self.assertIn("fallback", tool["description"].lower())

    # -- deepseek provider -----------------------------------------------

    def test_deepseek_success(self):
        mock = self._deepseek(
            results=[
                deepseek_search_mock.result_item("First", "https://a.example/1"),
                deepseek_search_mock.result_item("Second", "https://a.example/2"),
            ]
        )
        payload = self._search(
            self._layout(), self._env(api_base=mock.url), query="opencode v2"
        )

        self.assertTrue(payload["success"])
        self.assertEqual(payload["provider"], "deepseek")
        self.assertEqual(payload["engine_used"], "deepseek")
        self.assertFalse(payload["fallback_used"])
        self.assertEqual(payload["total_results"], 2)
        self.assertEqual(payload["results"][0]["title"], "First")
        self.assertEqual(payload["results"][0]["authority"], 3)
        self.assertEqual(payload["results"][0]["rerank_score"], 2.4)
        self.assertEqual(payload["providers_unavailable"], [])
        self.assertEqual(len(mock.requests), 1)
        self.assertEqual(mock.requests[0]["path"], "/v1/tools/search")
        self.assertEqual(mock.requests[0]["authorization"], "Bearer " + KEY)
        self.assertEqual(self.searxng.requests, [])

    def test_need_content_passthrough(self):
        mock = self._deepseek(
            results=[deepseek_search_mock.result_item("A", "https://a.example/1", content="# A")]
        )
        payload = self._search(
            self._layout(), self._env(api_base=mock.url),
            query="with content", need_content=True,
        )
        self.assertTrue(mock.requests[0]["payload"]["need_content"])
        self.assertEqual(payload["results"][0]["content"], "# A")

    def test_count_clamped_and_operators_composed(self):
        mock = self._deepseek(
            results=[deepseek_search_mock.result_item("A", "https://a.example/1")]
        )
        payload = self._search(
            self._layout(), self._env(api_base=mock.url),
            query="deepseek search api",
            count=99,
            language="de",
            time_range="week",
            site="github.com,arxiv.org",
        )
        sent = mock.requests[0]["payload"]
        self.assertEqual(sent["count"], 50)

        expected_after = (date.today() - timedelta(days=7)).isoformat()
        self.assertIn("lang:de", sent["query"])
        self.assertIn("after:" + expected_after, sent["query"])
        self.assertIn("site:github.com OR site:arxiv.org", sent["query"])
        self.assertIn("after:" + expected_after, payload["query"])

    def test_long_query_truncated_with_warning(self):
        mock = self._deepseek(
            results=[deepseek_search_mock.result_item("A", "https://a.example/1")]
        )
        payload = self._search(
            self._layout(), self._env(api_base=mock.url),
            query="word " * 60,
        )
        self.assertLessEqual(len(mock.requests[0]["payload"]["query"]), 128)
        self.assertTrue(any("shortened" in w for w in payload["warnings"]))

    # -- fallback behaviour ----------------------------------------------

    def test_missing_key_uses_searxng(self):
        mock = self._deepseek(
            results=[deepseek_search_mock.result_item("A", "https://a.example/1")]
        )
        payload = self._search(
            self._layout(), self._env(api_base=mock.url, key=None), query="no key here"
        )
        self.assertEqual(payload["provider"], "searxng")
        self.assertEqual(payload["engine_used"], "bing")
        self.assertEqual(payload["providers_unavailable"], ["deepseek"])
        self.assertFalse(payload["fallback_used"])
        self.assertFalse(payload["engine_fallback_used"])
        self.assertEqual(mock.requests, [])
        self.assertEqual(len(self.searxng.requests), 1)

    def test_provider_failures_fall_back_to_searxng(self):
        for status in (402, 408, 429, 500, 503):
            with self.subTest(status=status):
                mock = self._deepseek(status=status, body={"error": {"message": "nope"}})
                payload = self._search(
                    self._layout(), self._env(api_base=mock.url), query="break it"
                )
                self.assertEqual(payload["provider"], "searxng")
                self.assertTrue(payload["fallback_used"])
                self.assertEqual(payload["fallback_reason"], "http_{}".format(status))
                self.assertEqual(payload["providers_tried"], ["deepseek", "searxng"])

    def test_empty_results_fall_back_to_searxng(self):
        mock = self._deepseek(results=[])
        payload = self._search(
            self._layout(), self._env(api_base=mock.url), query="nothing at all"
        )
        self.assertEqual(payload["provider"], "searxng")
        self.assertEqual(payload["fallback_reason"], "empty")

    def test_401_is_fatal_without_fallback(self):
        mock = self._deepseek(status=401, body={"error": {"message": "bad key"}})
        payload = self._search(
            self._layout(), self._env(api_base=mock.url), query="bad key case"
        )
        self.assertFalse(payload["success"])
        self.assertIn("http_401", payload["error"])
        self.assertEqual(payload["providers_tried"], ["deepseek"])
        self.assertEqual(self.searxng.requests, [])

    def test_unreachable_api_falls_back(self):
        layout = self._layout()
        payload = self._search(
            layout,
            self._env(api_base="http://127.0.0.1:1"),
            query="connection refused",
        )
        self.assertEqual(payload["provider"], "searxng")
        self.assertEqual(payload["fallback_reason"], "network")

    # -- searxng-only routing --------------------------------------------

    def test_engines_route_to_searxng(self):
        mock = self._deepseek(
            results=[deepseek_search_mock.result_item("A", "https://a.example/1")]
        )
        payload = self._search(
            self._layout(), self._env(api_base=mock.url),
            query="austria", engines="wikipedia",
        )
        self.assertEqual(payload["provider"], "searxng")
        self.assertEqual(payload["engine_used"], "wikipedia")
        self.assertEqual(mock.requests, [])
        self.assertEqual(self.searxng.requests[0]["engines"], "wikipedia")
        self.assertTrue(any("SearXNG-only" in w for w in payload["warnings"]))

    def test_pageno_routes_to_searxng(self):
        mock = self._deepseek(
            results=[deepseek_search_mock.result_item("A", "https://a.example/1")]
        )
        payload = self._search(
            self._layout(), self._env(api_base=mock.url), query="page two", pageno=2
        )
        self.assertEqual(payload["provider"], "searxng")
        self.assertEqual(mock.requests, [])

    def test_pinned_to_searxng_never_calls_deepseek(self):
        mock = self._deepseek(
            results=[deepseek_search_mock.result_item("A", "https://a.example/1")]
        )
        payload = self._search(
            self._layout(),
            self._env(api_base=mock.url, providers="searxng"),
            query="pinned",
        )
        self.assertEqual(payload["provider"], "searxng")
        self.assertFalse(payload["fallback_used"])
        self.assertIn("deepseek", payload["providers_unavailable"])
        self.assertEqual(mock.requests, [])

    # -- configuration errors --------------------------------------------

    def test_no_provider_configured(self):
        layout = self._layout()
        payload = self._search(layout, self._env(key=None, searxng_primary=None),
                               query="nobody home")
        self.assertFalse(payload["success"])
        self.assertIn("No search provider", payload["error"])
        self.assertEqual(payload["providers_tried"], [])
        self.assertEqual(sorted(payload["providers_unavailable"]), ["deepseek", "searxng"])

    def test_missing_query_returns_error(self):
        out = self._call(
            SERVER,
            [
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": "search", "arguments": {}},
                }
            ],
            self._env(),
        )
        self.assertIn("error", out[0])


if __name__ == "__main__":
    unittest.main()
