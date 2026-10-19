import pandas as pd
import pytest
from gridlens.data_quality import quality_report, validate_hourly_table

def test_quality_report_counts_missing_and_duplicates():
    df = pd.DataFrame({"timestamp_utc": ["2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "bad"], "x": [1, None, 3]})
    report = quality_report(df)
    assert report["row_count"] == 3
    assert report["duplicate_timestamps"] == 1
    assert report["invalid_timestamps"] == 1
    assert report["missing_values"]["x"] == 1

def test_validate_rejects_duplicate_timestamp():
    df = pd.DataFrame({"timestamp_utc": pd.to_datetime(["2020-01-01T00:00Z"] * 2), "demand_mw": [1, 2], "temperature_c": [3, 4], "country": ["DE", "DE"]})
    with pytest.raises(ValueError, match="duplicate"):
        validate_hourly_table(df)

def test_validate_allows_missing_weather_but_not_negative_demand():
    valid = pd.DataFrame({"timestamp_utc": pd.to_datetime(["2020-01-01T00:00Z"]), "demand_mw": [10], "temperature_c": [None], "country": ["DE"]})
    validate_hourly_table(valid)
    valid.loc[0, "demand_mw"] = -1
    with pytest.raises(ValueError, match="negative"):
        validate_hourly_table(valid)
