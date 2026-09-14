#!/usr/bin/env python3
"""
AgriConnect Backend Server
Provides static file serving for the frontend and JSON REST API endpoints.
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import urllib.parse

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DB_DIR = BASE_DIR / "db"
DATA_JSON_PATH = DB_DIR / "data.json"
CONFIG_JSON_PATH = Path(__file__).resolve().parent / "config.json"


def load_config() -> dict:
    if CONFIG_JSON_PATH.exists():
        try:
            with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not read config.json: {e}", file=sys.stderr)
    return {"port": 8000, "host": "localhost"}


def load_data() -> dict:
    if DATA_JSON_PATH.exists():
        with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


class AgriConnectHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self) -> None:
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        # REST API: /api/data
        if path == "/api/data":
            self.send_json_response(load_data())
            return

        # REST API: /api/config
        if path == "/api/config":
            cfg = load_config()
            # Omit private keys if needed, or send public keys
            safe_cfg = {
                "google_maps_api_key": cfg.get("google_maps_api_key", ""),
                "app_name": "AgriConnect",
                "version": "2.0.0"
            }
            self.send_json_response(safe_cfg)
            return

        # REST API: /api/health
        if path == "/api/health":
            self.send_json_response({"status": "ok", "app": "AgriConnect"})
            return

        # Static file routing
        if path in ("", "/"):
            self.path = "/index.html"
        
        return super().do_GET()

    def send_json_response(self, data: dict | list, status: int = HTTPStatus.OK) -> None:
        payload = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format: str, *args) -> None:
        # Clean logging format
        sys.stdout.write(f"[AgriConnect Server] {self.address_string()} - {args[0]} - {args[1]}\n")
        sys.stdout.flush()


def run_server(host: str = "localhost", port: int = 8000, open_browser: bool = False) -> None:
    server_address = (host, port)
    httpd = HTTPServer(server_address, AgriConnectHandler)
    url = f"http://{host}:{port}"
    print("=" * 60)
    print(">> AgriConnect Web App Server is running!")
    print(f"   URL: {url}")
    print(f"   Frontend files: {FRONTEND_DIR}")
    print(f"   Database file:  {DATA_JSON_PATH}")
    print("   Press Ctrl+C to stop the server.")
    print("=" * 60)

    if open_browser:
        import webbrowser
        webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping AgriConnect server...")
        httpd.server_close()
        print("Server stopped cleanly.")


if __name__ == "__main__":
    config = load_config()
    server_host = config.get("host", "localhost")
    server_port = int(config.get("port", 8000))
    run_server(host=server_host, port=server_port, open_browser=False)
