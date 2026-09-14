import requests


def get_location_data(address):
    """
    Fetches location data from the Google Maps Geocoding API.
    """

    api_key = "YOUR_GOOGLE_MAPS_API_KEY"

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data["results"]:
            location = data["results"][0]["geometry"]["location"]

            return {
                "latitude": location["lat"],
                "longitude": location["lng"]
            }

        return None

    return None


def get_nearby_markets(latitude, longitude, radius=5000):
    """
    Fetches nearby markets from the Google Places API.
    """

    api_key = "YOUR_GOOGLE_MAPS_API_KEY"

    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{latitude},{longitude}",
        "radius": radius,
        "type": "market",
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:

        data = response.json()

        markets = []

        for place in data.get("results", []):

            markets.append({
                "name": place["name"],
                "location": place["geometry"]["location"]
            })

        return markets

    return []


def get_map_data(latitude, longitude):
    """
    Returns map data for displaying a location in Streamlit.
    """

    return {
        "latitude": latitude,
        "longitude": longitude
    }