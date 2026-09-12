"""Tests for the SearXNG MCP server (skills/searxng/scripts/opencode-searxng).

Protocol tests need no network. The integration test copies the server into a
temp skill layout next to a mock-pointed search script, so it is hermetic too.
"""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import searxng_mock

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "skills" / "searxng" / "scripts" / "opencode-searxng"
SCRIPT = ROOT / "skills" / "searxng" / "searxng-search.sh"


class OpenCodeSearxngTest(unittest.TestCase):
    def _call(self, server, messages):
        payload = "\n".join(json.dumps(m) for m in messages) + "\n"
        proc = subprocess.run(
            [sys.executable, str(server)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]

    def _temp_server(self, mock_url):
        tmp = Path(tempfile.mkdtemp(prefix="searxng-skill-"))
        (tmp / "scripts").mkdir()
        shutil.copy2(SERVER, tmp / "scripts" / "opencode-searxng")
        # copy2 preserves the executable bit the MCP server relies on.
        target = tmp / "searxng-search.sh"
        shutil.copy2(SCRIPT, target)
        target.write_text(searxng_mock.patch_script_instances(SCRIPT.read_text(), [mock_url]))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        return tmp / "scripts" / "opencode-searxng"

    def test_protocol_initialize_and_tools_list(self):
        out = self._call(
            SERVER,
            [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            ],
        )
        by_id = {m["id"]: m for m in out}
        self.assertEqual(by_id[1]["result"]["serverInfo"]["name"], "searxng")

        tool = by_id[2]["result"]["tools"][0]
        self.assertEqual(tool["name"], "search")
        self.assertIn("fallback", tool["description"].lower())
        self.assertIn("engines", tool["inputSchema"]["properties"])

    def test_tools_call_runs_fallback_end_to_end(self):
        mock = searxng_mock.MockSearxng().start()
        self.addCleanup(mock.stop)
        server = self._temp_server(mock.url)

        out = self._call(
            server,
            [
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": "search", "arguments": {"query": "weakcase"}},
                }
            ],
        )
        payload = json.loads(out[0]["result"]["content"][0]["text"])
        self.assertTrue(payload["fallback_used"])
        self.assertEqual(payload["fallback_reason"], "weak")
        self.assertIn("braveapi", {r["engine"] for r in payload["results"]})

    def test_tools_call_explicit_engines_bypasses_fallback(self):
        mock = searxng_mock.MockSearxng().start()
        self.addCleanup(mock.stop)
        server = self._temp_server(mock.url)

        out = self._call(
            server,
            [
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "search",
                        "arguments": {"query": "weakcase", "engines": "braveapi"},
                    },
                }
            ],
        )
        payload = json.loads(out[0]["result"]["content"][0]["text"])
        self.assertFalse(payload["fallback_used"])
        self.assertEqual({r["engine"] for r in payload["results"]}, {"braveapi"})
        self.assertEqual(len(mock.requests), 1)
        self.assertEqual(mock.requests[0]["engines"], "braveapi")

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
        )
        self.assertIn("error", out[0])


if __name__ == "__main__":
    unittest.main()
