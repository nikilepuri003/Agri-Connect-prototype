import pandas as pd

# This DataFrame contains sample market prices for different crops.
# Each row is one market and each column is a crop price or useful detail.
market_data = pd.DataFrame({
    "Market": [
        "Guntur Market",
        "Vijayawada Market",
        "Tenali Market",
        "Narasaraopet Market",
        "Bapatla Market"
    ],
    "Location": [
        "Guntur",
        "Vijayawada",
        "Tenali",
        "Narasaraopet",
        "Bapatla"
    ],
    "Latitude": [16.3067, 16.5062, 16.2430, 16.2342, 15.9042],
    "Longitude": [80.4365, 80.6480, 80.6400, 80.0490, 80.4670],
    "Tomato": [22, 25, 23, 24, 21],
    "Chilli": [105, 115, 110, 108, 102],
    "Rice": [32, 35, 33, 31, 34],
    "Cotton": [68, 72, 70, 69, 71],
    "Wheat": [30, 33, 31, 29, 32],
    "Distance": [5, 35, 30, 45, 50]
})