"""
starting_point.py
─────────────────
Initial exploration / scratchpad script.

This file was used to prototype the core deviation-detection logic before
it was refactored into the src/ package.  It pulls CPI and unemployment
data directly from FRED and contains two generations of the is_deviating
helper — the second (is_indic_deviating) is the one that graduated into
src/analysis/trends.py.
"""

# ─────────────────────────────────────────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────────────────────────────────────────

from fredapi import Fred
from dotenv import load_dotenv
import os
import pandas as pd

# Load FRED_API_KEY from .env before initialising the client
load_dotenv()
fred = Fred(api_key=os.getenv('FRED_API_KEY'))


# ─────────────────────────────────────────────────────────────────────────────
# DATA PULLS
# ─────────────────────────────────────────────────────────────────────────────

# Pull CPI data (All Urban Consumers, seasonally adjusted)
cpi = fred.get_series('CPIAUCSL')
print(cpi)

# Pull Unemployment data (U-3 headline rate)
unemployment = fred.get_series('UNRATE')


# ─────────────────────────────────────────────────────────────────────────────
# QUICK CALCULATIONS
# ─────────────────────────────────────────────────────────────────────────────

# Month-over-month CPI change (raw difference, not %)
cpi_mom = (cpi[-1] - cpi[-2]) / cpi[-2]

# Year-over-year CPI change: compare most recent to 13 months ago
# (iloc[-13] = same month last year, accounting for 0-indexing)
cpi_yoy = (cpi.iloc[-1] - cpi.iloc[-13]) / cpi.iloc[-13]


# ─────────────────────────────────────────────────────────────────────────────
# VERSION 1 — is_deviating  (prototype, z-score based)
# ─────────────────────────────────────────────────────────────────────────────

def is_deviating(sample: pd.Series) -> bool:
    """Determine if an indicator's YoY reading is more than 1 std dev from its mean.

    First-generation prototype.  Computes a modified z-score using the raw
    series values (not % changes) over the last 13 observations.

    Args:
        sample (pd.Series): Full time series for the indicator.

    Returns:
        bool: True if |z-score| > 1, False otherwise.
    """
    # YoY change as a ratio
    sample_yoy  = (sample.iloc[-1] - sample.iloc[-13]) / sample.iloc[-13]

    # Trailing 13-period stats (covers the same 1-year window used for YoY)
    sample_mean = sample.iloc[-13:].mean()
    sample_std  = sample.iloc[-13:].std()

    print(f"Sample mean:        {sample_mean}")
    print(f"Sample standard dev: {sample_std}")

    # Flag if the YoY reading sits more than one std dev from the recent mean
    if (abs(sample_yoy - sample_mean) / sample_std) > 1:
        return True
    else:
        return False


print(f"Sample is deviating?: {is_deviating(cpi)}")
print(cpi.iloc[-13:])
print(f"CPI YoY: {cpi_yoy}")

# Compute the full rolling YoY % change series for inspection
cpi_pct_change = cpi.pct_change(periods=12)


# ─────────────────────────────────────────────────────────────────────────────
# VERSION 2 — is_indic_deviating  (refactored, % change based)
# ─────────────────────────────────────────────────────────────────────────────

def is_indic_deviating(indic: pd.Series, name: str = "Unknown"):
    """Test if the most recent YoY % change deviates from the trailing norm.

    Second-generation prototype — operates on pct_change rather than raw
    values, which makes the deviation signal more comparable across series
    with very different scales.  This version was later promoted to
    src/analysis/trends.is_yoy_deviating().

    Args:
        indic (pd.Series): Full time series for the indicator.
        name  (str):       Display label for the printed output.

    Returns:
        None: Prints the result; return value added in the final version.
    """
    # Rolling 12-month % change for every observation
    indic_pct_change = indic.pct_change(periods=12)

    # Trailing 13-period stats on the % change series
    indic_pct_change_mean = indic_pct_change.iloc[-13:].mean()
    indic_pct_change_std  = indic_pct_change.iloc[-13:].std()

    # ── Diagnostic output ────────────────────────────────────────────────────
    print(f"\nIndicator: {name.upper()}")
    print(f"\n\tMost recent YoY: {indic_pct_change.iloc[-1]}")
    print(f"\tMean:             {indic_pct_change_mean}")
    print(f"\tStd:              {indic_pct_change_std}")
    print(f"\tDeviation:        {abs(indic_pct_change.iloc[-1] - indic_pct_change_mean)}")

    # Flag when the absolute gap from the mean exceeds one standard deviation
    if abs(indic_pct_change.iloc[-1] - indic_pct_change_mean) > indic_pct_change_std:
        print("\nIndiciator deviating.")
    else:
        print("\nIndicator not deviating.")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

is_indic_deviating(cpi, 'CPIAUCSL')
is_indic_deviating(unemployment, 'unemployment')
