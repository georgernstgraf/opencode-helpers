"""Test support for the deepseek-search skill.

Provides an in-process mock of the DeepSeek Search API (stdlib only). Nothing
here touches the network or the real API.

The mock answers ``POST /v1/tools/search``. ``queue`` holds ``(status, body)``
pairs consumed one per request (last one repeats); without a queue every
request is answered with ``status`` and ``{"results": results}``.
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def result_item(title, url, **extra):
    """One result in the shape the DeepSeek Search API returns."""
    item = {
        "title": title,
        "url": url,
        "snippet": "snippet for " + title,
        "summary": "summary for " + title,
        "date": "2026-06-01T00:00:00+00:00",
        "authority": 3,
        "rerank_score": 2.4,
        "content": "",
        "site_name": "example.com",
        "site_icon": None,
    }
    item.update(extra)
    return item


class MockDeepSeek:
    """A local mock of the DeepSeek Search API.

    Usage::

        mock = MockDeepSeek(results=[result_item("A", "https://a.example/1")]).start()
        ...  # point DEEPSEEK_SEARCH_API_BASE at mock.url, then inspect mock.requests
        mock.stop()
    """

    def __init__(self, results=None, status=200, body=None, queue=None):
        self.results = list(results or [])
        self.status = status
        self.body = body
        self.queue = list(queue or [])
        self.requests = []
        self.port = None
        self._server = None
        self._thread = None

    def start(self):
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length) if length else b""
                try:
                    payload = json.loads(raw.decode("utf-8") or "{}")
                except json.JSONDecodeError:
                    payload = None
                outer.requests.append(
                    {
                        "path": self.path,
                        "authorization": self.headers.get("Authorization", ""),
                        "payload": payload,
                    }
                )

                if outer.queue:
                    status, body = outer.queue.pop(0)
                else:
                    status = outer.status
                    body = outer.body
                    if body is None:
                        body = {"results": outer.results}

                encoded = json.dumps(body).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

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

    def stop(self):
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._thread.join(timeout=5)
            self._server = None
