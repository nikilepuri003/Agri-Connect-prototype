from src.data.buyer_data import buyers

def match_buyers(crop):
    """
    Matches farmers with potential buyers based on the selected crop.

    Parameters:
    crop (str): The crop for which to find matching buyers.

    Returns:
    DataFrame: A DataFrame containing buyers interested in the specified crop.
    """
    matching_buyers = buyers[buyers["Crop"] == crop]
    return matching_buyers.reset_index(drop=True)