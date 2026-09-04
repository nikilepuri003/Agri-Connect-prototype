import streamlit as st
from src.data.crop_catalog import crop_catalog

def sidebar():
    st.sidebar.title("🌾 AgriConnect")
    st.sidebar.write("AI-based Market Linkage & Price Discovery")

    # Crop selection with images
    selected_crops = st.sidebar.multiselect(
        "Select Crops",
        options=list(crop_catalog),
    )

    # Display crop images
    for crop in selected_crops:
        crop_image = crop_catalog[crop]["image"]
        if crop_image:
            st.sidebar.image(crop_image, width=50)

    # Navigation options
    page = st.sidebar.radio(
        "Navigate",
        [
            "Farmer Dashboard",
            "Market Analysis",
            "Buyer Marketplace"
        ]
    )

    return page, selected_crops