from pathlib import Path

# Crop catalog containing details and images of various crops.
crop_assets_dir = Path(__file__).resolve().parents[2] / "src" / "assets" / "crops"

crop_catalog = {
    "Tomato": {
        "image": crop_assets_dir / "tomato.svg",
        "description": "Tomatoes are a rich source of vitamins and are widely used in cooking."
    },
    "Chilli": {
        "image": crop_assets_dir / "chilli.svg",
        "description": "Chillies add spice to dishes and are known for their health benefits."
    },
    "Rice": {
        "image": crop_assets_dir / "rice.svg",
        "description": "Rice is a staple food for a large part of the world's population."
    },
    "Cotton": {
        "image": crop_assets_dir / "cotton.svg",
        "description": "Cotton is a major agricultural commodity used in textiles."
    },
    "Wheat": {
        "image": crop_assets_dir / "wheat.svg",
        "description": "Wheat is one of the most important cereal crops globally."
    }
}