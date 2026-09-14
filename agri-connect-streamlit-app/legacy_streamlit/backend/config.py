from __future__ import annotations

import os
from typing import Any

import streamlit as st


def get_api_key(name: str) -> str:
    """Read an optional API key from Streamlit secrets or environment variables."""
    try:
        secret: Any = st.secrets.get(name, "")
    except Exception:
        secret = ""
    return str(secret or os.getenv(name, ""))


def google_maps_api_key() -> str:
    return get_api_key("GOOGLE_MAPS_API_KEY")


def google_speech_api_key() -> str:
    return get_api_key("GOOGLE_SPEECH_API_KEY")
