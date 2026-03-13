"""
correlation.py
-----------------
Bla bla bla
"""

#
# IMPORTS
#

import pandas as pd

#
# PHILLIPS CURVE
#

def phillips_curve_dev(cpi: pd.Series, unemployment: pd.Series, n_months: int):
    """
    Determine if the Phillips Curve is deviating from historical norms.
    
    Args:
        cpi          (pd.Series): The CPIAUCSL series from FRED.
        unemployment (pd.Series): The UNRATE series from FRED.
        n_months     (int): The comparison range used when calculating mean and std.
    
    Returns:
        dict:
            is_deviating     (bool): True if the Phillips Curve is deviating from historical norms
            deviating_spread (float): The absolute difference between current Phillips Curve measurement and rolling mean.
    """
    rolling_p_c = cpi.interpolate().rolling(window=24).corr(other=unemployment.interpolate())

    deviating_spread = abs(rolling_p_c.iloc[-1] - rolling_p_c.iloc[-n_months:].mean())

    if deviating_spread > rolling_p_c.iloc[-n_months:].std():
        return {
            'is_deviating': True,
            'deviating_spread': deviating_spread
        }
    else:
        return {
            'is_deviating': False,
            'deviating_spread': deviating_spread
        }