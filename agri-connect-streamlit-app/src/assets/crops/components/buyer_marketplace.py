import streamlit as st
import pandas as pd
from src.data.buyer_data import buyers
from src.data.crop_catalog import crop_catalog
from src.utils.formatting import format_currency
from .voice_input import get_voice_input
from .maps import display_market_map

def buyer_marketplace():
    st.title("🤝 Buyer Marketplace")
    st.write("Connect farmers directly with potential buyers.")

    # Voice input for crop selection
    selected_crop = get_voice_input()
    if not selected_crop:
        selected_crop = st.selectbox("Select Crop", ["Tomato", "Chilli", "Rice", "Cotton"])

    # Show only buyers who want the selected crop
    filtered_buyers = buyers[buyers["Crop"] == selected_crop]

    if len(filtered_buyers) > 0:
        for _, buyer in filtered_buyers.iterrows():
            with st.container():
                st.subheader(f"🏢 {buyer['Buyer']}")
                col1, col2, col3 = st.columns(3)

                col1.image(crop_catalog[buyer["Crop"]]["image"], width=50)
                col1.write(f"💰 Offer: {format_currency(buyer['Price'])}/kg")
                col2.write(f"📦 Requirement: {buyer['Required Quantity']}")
                col3.write(f"📍 Location: {buyer['Location']}")

                # Connect button for each buyer
                if st.button(f"Connect with {buyer['Buyer']}", key=buyer["Buyer"]):
                    st.success("Buyer connection request sent!")

                # Display map for buyer's location
                display_market_map(buyer["Location"])

                st.divider()
    else:
        st.info("No buyers found.")
