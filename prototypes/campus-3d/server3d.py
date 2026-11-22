"""Local demo server: serve the campus screen and call the existing saved game.

Run: uv run python prototypes/campus-3d/server3d.py
This is a localhost prototype, not a production or authenticated hosting service.
"""

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from page3d import HERE, PROJECT, build_page
import db
from campus_game import command


class CampusHandler(BaseHTTPRequestHandler):
    def reply(self, status, content, kind):
        data = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", kind + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def json_reply(self, status, content):
        self.reply(status, json.dumps(content, ensure_ascii=False), "application/json")

    def local_request(self):
        # Accept only our local host, and reject commands from unrelated websites.
        hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        host = self.headers.get("Host")
        origin = self.headers.get("Origin")
        return host in hosts and (origin is None or origin == f"http://{host}")

    def do_GET(self):
        if not self.local_request():
            return self.json_reply(403, {"error": "Local requests only."})
        path = urlparse(self.path).path
        if path == "/":
            return self.reply(200, self.server.campus_page, "text/html")
        public_files = {"/play.js": "text/javascript", "/table.js": "text/javascript", "/play.css": "text/css"}
        if path in public_files:
            return self.reply(200, (HERE / path[1:]).read_text(encoding="utf-8"), public_files[path])
        self.json_reply(404, {"error": "Not found."})

    def do_POST(self):
        if self.path != "/api/command":
            return self.json_reply(404, {"error": "Not found."})
        if not self.local_request():
            return self.json_reply(403, {"error": "Local requests only."})
        if self.headers.get_content_type() != "application/json":
            return self.json_reply(415, {"error": "JSON required."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError("Invalid request size.")
            payload = json.loads(self.rfile.read(length))
            with self.server.command_lock:
                result = command(payload)
        except (ValueError, UnicodeDecodeError) as error:
            return self.json_reply(400, {"error": str(error)})
        except Exception:
            # Do not claim the action was saved or expose local file paths.
            return self.json_reply(500, {"error": "Could not complete the request. Reopen your game to check progress. / Não foi possível concluir o pedido. Reabre o jogo para confirmar o progresso."})
        self.json_reply(200, result)


def make_server(port=8765):
    server = ThreadingHTTPServer(("127.0.0.1", port), CampusHandler)
    server.campus_page = build_page(playable=True)
    server.command_lock = threading.Lock()
    return server


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--database", type=str, default=str(PROJECT / "data" / "campus3d.db"))
    args = parser.parse_args()
    from pathlib import Path
    db.DB_PATH = Path(args.database)
    with make_server(args.port) as server:
        print(f"Open http://127.0.0.1:{server.server_port} — Ctrl+C to stop.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
