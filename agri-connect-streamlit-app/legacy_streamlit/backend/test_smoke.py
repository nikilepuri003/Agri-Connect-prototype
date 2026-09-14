from backend.maps import google_maps_directions_url, google_maps_url
from backend.voice import crop_from_voice
from db.data import BUYERS, CROPS, MARKETS, QUALITY_GRADES, RENTALS, apply_quality_price, distances_from, market_rows


def test_data_and_crop_matching() -> None:
    assert set(CROPS) == {"Tomato", "Chilli", "Rice", "Cotton", "Wheat"}
    assert len(MARKETS) == len(RENTALS) == 5
    assert len(BUYERS) > 0
    assert crop_from_voice("I want to sell mirchi") == "Chilli"
    assert crop_from_voice("నేను టమాటా అమ్మాలి") == "Tomato"
    assert "Price (₹/kg)" in market_rows("Rice")


def test_map_links_are_actionable() -> None:
    assert google_maps_url("Guntur") == "https://www.google.com/maps/search/?api=1&query=Guntur+market"
    assert "destination=Guntur+market" in google_maps_directions_url("Guntur")


def test_location_aware_distances() -> None:
    assert distances_from("Mangalagiri")['Vijayawada'] == 18
    assert distances_from("Tenali village")['Tenali'] == 3


def test_quality_changes_price() -> None:
    assert apply_quality_price(100, "Premium grade") == 112
    assert apply_quality_price(100, "Standard grade") == 100
    assert apply_quality_price(100, "Value grade") == 88
    assert len(QUALITY_GRADES) == 3