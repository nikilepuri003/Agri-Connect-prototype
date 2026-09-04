import pandas as pd

# This DataFrame stores sample buyers who are willing to purchase crops.
# It includes their crop preferences, price offers, quantity requirements,
# and their city location.
buyers = pd.DataFrame({
    "Buyer": [
        "ABC Vegetables",
        "FreshMart",
        "Agro Foods Ltd",
        "Sri Lakshmi Traders",
        "FarmFresh Pvt Ltd",
        "Green Valley",
        "Organic Harvest",
        "City Farmers Market",
        "Harvest Hub",
        "Local Produce Co."
    ],
    "Crop": [
        "Tomato",
        "Tomato",
        "Chilli",
        "Rice",
        "Cotton",
        "Wheat",
        "Tomato",
        "Chilli",
        "Rice",
        "Cotton"
    ],
    "Price": [
        24,
        23,
        118,
        36,
        73,
        25,
        22,
        115,
        34,
        70
    ],
    "Required Quantity": [
        "500-2000 kg",
        "500-1500 kg",
        "1000-5000 kg",
        "2000-10000 kg",
        "1000-5000 kg",
        "500-3000 kg",
        "1000-4000 kg",
        "2000-8000 kg",
        "1500-6000 kg",
        "1000-3000 kg"
    ],
    "Location": [
        "Vijayawada",
        "Guntur",
        "Vijayawada",
        "Tenali",
        "Guntur",
        "Bapatla",
        "Narasaraopet",
        "Guntur",
        "Tenali",
        "Bapatla"
    ]
})