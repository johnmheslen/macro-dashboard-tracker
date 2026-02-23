from src.data.fred_client import get_series

# Checking Conditional analysis function 1
# yield_curve = get_series('t10y2y')
# from src.analysis.conditional import check_yield_curve_inverted
# print(check_yield_curve_inverted(yield_curve))

# Checking Conditional analysis function 2
cpi = get_series('cpi')
# from src.analysis.conditional import check_series_accelerating
# print(check_series_accelerating(cpi, 6))

# Checking Conditional analysis function 3
mortrate = get_series('mortgage_rate')
housestarts = get_series('housing_starts')
from src.analysis.conditional import check_housing_slowdown
print(check_housing_slowdown(housestarts, mortrate, 6))

mortrate_monthly = mortrate.resample("ME").last()

print(mortrate_monthly.iloc[-8:])

