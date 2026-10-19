import pandas as pd
from gridlens.features import add_time_features

def test_time_features_are_derived_in_local_timezone():
    df = pd.DataFrame({"timestamp_utc": pd.to_datetime(["2024-01-01T00:00:00Z"]), "demand_mw": [1], "temperature_c": [2], "country": ["DE"]})
    result = add_time_features(df)
    assert result.loc[0, "hour_local"] == 1
    assert result.loc[0, "weekday"] == "Monday"
    assert result.loc[0, "season"] == "Winter"
    assert bool(result.loc[0, "is_weekend"]) is False
