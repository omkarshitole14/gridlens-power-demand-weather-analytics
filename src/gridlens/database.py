import sqlite3
from pathlib import Path
import pandas as pd

def write_database(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        df.to_sql("hourly_demand_weather", connection, if_exists="replace", index=False)
        connection.execute("CREATE INDEX IF NOT EXISTS idx_hourly_timestamp_utc ON hourly_demand_weather(timestamp_utc)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_hourly_month ON hourly_demand_weather(month)")
