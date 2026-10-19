"""Static local-only server. Never exposes the repository or runs the engine."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse

HERE = Path(__file__).resolve().parent


class Handler(SimpleHTTPRequestHandler):
    root = HERE / "web"

    def do_GET(self):
        # Prevent nonlocal Host use and any symlink escape/directory listing.
        host = self.headers.get("Host", "").split(":")[0]
        if host not in {"127.0.0.1", "localhost"}:
            self.send_error(403); return
        super().do_GET()

    def translate_path(self, path):
        target = Path(super().translate_path(path)).resolve()
        return str(target if target.is_relative_to(self.root) else self.root / "forbidden")

    def list_directory(self, path):
        self.send_error(403, "Directory listing disabled")

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
        super().end_headers()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--root", choices=("web", "academic-demo-dist"), default="web")
    args = parser.parse_args()
    root = HERE / args.root
    if not (root / "catalog.json").exists():
        parser.error("Run prepare.py first; no bundle is available")
    Handler.root = root.resolve()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(root)))
    print(f"GeoImpact Review Studio: http://127.0.0.1:{args.port} ({args.root}; full viewer HOLD)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
