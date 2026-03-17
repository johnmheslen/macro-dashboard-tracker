from src.data.fred_client import get_series
import pandas as pd

# # Checking Conditional analysis function 1
# # yield_curve = get_series('t10y2y')
# # from src.analysis.conditional import check_yield_curve_inverted
# # print(check_yield_curve_inverted(yield_curve))

# # Checking Conditional analysis function 2
# cpi = get_series('cpi')
# # from src.analysis.conditional import check_series_accelerating
# # print(check_series_accelerating(cpi, 6))

# # Checking Conditional analysis function 3
# mortrate = get_series('mortgage_rate')
# housestarts = get_series('housing_starts')
# # from src.analysis.conditional import check_housing_slowdown
# # print(check_housing_slowdown(housestarts, mortrate, 6))

# # mortrate_monthly = mortrate.resample("ME").last()

# # print(mortrate_monthly.iloc[-8:])

# # Checking Conditional analysis function 4
# from src.analysis.conditional import check_unemployment_drop
# unrate = get_series('unemployment')
# print(check_unemployment_drop(unrate))


# # ---------- Checking Conditional analysis functin 4 ----------
# from src.analysis.conditional import check_fed_rate_change
# fed_rate = get_series('fed_funds_rate')
# print(check_fed_rate_change(fed_rate))

# print(fed_rate.iloc[-1])
# print(fed_rate.iloc[-2])


# # ---------- Checking Conditinal analysis (oil spike) ----------
# from src.analysis.conditional import check_oil_spike
# oil_prices = get_series('crude_oil_wti')

# print(check_oil_spike(oil_prices))


# # ------- Checking Phillips Curve correlation ----------
# cpi = get_series('cpi')
# unemployment = get_series('unemployment')

# print("Without resampling:\n")
# print(cpi.index[-1])
# print(unemployment.index[-1])
# print(cpi.tail())
# print(unemployment.tail())
# print()
# df = cpi.interpolate().rolling(window=24).corr(other=unemployment.interpolate())
# print(df.tail())

# cpi_m = cpi.resample('MS').last()
# unemployment_m = unemployment.resample('MS').last()

# print(cpi_m.index[-5:])
# print(unemployment_m.index[-5:])


# # df = cpi_m.rolling(window=24).corr(unemployment_m)

# # print(df.tail())

# # ----- Test phillips curve correlation method -------
# print("\n" + "-"*10 + "Phillips Curve Correlation Method" + "-"*10)
# from src.analysis.correlation import phillips_curve_dev
# print(phillips_curve_dev(cpi, unemployment, 120))
# print()
# print(f"Current: {df.iloc[-1]}\nMean: {df.iloc[-120:].mean()}\nStandard Dev: {df.iloc[-120:].std()}")


# ---------- Testing forecast.py module ------------
from src.analysis.forecast import forecast_series
series = get_series('cpi')

print(forecast_series(series))