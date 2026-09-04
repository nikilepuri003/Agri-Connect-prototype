import streamlit as st

from src.services.map_service import (
    get_map_data,
    get_location_data,
    get_nearby_markets
)


def display_map(latitude=16.3067, longitude=80.4365):

    map_data = get_map_data(
        latitude,
        longitude
    )

    st.subheader("📍 Market Location")

    st.map(
        {
            "latitude": [map_data["latitude"]],
            "longitude": [map_data["longitude"]]
        },
        latitude=map_data["latitude"],
        longitude=map_data["longitude"],
        zoom=12
    )


def display_market_map(address):

    location = get_location_data(address)

    if location is None:
        st.error("Unable to find this location.")
        return

    latitude = location["latitude"]
    longitude = location["longitude"]

    display_map(latitude, longitude)

    markets = get_nearby_markets(
        latitude,
        longitude
    )

    if markets:

        st.subheader("🏪 Nearby Markets")

        for market in markets:

            st.write(
                f"**{market['name']}**"
            )

    else:

        st.info("No nearby markets found.")