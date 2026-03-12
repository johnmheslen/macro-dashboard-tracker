"""
trends.py
─────────
Trend deviation analysis for the macro dashboard.

Detects when a macroeconomic indicator's recent rate-of-change has broken
outside its own trailing norm.  Both year-over-year (YoY) and
month-over-month (MoM) flavours are provided so callers can choose the
appropriate time horizon.

Logic overview
──────────────
  1. Compute the rolling % change for the chosen period (12 months or 1 month).
  2. Take the last 13 observations as the "recent norm" window — this covers
     exactly one year of changes plus the current reading.
  3. Flag deviation when the latest reading is more than one standard deviation
     away from the window mean.
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

from fredapi import Fred
from dotenv import load_dotenv
import os
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# CLIENT SETUP  (kept here for standalone usage of this module)
# ─────────────────────────────────────────────────────────────────────────────

load_dotenv()
fred = Fred(api_key=os.getenv('FRED_API_KEY'))


# ─────────────────────────────────────────────────────────────────────────────
# DEVIATION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def is_yoy_deviating(indic: pd.Series, name: str = "Unknown") -> bool:
    """Detect whether the latest year-over-year change is outside the norm.

    Computes 12-month % changes for the whole series, then checks if the
    most recent value sits more than one standard deviation from the mean
    of the last 13 monthly readings.

    Args:
        indic (pd.Series): Full time series for the indicator.
        name  (str):       Display label used in printed output.

    Returns:
        bool: True if the latest YoY change deviates by more than 1 std dev,
              False otherwise.
    """
    # Compute rolling 12-month (YoY) percentage change for every observation
    indic_pct_change = indic.pct_change(periods=12)

    # Summarise the trailing 13-period window (1 year of YoY readings)
    indic_pct_change_mean = indic_pct_change.iloc[-13:].mean()
    indic_pct_change_std  = indic_pct_change.iloc[-13:].std()

    # ── Diagnostic printout ──────────────────────────────────────────────────
    print(f"\nIndicator: {name.upper()}")
    print(f"\n\tMost recent YoY: {indic_pct_change.iloc[-1]}")
    print(f"\tMean:             {indic_pct_change_mean}")
    print(f"\tStd:              {indic_pct_change_std}")
    print(f"\tDeviation:        {abs(indic_pct_change.iloc[-1] - indic_pct_change_mean)}")

    # Deviation is flagged when the absolute gap from the mean exceeds 1 std dev
    if abs(indic_pct_change.iloc[-1] - indic_pct_change_mean) > indic_pct_change_std:
        print("\nIndiciator deviating.")
        return True
    else:
        print("\nIndicator not deviating.")
        return False


def is_mom_deviating(indic: pd.Series, name: str = "Unknown") -> bool:
    """Detect whether the latest month-over-month change is outside the norm.

    Same logic as is_yoy_deviating but uses a 1-month % change instead of
    12-month, making it more sensitive to short-term momentum shifts.

    Args:
        indic (pd.Series): Full time series for the indicator.
        name  (str):       Display label used in printed output.

    Returns:
        bool: True if the latest MoM change deviates by more than 1 std dev,
              False otherwise.
    """
    # Compute rolling 1-month (MoM) percentage change for every observation
    indic_pct_change = indic.pct_change(periods=1)

    # Summarise the trailing 13-period window
    indic_pct_change_mean = indic_pct_change.iloc[-13:].mean()
    indic_pct_change_std  = indic_pct_change.iloc[-13:].std()

    # ── Diagnostic printout ──────────────────────────────────────────────────
    print(f"\nIndicator: {name.upper()}")
    print(f"Most recent MoM: {indic_pct_change.iloc[-1]}")
    print(f"Mean:            {indic_pct_change_mean}")
    print(f"Std:             {indic_pct_change_std}")
    print(f"Deviation:       {abs(indic_pct_change.iloc[-1] - indic_pct_change_mean)}")

    # Same threshold as YoY: flag when gap from mean exceeds 1 std dev
    if abs(indic_pct_change.iloc[-1] - indic_pct_change_mean) > indic_pct_change_std:
        print("\nIndicator deviating.")
        return True
    else:
        print("\nIndicator not deviating.")
        return False
