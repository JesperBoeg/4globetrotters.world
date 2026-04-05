"""Dev server that serves local files and proxies /wp-content/uploads/ to live site."""
import http.server
import urllib.request
import os

SITE_DIR = os.path.join(os.path.dirname(__file__), "option-b-static", "site")
LIVE_HOST = "https://4globetrotters.world"
PORT = 8080


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith("/wp-content/uploads/"):
            # Try local file first, fall back to live site
            local_path = os.path.join(SITE_DIR, self.path.lstrip("/"))
            if os.path.isfile(local_path):
                super().do_GET()
            else:
                self._proxy_to_live()
        else:
            super().do_GET()

    def _proxy_to_live(self):
        url = LIVE_HOST + self.path
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                self.send_response(resp.status)
                ct = resp.getheader("Content-Type", "application/octet-stream")
                self.send_header("Content-Type", ct)
                self.send_header("Content-Length", len(data))
                self.send_header("Cache-Control", "public, max-age=86400")
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            self.send_error(502, f"Proxy error: {e}")


if __name__ == "__main__":
    server = http.server.HTTPServer(("", PORT), ProxyHandler)
    print(f"Dev server on http://localhost:{PORT}")
    print(f"Local files from: {SITE_DIR}")
    print(f"Images proxied from: {LIVE_HOST}")
    server.serve_forever()
