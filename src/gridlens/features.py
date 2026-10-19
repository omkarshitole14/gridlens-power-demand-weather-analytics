import pandas as pd

def add_time_features(df: pd.DataFrame, timezone: str = "Europe/Berlin") -> pd.DataFrame:
    result = df.copy()
    utc = pd.to_datetime(result["timestamp_utc"], utc=True, errors="raise")
    local = utc.dt.tz_convert(timezone)
    result["timestamp_utc"] = utc
    result["timestamp_local"] = local
    result["hour_local"] = local.dt.hour.astype("int8")
    result["weekday"] = local.dt.day_name()
    result["month"] = local.dt.month.astype("int8")
    result["season"] = local.dt.month.map({12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring", 6: "Summer", 7: "Summer", 8: "Summer", 9: "Autumn", 10: "Autumn", 11: "Autumn"})
    result["is_weekend"] = local.dt.dayofweek >= 5
    return result
