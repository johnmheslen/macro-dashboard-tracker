"""
conditional.py
──────────────
Event-detection checks for the macro dashboard.

Each function in this module inspects one or more FRED time series and
returns a plain dict describing whether a specific macroeconomic condition
is currently active, along with supporting metrics.

Return dicts are intentionally flat and JSON-serialisable so they can be
consumed directly by downstream reporting or alerting layers.
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

import pandas as pd


# ─────────────────────────────────────────────────────────────────────────────
# YIELD CURVE
# ─────────────────────────────────────────────────────────────────────────────

def check_yield_curve_inverted(series: pd.Series) -> dict:
    """Check whether the yield curve is currently inverted.

    An inverted yield curve (10-year minus 2-year Treasury spread < 0) is a
    historically reliable leading indicator of recession.

    Args:
        series (pd.Series): The T10Y2Y spread series from FRED.
                            Positive = normal, negative = inverted.

    Returns:
        dict:
            is_inverted (bool):  True if the most recent spread is negative.
            spread      (float): The current spread value (percentage points).
    """
    # A negative spread means the 2-year yield exceeds the 10-year yield
    if series[-1] < 0:
        return {
            'is_inverted': True,
            'spread': series.iloc[-1]
        }
    else:
        return {
            'is_inverted': False,
            'spread': series.iloc[-1]
        }


# ─────────────────────────────────────────────────────────────────────────────
# SERIES MOMENTUM
# ─────────────────────────────────────────────────────────────────────────────

def check_series_accelerating(series: pd.Series, n_months: int = 3) -> dict:
    """Determine whether a series is accelerating over the last n months.

    Acceleration here means the first-order differences are themselves
    growing — i.e. the second derivative of the series is positive for
    every period in the window.

    Args:
        series   (pd.Series): Any monthly macroeconomic series.
        n_months (int):       Number of recent months to evaluate.
                              Defaults to 3.

    Returns:
        dict:
            is_accelerating (bool): True if the second-difference was
                                    positive for all n_months periods.
    """
    # First difference: change between consecutive periods
    monthly_changes = series.diff()

    # Second difference: how the rate-of-change is itself changing.
    # Positive = the changes are getting bigger → acceleration.
    second_diff = monthly_changes.diff()

    # All values in the window must be positive for true acceleration
    if (second_diff.iloc[-n_months:] > 0).all():
        return {'is_accelerating': True}
    else:
        return {'is_accelerating': False}


# ─────────────────────────────────────────────────────────────────────────────
# HOUSING MARKET
# ─────────────────────────────────────────────────────────────────────────────

def check_housing_slowdown(
    housestarts: pd.Series,
    mortrate:    pd.Series,
    n_months:    int = 3
) -> dict:
    """Detect a potential housing-market slowdown.

    Flags a slowdown when *both* of the following are true over the
    last n months:
        • Housing starts have been declining every month.
        • The 30-year mortgage rate has been rising every month.

    The mortgage rate series is weekly, so it is resampled to monthly
    (taking the last weekly reading in each month) before differencing.

    Args:
        housestarts (pd.Series): Monthly housing starts (HOUST).
        mortrate    (pd.Series): Weekly 30-year fixed mortgage rate
                                 (MORTGAGE30US).
        n_months    (int):       Lookback window in months. Defaults to 3.

    Returns:
        dict:
            potential_slowdown (bool):  True when both conditions are met.
            starts_decrease    (float): Absolute drop in starts over the window
                                        (housestarts[−n] − housestarts[−1]).
            rates_increase     (float): Percentage increase in mortgage rate
                                        over the window (basis points × 100).
            n_months           (int):   The lookback window used.
    """
    # ── Resample mortgage rate from weekly → monthly ─────────────────────────
    # 'ME' = Month End frequency; .last() keeps the final weekly reading
    mortrate_monthly      = mortrate.resample('ME').last()
    mortrate_monthly_diff = mortrate_monthly.diff()   # month-on-month change

    # ── First difference of housing starts ───────────────────────────────────
    housestarts_diff = housestarts.diff()

    # ── Pre-compute summary metrics (returned regardless of outcome) ─────────
    starts_decrease = housestarts.iloc[-n_months] - housestarts.iloc[-1]
    rates_increase  = round(
        100 * (mortrate_monthly.iloc[-1] - mortrate_monthly.iloc[-n_months])
            / mortrate_monthly.iloc[-n_months],
        3
    )

    # Both starts must fall AND rates must rise for every period in the window
    if (housestarts_diff.iloc[-n_months:] < 0).all() and \
       (mortrate_monthly_diff.iloc[-n_months:] > 0).all():
        return {
            'potential_slowdown': True,
            'starts_decrease':    starts_decrease,
            'rates_increase':     rates_increase,
            'n_months':           n_months
        }
    else:
        return {
            'potential_slowdown': False,
            'starts_decrease':    starts_decrease,
            'rates_increase':     rates_increase,
            'n_months':           n_months
        }


# ─────────────────────────────────────────────────────────────────────────────
# LABOR MARKET
# ─────────────────────────────────────────────────────────────────────────────

def check_unemployment_drop(unrate: pd.Series) -> dict:
    """Determine whether the unemployment rate is below 4%.

    A sub-4% unemployment rate is commonly used as a threshold for a
    "tight" labor market, which can signal inflationary wage pressure.

    Args:
        unrate (pd.Series): Monthly unemployment rate series (UNRATE).

    Returns:
        dict:
            below_4pct    (bool):  True if the latest reading is < 4.0.
            current_unrate (float): The most recent unemployment rate value.
    """
    if unrate.iloc[-1] < 4:
        return {
            'below_4pct':     True,
            'current_unrate': unrate.iloc[-1]
        }
    else:
        return {
            'below_4pct':     False,
            'current_unrate': unrate.iloc[-1]
        }


# ─────────────────────────────────────────────────────────────────────────────
# MONETARY POLICY
# ─────────────────────────────────────────────────────────────────────────────

def check_fed_rate_change(fed_rate: pd.Series) -> dict:
    """Detect whether the Federal Funds Rate changed in the most recent period.

    Compares the last two monthly observations.  Any non-zero difference
    indicates the Fed moved rates at its most recent meeting.

    Args:
        fed_rate (pd.Series): Monthly effective federal funds rate (FEDFUNDS).

    Returns:
        dict:
            rate_changed   (bool):  True if the rate moved between the last
                                    two observations.
            change_amount  (float): Signed difference (positive = hike,
                                    negative = cut), in percentage points.
    """
    change_amount = fed_rate.iloc[-1] - fed_rate.iloc[-2]

    if fed_rate.iloc[-1] != fed_rate.iloc[-2]:
        return {
            'rate_changed':  True,
            'change_amount': change_amount
        }
    else:
        return {
            'rate_changed':  False,
            'change_amount': change_amount
        }


# ─────────────────────────────────────────────────────────────────────────────
# COMMODITIES
# ─────────────────────────────────────────────────────────────────────────────

def check_oil_spike(crude_oil: pd.Series) -> dict:
    """Detect a sharp spike in crude oil prices over the past 30 days.

    A ≥15% rise in WTI crude over 30 calendar days is flagged as a spike.
    Because the series is daily and may have gaps (weekends/holidays),
    pd.Series.asof() is used to find the closest available price to the
    30-day lookback date rather than assuming a fixed integer offset.

    Args:
        crude_oil (pd.Series): Daily WTI crude oil price series (DCOILWTICO).

    Returns:
        dict:
            oil_spike      (bool):  True if price rose ≥15% over 30 days.
            oil_pct_change (float): Actual percentage change (as a decimal,
                                    e.g. 0.18 = 18% increase).
    """
    # Most recent available trading date
    crude_date = crude_oil.index[-1]

    # Target lookback date — 30 calendar days prior
    crude_date_back = crude_date - pd.DateOffset(days=30)

    # asof() returns the last valid price on or before crude_date_back,
    # handling weekends and holidays gracefully
    crude_date_back_value = crude_oil.asof(crude_date_back)

    pct_change = (crude_oil.iloc[-1] - crude_date_back_value) / crude_date_back_value

    # Threshold: 15% (1.15×) rise constitutes a spike
    if crude_oil.iloc[-1] > crude_date_back_value * 1.15:
        return {
            'oil_spike':      True,
            'oil_pct_change': pct_change
        }
    else:
        return {
            'oil_spike':      False,
            'oil_pct_change': pct_change
        }
