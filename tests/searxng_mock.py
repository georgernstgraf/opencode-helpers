"""Test support for the SearXNG skill.

Provides an in-process mock of the SearXNG JSON API (stdlib only) and a helper
to point a copy of `searxng-search.sh` at a mock instance. Nothing here touches
the network or the real instance.

The mock resolves results per requested engine: a request carrying
`engines=brave,google` returns the concatenation of those engines' configured
results, minus any engine listed as suspended (`unresponsive`).
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

        mock = MockSearxng(engine_results={"brave": [...]}).start()
        ...  # use mock.url, then inspect mock.requests
        mock.stop()

    ``engine_results`` maps an engine name to the results it returns when
    explicitly requested. ``unresponsive`` lists engines that are "suspended":
    they contribute no results and appear in ``unresponsive_engines``.
    ``broken_engines`` makes a request naming any of these engines fail at the
    transport level (a non-JSON body), simulating a timeout/error.
    Queries without an ``engines`` parameter return ``default``.
    """

    def __init__(self, engine_results=None, unresponsive=None, default=None,
                 broken_engines=None):
        self.engine_results = dict(engine_results or {})
        self.unresponsive = list(unresponsive or [])
        self.broken_engines = list(broken_engines or [])
        self.default = [] if default is None else default
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

                requested = [e for e in record["engines"].split(",") if e]
                if any(name in outer.broken_engines for name in requested):
                    body = b"<html>upstream error</html>"
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return

                results, unresponsive = outer._resolve(record)
                body = json.dumps(
                    {
                        "number_of_results": len(results),
                        "results": results,
                        "unresponsive_engines": unresponsive,
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
        requested = [e for e in record["engines"].split(",") if e] if record["engines"] else []
        if not requested:
            # No explicit engines (category query): report all configured
            # suspensions so a "broken" instance can be simulated.
            return self.default, [
                [name, "Suspended: test"] for name in self.unresponsive
            ]

        results = []
        unresponsive = []
        for name in requested:
            if name in self.unresponsive:
                unresponsive.append([name, "Suspended: test"])
                continue
            results.extend(self.engine_results.get(name, []))
        return results, unresponsive

    def stop(self):
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._thread.join(timeout=5)
            self._server = None
