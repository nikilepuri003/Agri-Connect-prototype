import os

from backend.server import REGIONAL_MANDI_HUBS, query_openai_markets


def handler(request):
    payload = request.get_json() if hasattr(request, "get_json") else {}
    location = str(payload.get("location", "")).strip()
    crop = str(payload.get("crop", "Tomato")).strip()
    if not location:
        return {"statusCode": 400, "body": {"error": "Location is required"}}

    markets = []
    source = "kisan_spatial_engine"
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key:
        try:
            markets = query_openai_markets(api_key, location, crop)
            source = "openai"
        except Exception:
            markets = []

    if not markets:
        location_lower = location.casefold()
        for hub, hub_markets in REGIONAL_MANDI_HUBS.items():
            if hub in location_lower:
                markets = hub_markets
                break
    if not markets:
        town = location.title()
        markets = [{"market": f"{town} APMC Main Mandi", "location": town, "latitude": 16.3, "longitude": 80.4, "prices": {"Tomato": 24, "Chilli": 110, "Rice": 33, "Cotton": 70, "Wheat": 31}, "distance": 6, "landmarks": f"{town} Rythu Bazar · Main Bus Depot"}]

    rentals = [{"market": market["market"], "shop": f"{market['location']} Stall #1", "daily_rent": 350, "security_deposit": 800, "landmark": market.get("landmarks", "Main Yard Lane")} for market in markets]
    return {"statusCode": 200, "body": {"markets": markets, "rentals": rentals, "source": source}}
