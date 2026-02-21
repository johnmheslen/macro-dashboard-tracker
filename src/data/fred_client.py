from src.data.series_config import SERIES
from fredapi import Fred
from dotenv import load_dotenv
import os

load_dotenv()
fred = Fred(api_key=os.getenv('FRED_API_KEY'))


def get_series(series_key):
    series_id = SERIES[series_key]['id']
    return fred.get_series(series_id)

def get_frequency(series_key):
    return SERIES[series_key]['frequency']