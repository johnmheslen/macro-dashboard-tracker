# Install dependencies
from fredapi import Fred
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
fred = Fred(api_key=os.getenv('FRED_API_KEY'))


# Pull CPI data
cpi = fred.get_series('CPIAUCSL')
print(cpi)

# Pull Unemployment data
unemployment = fred.get_series('UNRATE')


# Calculate MoM CPIAUCSL trend
cpi_mom = (cpi[-1] - cpi[-2]) / cpi[-2]

# Calculate YoY CPIAUCSL trend
cpi_yoy = (cpi.iloc[-1] - cpi.iloc[-13]) / cpi.iloc[-13]

def is_deviating(sample: pd.Series):
    """Function for determining if an indicator is trending away from mean by more than 1 standard deviation."""
    sample_yoy = (sample.iloc[-1] - sample.iloc[-13]) / sample.iloc[-13]
    sample_mean = sample.iloc[-13:].mean()
    sample_std = sample.iloc[-13:].std()

    print(f"Sample mean: {sample_mean}")
    print(f"Sample standard dev: {sample_std}")

    if (abs(sample_yoy - sample_mean) / sample_std) > 1:
        return True
    else:
        return False
    

print(f"Sample is deviating?: {is_deviating(cpi)}")

print(cpi.iloc[-13:])

print(f"CPI YoY: {cpi_yoy}")

cpi_pct_change = cpi.pct_change(periods=12)



def is_indic_deviating(indic: pd.Series, name: str = "Unknown"):
    """A function to test if recent YoY calculation is deviating from the norm."""

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
    else:
        print("\nIndicator not deviating.")



is_indic_deviating(cpi, 'CPIAUCSL')
is_indic_deviating(unemployment, 'unemployment')
