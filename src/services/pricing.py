import pandas as pd

def calculate_transport_cost(distance, rate_per_kg=0.05):
    return distance * rate_per_kg

def calculate_net_price(market_price, transport_cost, quality_factor):
    adjusted_price = market_price * quality_factor
    net_price = adjusted_price - transport_cost
    return net_price

def calculate_expected_revenue(net_price, quantity):
    return net_price * quantity

def get_best_market(prices_df, quantity, quality):
    quality_factors = {
        "A": 1.00,
        "B": 0.90,
        "C": 0.80
    }
    
    quality_factor = quality_factors.get(quality, 1.00)
    
    prices_df["Transport Cost/kg"] = prices_df["Distance"].apply(calculate_transport_cost)
    prices_df["Adjusted Price"] = prices_df["Market Price"] * quality_factor
    prices_df["Net Price/kg"] = prices_df.apply(lambda row: calculate_net_price(row["Adjusted Price"], row["Transport Cost/kg"], quality_factor), axis=1)
    prices_df["Expected Revenue"] = prices_df["Net Price/kg"] * quantity
    
    best_market = prices_df.loc[prices_df["Expected Revenue"].idxmax()]
    return best_market, prices_df

def prepare_market_data(market_data, crop):
    prices = market_data[["Market", "Location", crop, "Distance"]].copy()
    prices.rename(columns={crop: "Market Price"}, inplace=True)
    return prices