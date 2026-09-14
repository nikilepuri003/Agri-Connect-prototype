def get_crop_images():
    return {
        "Tomato": "src/assets/crops/tomato.svg",
        "Chilli": "src/assets/crops/chilli.svg",
        "Rice": "src/assets/crops/rice.svg",
        "Cotton": "src/assets/crops/cotton.svg",
        "Wheat": "src/assets/crops/wheat.svg"
    }

def get_background_image():
    return "src/assets/backgrounds/agri_3d_pattern.svg"

def validate_crop_selection(selected_crop):
    valid_crops = ["Tomato", "Chilli", "Rice", "Cotton", "Wheat"]
    if selected_crop not in valid_crops:
        raise ValueError("Invalid crop selected. Please choose a valid crop.")

def format_price(price):
    return f"₹{price:.2f}"