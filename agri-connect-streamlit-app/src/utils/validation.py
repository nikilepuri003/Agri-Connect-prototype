def validate_crop_selection(crop):
    valid_crops = ["Tomato", "Chilli", "Rice", "Cotton", "Wheat"]
    if crop not in valid_crops:
        raise ValueError(f"Invalid crop selection: {crop}. Please choose from {valid_crops}.")

def validate_quantity(quantity):
    if quantity < 100 or quantity > 100000:
        raise ValueError("Quantity must be between 100 and 100000 kg.")

def validate_location(location):
    valid_locations = ["Guntur", "Vijayawada", "Tenali", "Narasaraopet", "Bapatla"]
    if location not in valid_locations:
        raise ValueError(f"Invalid location: {location}. Please choose from {valid_locations}.")

def validate_quality(quality):
    valid_qualities = ["A", "B", "C"]
    if quality not in valid_qualities:
        raise ValueError(f"Invalid quality selection: {quality}. Please choose from {valid_qualities}.")