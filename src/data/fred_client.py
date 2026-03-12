"""
fred_client.py
──────────────
Thin wrapper around the fredapi library.

Provides two simple accessors used by the rest of the project:
    get_series(series_key)   – fetch the full time series as a pd.Series
    get_frequency(series_key) – return the update frequency string

The FRED API key is loaded from a .env file via python-dotenv so it never
has to be hard-coded anywhere in the project.
"""

from src.data.series_config import SERIES
from fredapi import Fred
from dotenv import load_dotenv
import os

# ─────────────────────────────────────────────────────────────────────────────
# CLIENT INITIALISATION
# ─────────────────────────────────────────────────────────────────────────────

# Load environment variables from .env so FRED_API_KEY is available
load_dotenv()

# Instantiate a single shared FRED client for the entire application
fred = Fred(api_key=os.getenv('FRED_API_KEY'))


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def get_series(series_key: str):
    """Fetch a complete FRED time series by its project alias.

    Looks up the official FRED series ID in the SERIES registry, then
    retrieves the full history from the FRED API.

    Args:
        series_key (str): Project alias defined in series_config.SERIES
                          (e.g. 'cpi', 'unemployment').

    Returns:
        pd.Series: Indexed by date, containing all available observations.
    """
    # Translate the friendly alias into the canonical FRED series ID
    series_id = SERIES[series_key]['id']
    return fred.get_series(series_id)


def get_frequency(series_key: str) -> str:
    """Return the update frequency for a given series.

    Used by analysis modules (e.g. historical.py) to convert a
    human-readable frequency label into the correct number of periods
    for slicing and resampling.

    Args:
        series_key (str): Project alias defined in series_config.SERIES.

    Returns:
        str: One of 'daily', 'weekly', 'monthly', 'quarterly', 'annual'.
    """
    return SERIES[series_key]['frequency']
