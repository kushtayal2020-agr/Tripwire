"""Serve the local Tripwire text-scanning web interface."""
import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .scan import scan

MAX_REQUEST_BYTES = 1_000_000
INDEX_FILE = Path(__file__).with_name("web") / "index.html"


class TripwireHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        try:
            page = INDEX_FILE.read_bytes()
        except OSError:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Web interface is unavailable")
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'")
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        if self.path != "/api/scan":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        if self.headers.get_content_type() != "application/json":
            self.send_error(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "Expected application/json")
            return

        try:
            content_length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid Content-Length")
            return

        if content_length < 0:
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid Content-Length")
            return
        if content_length > MAX_REQUEST_BYTES:
            self.send_error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "Text exceeds the 1 MB limit")
            return

        try:
            payload = json.loads(self.rfile.read(content_length))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_error(HTTPStatus.BAD_REQUEST, "Request body must be valid UTF-8 JSON")
            return
        if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
            self.send_error(HTTPStatus.BAD_REQUEST, "JSON body must contain a string 'text' field")
            return

        result = scan(payload["text"], use_classifier=False)
        response = json.dumps({
            "verdict": result.verdict,
            "score": result.score,
            "reasons": result.reasons,
        }).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format_string, *args):
        print(f"[Tripwire web] {self.address_string()} - {format_string % args}")


def create_server(port: int = 8000) -> ThreadingHTTPServer:
    """Create a local-only web server, primarily useful for tests and embedding."""
    return ThreadingHTTPServer(("127.0.0.1", port), TripwireHandler)


def main() -> int:
    parser = argparse.ArgumentParser(description="Start the local Tripwire scanning web interface.")
    parser.add_argument("--port", type=int, default=8000, help="local server port (default: 8000)")
    args = parser.parse_args()
    if not 0 < args.port < 65536:
        parser.error("--port must be between 1 and 65535")

    server = create_server(args.port)
    url = f"http://127.0.0.1:{server.server_address[1]}"
    print(f"Tripwire web interface: {url} (press Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Tripwire web interface.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
