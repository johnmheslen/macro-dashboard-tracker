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
# from src.analysis.conditional import check_housing_slowdown
# print(check_housing_slowdown(housestarts, mortrate, 6))

# mortrate_monthly = mortrate.resample("ME").last()

# print(mortrate_monthly.iloc[-8:])

# Checking Conditional analysis function 4
from src.analysis.conditional import check_unemployment_drop
unrate = get_series('unemployment')
print(check_unemployment_drop(unrate))


# ---------- Checking Conditional analysis functin 4 ----------
from src.analysis.conditional import check_fed_rate_change
fed_rate = get_series('fed_funds_rate')
print(check_fed_rate_change(fed_rate))

print(fed_rate.iloc[-1])
print(fed_rate.iloc[-2])


# ---------- Checking Conditinal analysis (oil spike) ----------
from src.analysis.conditional import check_oil_spike
oil_prices = get_series('crude_oil_wti')
print(check_oil_spike(oil_prices))