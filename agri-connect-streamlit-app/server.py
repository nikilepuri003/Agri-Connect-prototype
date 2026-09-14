#!/usr/bin/env python3
"""
AgriConnect Application Launcher
Run this script to start the AgriConnect Web Application.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.server import load_config, run_server

if __name__ == "__main__":
    cfg = load_config()
    host = cfg.get("host", "localhost")
    port = int(cfg.get("port", 8000))
    run_server(host=host, port=port, open_browser=True)

