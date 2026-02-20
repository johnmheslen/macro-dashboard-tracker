from fredapi import Fred
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
fred = Fred(api_key=os.getenv('FRED_API_KEY'))



# Year over Year Trend Analysis
def is_yoy_deviating(indic: pd.Series, name: str = "Unknown"):
    """A function to test if recent YoY calculation is deviating from the norm.
    
    Args:
        indic (pd.Series): The indicator variable we are analyzing.
        name (string): The name of the indicator variable.

    Returns:
        True or False
    """

    indic_pct_change = indic.pct_change(periods=12)

    indic_pct_change_mean = indic_pct_change.iloc[-13:].mean()
    indic_pct_change_std = indic_pct_change.iloc[-13:].std()

    print(f"\nIndicator: {name.upper()}")
    print(f"\n\tMost recent YoY: {indic_pct_change.iloc[-1]}")
    print(f"\tMean: {indic_pct_change_mean}")
    print(f"\tStd: {indic_pct_change_std}")
    print(f"\tDeviation: {abs(indic_pct_change.iloc[-1] - indic_pct_change_mean)}")

    if abs(indic_pct_change.iloc[-1] - indic_pct_change_mean) > indic_pct_change_std:
        print("\nIndiciator deviating.")
        return True
    else:
        print("\nIndicator not deviating.")
        return False


# Month over Month Trend Analysis
def is_mom_deviating(indic: pd.Series, name: str = "Unknown"):
    """A function to test if recent MoM calculation is deviating from the norm.
    
    Args:
        indic (pd.Series): The indicator variable we are analyzing.
        name (string): The name of the indicator variable.

    Returns:
        True or False
    """

    indic_pct_change = indic.pct_change(periods=1)

    indic_pct_change_mean = indic_pct_change.iloc[-13:].mean()
    indic_pct_change_std = indic_pct_change.iloc[-13:].std()

    print(f"\nIndicator: {name.upper()}")
    print(f"Most recent MoM: {indic_pct_change.iloc[-1]}")
    print(f"Mean: {indic_pct_change_mean}")
    print(f"Std: {indic_pct_change_std}")
    print(f"Deviation: {abs(indic_pct_change.iloc[-1] - indic_pct_change_mean)}")

    if abs(indic_pct_change.iloc[-1] - indic_pct_change_mean) > indic_pct_change_std:
        print("\nIndicator deviating.")
        return True
    else:
        print("\nIndicator not deviating.")
        return False