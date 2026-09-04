import streamlit as st
import pandas as pd
from src.data.market_data import market_data
from src.data.crop_catalog import crop_catalog

def market_analysis():
    st.title("📊 Market Price Analysis")
    st.write("Compare crop prices across nearby markets.")

    # Crop selection with images
    crop_options = list(crop_catalog)
    selected_crop = st.selectbox("Select Crop", crop_options)

    # Display crop image
    crop_image = crop_catalog[selected_crop]["image"]
    st.image(crop_image, width=100)

    # Create a table with only market, price, and distance
    analysis = market_data[["Market", selected_crop, "Distance"]].copy()
    analysis.rename(columns={selected_crop: "Price (₹/kg)"}, inplace=True)

    # Show the market price table
    st.dataframe(analysis, use_container_width=True, hide_index=True)

    st.subheader("📈 Price Comparison")
    st.bar_chart(analysis.set_index("Market")["Price (₹/kg)"])

    # Find the market with the highest price
    highest = analysis.loc[analysis["Price (₹/kg)"].idxmax()]
    st.success(f"Highest price: {highest['Market']} - ₹{highest['Price (₹/kg)']}/kg")

    # Add Google Maps functionality to show market locations
    st.subheader("🗺️ Market Locations")
    for market in analysis['Market']:
        st.map(data=market_data[market_data['Market'] == market][['Latitude', 'Longitude']])

# Call the function to render the market analysis component
if __name__ == "__main__":
    market_analysis()