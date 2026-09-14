from __future__ import annotations

import streamlit as st

from db.data import MARKETS


def render_market_map() -> None:
    coordinates = MARKETS[["Latitude", "Longitude"]].rename(
        columns={"Latitude": "latitude", "Longitude": "longitude"}
    )
    coordinates = coordinates.dropna()
    if coordinates.empty:
        st.warning("Market locations are not available right now.")
        return
    st.map(coordinates, latitude="latitude", longitude="longitude", zoom=9)
    st.caption("Pins show nearby markets. Open Google Maps for turn-by-turn directions and live landmarks.")


def google_maps_url(location: str) -> str:
    return f"https://www.google.com/maps/search/?api=1&query={location.replace(' ', '+')}+market"


def google_maps_directions_url(location: str, origin: str = "") -> str:
    destination = f"{location.replace(' ', '+')}+market"
    origin_query = f"&origin={origin.replace(' ', '+')}" if origin.strip() else ""
    return f"https://www.google.com/maps/dir/?api=1{origin_query}&destination={destination}"