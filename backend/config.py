from __future__ import annotations

import os


def get_api_key(name: str) -> str:
    """Read an optional API key from the host environment."""
    return os.getenv(name, "")


def google_maps_api_key() -> str:
    return get_api_key("GOOGLE_MAPS_API_KEY")


def google_speech_api_key() -> str:
    return get_api_key("GOOGLE_SPEECH_API_KEY")
