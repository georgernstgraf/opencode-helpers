"""Test support for the SearXNG skill.

Provides an in-process mock of the SearXNG JSON API (stdlib only) and a helper
to point a copy of `searxng-search.sh` at a mock instance. Nothing here touches
the network or the real instance.
"""

import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

INSTANCES_RE = re.compile(r"INSTANCES=\(\n(?:.*\n)*?\)")


def result_item(title, url, engine):
    """One search result in the shape SearXNG returns."""
    return {
        "title": title,
        "url": url,
        "engine": engine,
        "engines": [engine],
        "content": "snippet for " + title,
    }


BRAVE_RESULTS = [
    result_item("Brave 1", "https://example.com/a", "braveapi"),
    result_item("Brave 2", "https://example.com/new", "braveapi"),
]

# Query substring -> results. "braveapi" is matched via the engines parameter.
DEFAULT_SCENARIOS = {
    "braveapi": BRAVE_RESULTS,
    "emptycase": [],
    "weakcase": [
        result_item("Weak 1", "https://example.com/a", "mwmbl"),
        result_item("Weak 2", "https://example.com/b", "mwmbl"),
    ],
    "onegoogle": [result_item("Google 1", "https://g.com/1", "google")],
    "googlecase": [
        result_item("Google 1", "https://g.com/1", "google"),
        result_item("Google 2", "https://g.com/2", "google"),
        result_item("Google 3", "https://g.com/3", "google"),
    ],
}


def patch_script_instances(script_text, instance_urls):
    """Return `script_text` with its INSTANCES array replaced by `instance_urls`."""
    block = "INSTANCES=(\n" + "".join('    "{0}"\n'.format(u) for u in instance_urls) + ")\n"
    patched, count = INSTANCES_RE.subn(block, script_text, count=1)
    if count != 1:
        raise RuntimeError("INSTANCES block not found in searxng-search.sh")
    return patched


class MockSearxng:
    """A local SearXNG JSON API mock.

    Usage::

        mock = MockSearxng().start()
        ...  # use mock.url, then inspect mock.requests
        mock.stop()
    """

    def __init__(self, scenarios=None, default=None, unresponsive=None):
        self.scenarios = dict(DEFAULT_SCENARIOS if scenarios is None else scenarios)
        self.default = [] if default is None else default
        self.unresponsive = list(unresponsive or [])
        self.requests = []
        self.port = None
        self._server = None
        self._thread = None

    def start(self):
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                qs = parse_qs(urlparse(self.path).query)
                record = {
                    "q": qs.get("q", [""])[0],
                    "engines": qs.get("engines", [""])[0],
                    "categories": qs.get("categories", [""])[0],
                    "language": qs.get("language", [""])[0],
                    "time_range": qs.get("time_range", [""])[0],
                    "safesearch": qs.get("safesearch", [""])[0],
                }
                outer.requests.append(record)

                results = outer._resolve(record)
                body = json.dumps(
                    {
                        "number_of_results": len(results),
                        "results": results,
                        "unresponsive_engines": [
                            [name, "Suspended: test"] for name in outer.unresponsive
                        ],
                    }
                ).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self._server.server_address[1]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    @property
    def url(self):
        return "http://127.0.0.1:{0}".format(self.port)

    def _resolve(self, record):
        # Explicit engines are being requested.
        if record["engines"]:
            if "braveapi" in record["engines"]:
                return self.scenarios.get("braveapi", [])
            return self.default
        # Default query: match by query substring.
        for key, results in self.scenarios.items():
            if key != "braveapi" and key in record["q"]:
                return results
        return self.default

    def stop(self):
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._thread.join(timeout=5)
            self._server = None
