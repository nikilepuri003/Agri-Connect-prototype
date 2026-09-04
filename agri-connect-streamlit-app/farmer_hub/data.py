from __future__ import annotations

import pandas as pd


CROPS = {
    "Tomato": {"icon": "🍅", "unit": "₹/kg"},
    "Chilli": {"icon": "🌶️", "unit": "₹/kg"},
    "Rice": {"icon": "🌾", "unit": "₹/kg"},
    "Cotton": {"icon": "☁️", "unit": "₹/kg"},
    "Wheat": {"icon": "🌱", "unit": "₹/kg"},
}

QUALITY_GRADES = {
    "Premium grade": {"adjustment": 1.12, "description": "Clean, fresh, uniform produce"},
    "Standard grade": {"adjustment": 1.00, "description": "Good market-ready produce"},
    "Value grade": {"adjustment": 0.88, "description": "Mixed size or lower visual quality"},
}

MARKETS = pd.DataFrame(
    [
        ["Guntur Market", "Guntur", 16.3067, 80.4365, 22, 105, 32, 68, 30, 5, "NTR Bus Stand · Guntur Railway Station"],
        ["Vijayawada Market", "Vijayawada", 16.5062, 80.6480, 25, 115, 35, 72, 33, 35, "Benz Circle · Vijayawada Railway Station"],
        ["Tenali Market", "Tenali", 16.2430, 80.6400, 23, 110, 33, 70, 31, 30, "Tenali Railway Station · Clock Tower"],
        ["Narasaraopet Market", "Narasaraopet", 16.2342, 80.0490, 24, 108, 31, 69, 29, 45, "Narasaraopet Railway Station · Palnadu Road"],
        ["Bapatla Market", "Bapatla", 15.9042, 80.4670, 21, 102, 34, 71, 32, 50, "Bapatla Beach Road · Railway Station"],
    ],
    columns=["Market", "Location", "Latitude", "Longitude", "Tomato", "Chilli", "Rice", "Cotton", "Wheat", "Distance", "Landmarks"],
)

RENTALS = pd.DataFrame(
    [
        ["Guntur Market", "Vegetable lane A", 450, 1200, "Near NTR Bus Stand"],
        ["Vijayawada Market", "Fresh produce lane 3", 650, 1800, "Near Benz Circle"],
        ["Tenali Market", "Farmer row 2", 350, 900, "Near Clock Tower"],
        ["Narasaraopet Market", "Main yard stall 8", 300, 750, "Near Railway Station"],
        ["Bapatla Market", "Coastal market row 1", 275, 700, "Near Beach Road"],
    ],
    columns=["Market", "Shop", "Daily rent", "Security deposit", "Landmark"],
)

LOCATION_DISTANCE_HINTS = {
    "mangalagiri": {"Guntur": 28, "Vijayawada": 18, "Tenali": 35, "Narasaraopet": 70, "Bapatla": 65},
    "tenali": {"Guntur": 30, "Vijayawada": 32, "Tenali": 3, "Narasaraopet": 68, "Bapatla": 38},
    "guntur": {"Guntur": 5, "Vijayawada": 35, "Tenali": 30, "Narasaraopet": 45, "Bapatla": 50},
    "vijayawada": {"Guntur": 35, "Vijayawada": 5, "Tenali": 32, "Narasaraopet": 65, "Bapatla": 75},
    "bapatla": {"Guntur": 50, "Vijayawada": 75, "Tenali": 38, "Narasaraopet": 85, "Bapatla": 5},
    "narasaraopet": {"Guntur": 45, "Vijayawada": 65, "Tenali": 68, "Narasaraopet": 5, "Bapatla": 85},
}

BUYERS = pd.DataFrame(
    [
        ["ABC Vegetables", "Tomato", 24, "500–2,000 kg", "Vijayawada", "Fresh produce retailer"],
        ["FreshMart", "Tomato", 23, "500–1,500 kg", "Guntur", "Supermarket chain"],
        ["Agro Foods Ltd", "Chilli", 118, "1,000–5,000 kg", "Vijayawada", "Food processor"],
        ["Sri Lakshmi Traders", "Rice", 36, "2,000–10,000 kg", "Tenali", "Grain wholesaler"],
        ["FarmFresh Pvt Ltd", "Cotton", 73, "1,000–5,000 kg", "Guntur", "Textile supplier"],
        ["Green Valley", "Wheat", 35, "500–3,000 kg", "Bapatla", "Flour mill"],
        ["Organic Harvest", "Tomato", 22, "1,000–4,000 kg", "Narasaraopet", "Organic grocer"],
        ["City Farmers Market", "Chilli", 115, "2,000–8,000 kg", "Guntur", "Local market collective"],
    ],
    columns=["Buyer", "Crop", "Price", "Quantity", "Location", "Type"],
)


def market_rows(crop: str) -> pd.DataFrame:
    result = MARKETS[["Market", "Location", crop, "Distance", "Landmarks"]].copy()
    return result.rename(columns={crop: "Price (₹/kg)", "Distance": "Distance (km)"})


def distances_from(location: str) -> dict[str, int]:
    """Return local distance estimates, falling back to the demo regional distances."""
    location_text = location.casefold().strip()
    for place, distances in LOCATION_DISTANCE_HINTS.items():
        if place in location_text:
            return distances
    return dict(zip(MARKETS["Location"], MARKETS["Distance"]))


def apply_quality_price(price: float, grade: str) -> float:
    return round(price * QUALITY_GRADES[grade]["adjustment"], 2)