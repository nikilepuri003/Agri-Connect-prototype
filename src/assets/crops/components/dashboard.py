import streamlit as st
import pandas as pd
from src.data.market_data import market_data
from src.data.buyer_data import buyers
from src.data.crop_catalog import crop_catalog
from .voice_input import get_voice_input

def display_dashboard():
    st.title("🌾 AgriConnect Dashboard")
    st.subheader("Sell Your Crops and Connect with Buyers")

    st.markdown("### Select Your Crops")
    
    crop_options = ["Tomato", "Chilli", "Rice", "Cotton", "Wheat"]
    selected_crops = st.multiselect("Choose Crops", crop_options)

    if st.button("Use Voice Input"):
        voice_input = get_voice_input()
        if voice_input:
            selected_crops = voice_input.split(",")

    if selected_crops:
        st.markdown("### Selected Crops")
        for crop in selected_crops:
            st.image(crop_catalog[crop]["image"], width=100, caption=crop)

        st.divider()

        # Display market data for selected crops
        for crop in selected_crops:
            prices = market_data[["Market", "Location", crop, "Distance"]].copy()
            prices.rename(columns={crop: "Market Price"}, inplace=True)

            st.subheader(f"Market Prices for {crop}")
            st.dataframe(prices)

            best_market = prices.loc[prices["Market Price"].idxmax()]
            st.success(f"Best Market for {crop}: {best_market['Market']} at ₹{best_market['Market Price']}/kg")

            # Show potential buyers for the selected crop
            matching_buyers = buyers[buyers["Crop"] == crop]
            if not matching_buyers.empty:
                st.subheader(f"Potential Buyers for {crop}")
                st.dataframe(matching_buyers)

    else:
        st.warning("Please select at least one crop to see market data.")

    # Display Google Maps for selected markets
    if selected_crops:
        st.subheader("Market Locations")
        for crop in selected_crops:
            if {"Latitude", "Longitude"}.issubset(market_data.columns):
                st.map(market_data[["Latitude", "Longitude"]])

    # Set background
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("src/assets/backgrounds/agri_3d_pattern.svg");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    display_dashboard()