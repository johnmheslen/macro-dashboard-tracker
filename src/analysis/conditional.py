# import statements
import pandas as pd


def check_yield_curve_inverted(series: pd.Series):
    """
    Check if yield curve is inverted and by how much

    Args:
        series: pd.Series

    Returns:
        {'is_inverted': bool, 'spread': float}
    """


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
    


def check_series_accelerating(series: pd.Series, n_months: int = 3):
    """
    Determine if a given series is accelerating over the last n months
    
    Args:
        series: pd.Series
        n_months: int
    
    Returns:
        {'is_accelerating': bool}
    """

    monthly_changes = series.diff()

    second_diff = monthly_changes.diff()

    if (second_diff.iloc[-n_months:] > 0).all():
        return {
            'is_accelerating': True
        }
    else:
        return {
            'is_accelerating': False
        }



def check_housing_slowdown(housestarts: pd.Series, mortrate: pd.Series, n_months: int=3):
    """
    Determine if Housing Starts have been declining for n months, and Mortgage Rates have be rising for n months

    Args:
        housestarts: pd.Series
        mortrate: pd.Series
        n_months: int = 3

    Returns:
        {'potential_slowdown': True}
    """

    mortrate_monthly = mortrate.resample('ME').last()
    mortrate_monthly_diff = mortrate_monthly.diff()

    housestarts_diff = housestarts.diff()

    if (housestarts_diff.iloc[-n_months:] < 0).all() and (mortrate_monthly_diff.iloc[-n_months:] > 0).all():
            return {
                'potential_slowdown': True,
                'starts_decrease': housestarts.iloc[-n_months] - housestarts.iloc[-1],
                'rates_increase': round(100 * (mortrate_monthly.iloc[-1] - mortrate_monthly.iloc[-n_months]) / mortrate_monthly.iloc[-n_months], 3),
                'n_months': n_months}
    else:
        return {'potential_slowdown': False,
                'starts_decrease': housestarts.iloc[-n_months] - housestarts.iloc[-1],
                'rates_increase': round(100 * (mortrate_monthly.iloc[-1] - mortrate_monthly.iloc[-n_months]) / mortrate_monthly.iloc[-n_months], 3),
                'n_months': n_months}