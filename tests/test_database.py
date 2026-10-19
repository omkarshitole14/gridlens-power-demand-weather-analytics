import sqlite3
import pandas as pd
from gridlens.database import write_database

def test_database_writer_creates_table_and_indexes(tmp_path):
    df = pd.DataFrame({"timestamp_utc": ["2020-01-01T00:00:00+00:00"], "month": [1], "demand_mw": [123.0]})
    path = tmp_path / "sample.sqlite"
    write_database(df, path)
    with sqlite3.connect(path) as connection:
        count = connection.execute("SELECT COUNT(*) FROM hourly_demand_weather").fetchone()[0]
        indexes = {row[1] for row in connection.execute("PRAGMA index_list(hourly_demand_weather)")}
    assert count == 1
    assert "idx_hourly_timestamp_utc" in indexes
