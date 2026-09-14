#!/usr/bin/env python3
"""
AgriConnect Launcher (app.py)
"""

if __name__ == "__main__":
    from backend.server import load_config, run_server
    cfg = load_config()
    run_server(host=cfg.get("host", "localhost"), port=int(cfg.get("port", 8000)), open_browser=True)
