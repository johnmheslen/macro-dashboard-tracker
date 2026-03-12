"""
series_config.py
────────────────
Central registry of all FRED (Federal Reserve Economic Data) series used
throughout the macro dashboard.

Each key is a short, human-friendly alias used across the codebase.
Each value is a dict with:
    id        – the official FRED series identifier
    name      – a readable display name
    frequency – how often the series is updated ('daily', 'weekly',
                'monthly', 'quarterly', 'annual')

Adding a new series here is all that's required to make it available to
fred_client.get_series() and the analysis modules.
"""

# ─────────────────────────────────────────────────────────────────────────────
# SERIES REGISTRY
# ─────────────────────────────────────────────────────────────────────────────

SERIES = {

    # ── Inflation ─────────────────────────────────────────────────────────────

    'cpi': {
        'id': 'CPIAUCSL',               # All Urban Consumers, seasonally adjusted
        'name': 'Consumer Price Index',
        'frequency': 'monthly'
    },
    'pce_price_index': {
        'id': 'PCEPI',                  # Personal Consumption Expenditures; the Fed's preferred inflation gauge
        'name': 'PCE Price Index',
        'frequency': 'monthly'
    },

    # ── Labor Market ──────────────────────────────────────────────────────────

    'unemployment': {
        'id': 'UNRATE',                 # U-3 headline unemployment rate (%)
        'name': 'Unemployment Rate',
        'frequency': 'monthly'
    },
    'nonfarm_payrolls': {
        'id': 'PAYEMS',                 # Total nonfarm employees (thousands)
        'name': 'Nonfarm Payrolls',
        'frequency': 'monthly'
    },

    # ── Growth ────────────────────────────────────────────────────────────────

    'real_gdp': {
        'id': 'GDPC1',                  # Chained 2017 dollars, seasonally adjusted annual rate
        'name': 'Real GDP',
        'frequency': 'quarterly'
    },

    # ── Interest Rates & Credit ───────────────────────────────────────────────

    't10y2y': {
        'id': 'T10Y2Y',                 # Yield curve spread; negative value = inverted = recession signal
        'name': '10 Year - 2 Year Treasury Spread',
        'frequency': 'daily'
    },
    'fed_funds_rate': {
        'id': 'FEDFUNDS',               # Effective federal funds rate (%)
        'name': 'Federal Funds Effective Rate',
        'frequency': 'monthly'
    },
    'mortgage_rate': {
        'id': 'MORTGAGE30US',           # 30-year fixed rate national average (%)
        'name': '30 Year Fixed Mortgage Rate',
        'frequency': 'weekly'
    },

    # ── Housing ───────────────────────────────────────────────────────────────

    'housing_starts': {
        'id': 'HOUST',                  # New privately-owned housing units started (thousands, SAAR)
        'name': 'Housing Starts',
        'frequency': 'monthly'
    },

    # ── Sentiment ─────────────────────────────────────────────────────────────

    'consumer_sentiment': {
        'id': 'UMCSENT',                # University of Michigan Consumer Sentiment Index
        'name': 'Consumer Sentiment',
        'frequency': 'monthly'
    },

    # ── Commodities ───────────────────────────────────────────────────────────

    'crude_oil_wti': {
        'id': 'DCOILWTICO',             # West Texas Intermediate spot price (USD/barrel)
        'name': 'Crude Oil(WTI)',
        'frequency': 'daily'
    },
}
