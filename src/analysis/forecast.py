"""
forecast.py
---------------------
"""
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def forecast_series(series: pd.Series, n_periods: int = 3, order: tuple = (1, 1, 1)):
    """
    Generate ARIMA forecast for a given series.
    
    Args:
        series: pd.Series of the indicator
        n_periods: how many periods ahead to forecast
        order: (p, d, q) tuple for ARIMA
        
    Returns:
        dict with 'metadata' and 'forecasts' keys
    """

    # Fit the model
    model = ARIMA(series, order=order)
    fitted = model.fit()

    # Get forecast with confidence intervals
    forecast_result = fitted.get_forecast(steps=n_periods)
    forecast_values = forecast_result.predicted_mean
    confidence_intervals = forecast_result.conf_int()

    # TODO: Build your forecast lists here
    # forecast_values is a Series of predicted values
    # confidence_intervals is a DataFrame with 'lower' and 'upper' columns
    # Loop through each period and build the dict structure you designed

    # TODO: Calculate mom_change for each forecasted period
    # Hint: you need the last actual value from the original series
    # as your starting point for the first period's pct_change
    
    forecasts = []
    for i in range(len(forecast_values)):
        if i == 0:
            mom_change = (forecast_values.iloc[i] - series.iloc[-1])/series.iloc[-1]
        else:
            mom_change = (forecast_values.iloc[i] - forecast_values.iloc[i-1])/forecast_values.iloc[i-1]

        forecasts.append({
            'period': i+1,
            'value': forecast_values.iloc[i],
            'ci': confidence_intervals.iloc[i].tolist(),
            'mom_change': mom_change
        })

    return {
        'metadata': {
            'n_periods': n_periods,
            'inputs': order
        },
        'forecasts': forecasts
    }