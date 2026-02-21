# Imports
import pandas as pd
from scipy.stats import percentileofscore 
from src.data.fred_client import get_series
from src.data.fred_client import get_frequency

# Map frequencies
freq_map = {
    'monthly': 12,
    'quarterly': 4,
    'annual': 1,
    'daily': 365
}

# Create historical comparison function

def historical_comparison(indicator: str, range: int):
    """A function to compare current indicator reading to historical ranges.
    
    Args:
        indicator (string): The indicator variable we are analyzing.
        range (int): The range of time we are analyzing our reading over.

    Returns:
        ranking (float): Percentile of current reading compared to historical range.
    """

    # Get series from indicator parameter
    indic_series = get_series(indicator)

    # Get most recent reading from indicator series
    current_reading = indic_series.iloc[-1]

    # Get and return percentile of current_reading
    return percentileofscore(indic_series.iloc[-1*freq_map[get_frequency(indicator)]*range:], current_reading, kind='strict', nan_policy='omit')
