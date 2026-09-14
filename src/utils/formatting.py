def format_currency(value):
    """Format a numeric value as currency."""
    return f"₹{value:,.2f}"

def format_quantity(value):
    """Format quantity for display."""
    return f"{value} kg"

def format_percentage(value):
    """Format a percentage value for display."""
    return f"{value:.2f}%"

def format_distance(value):
    """Format distance for display."""
    return f"{value} km"

def format_revenue(value):
    """Format revenue for display."""
    return f"₹{value:,.0f}"