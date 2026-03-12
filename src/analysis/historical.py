"""
historical.py
─────────────
Historical context module for the macro dashboard.

Provides percentile-based ranking so a single indicator reading can be
understood relative to its own history.  For example: "the current CPI
reading is in the 94th percentile of the last 5 years" conveys far more
than a raw number alone.
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

import pandas as pd
from scipy.stats import percentileofscore
from src.data.fred_client import get_series, get_frequency

# ─────────────────────────────────────────────────────────────────────────────
# FREQUENCY → PERIODS-PER-YEAR LOOKUP
# ─────────────────────────────────────────────────────────────────────────────

# Maps each series frequency to the number of data points expected per year.
# Used to convert a user-supplied year range into the correct number of rows
# to slice from the tail of the series.
freq_map = {
    'daily':     365,
    'weekly':     52,
    'monthly':    12,
    'quarterly':   4,
    'annual':      1,
}


# ─────────────────────────────────────────────────────────────────────────────
# ANALYSIS FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def historical_comparison(indicator: str, range: int) -> float:
    """Rank the most recent reading of an indicator against its own history.

    Fetches the full series, isolates the trailing window defined by
    ``range`` years, and returns where the latest observation falls within
    that window as a percentile (0–100).

    Args:
        indicator (str): Project alias for the FRED series
                         (e.g. 'cpi', 'fed_funds_rate').
        range (int):     How many years of history to use as the comparison
                         window (e.g. 5 = last 5 years of data).

    Returns:
        float: Percentile rank of the current reading within the historical
               window.  0 = all-time low end, 100 = all-time high end.
               Uses 'strict' scoring so ties rank below the current value.
    """
    # Pull the complete series from FRED
    indic_series = get_series(indicator)

    # Capture the single most recent data point we want to rank
    current_reading = indic_series.iloc[-1]

    # Determine how many observations correspond to the requested year range.
    # e.g. monthly series × 5 years = 60 observations
    n_periods = freq_map[get_frequency(indicator)] * range

    # Slice the trailing window and compute the percentile rank.
    # nan_policy='omit' ensures missing observations don't break the score.
    return percentileofscore(
        indic_series.iloc[-n_periods:],
        current_reading,
        kind='strict',
        nan_policy='omit'
    )
