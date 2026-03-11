import time
from src.data.series_config import SERIES
from src.data.fred_client import get_series

for key, meta in SERIES.items():
    for attempt in range(3):
        try:
            series = get_series(key)
            print(f"\n=== {meta['name']} ({meta['id']}) ===")
            print(series.head())
            break
        except Exception as e:
            if attempt < 2:
                print(f"  Retrying {meta['id']} ({e})...")
                time.sleep(2)
            else:
                print(f"  FAILED {meta['id']}: {e}")
