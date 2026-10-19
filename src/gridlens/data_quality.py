import pandas as pd

def quality_report(df: pd.DataFrame, timestamp_col: str = "timestamp_utc") -> dict:
    if timestamp_col not in df.columns:
        raise ValueError(f"Required timestamp column not found: {timestamp_col}")
    timestamps = pd.to_datetime(df[timestamp_col], utc=True, errors="coerce")
    return {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": list(df.columns),
        "invalid_timestamps": int(timestamps.isna().sum()),
        "duplicate_timestamps": int(timestamps.duplicated().sum()),
        "missing_values": {key: int(value) for key, value in df.isna().sum().items()},
        "start_utc": None if timestamps.dropna().empty else timestamps.min().isoformat(),
        "end_utc": None if timestamps.dropna().empty else timestamps.max().isoformat(),
    }

def validate_hourly_table(df: pd.DataFrame) -> None:
    required = {"timestamp_utc", "demand_mw", "temperature_c", "country"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Prepared data is missing required columns: {sorted(missing)}")
    if df["timestamp_utc"].isna().any():
        raise ValueError("Prepared data contains invalid timestamps")
    if df["timestamp_utc"].duplicated().any():
        raise ValueError("Prepared data contains duplicate UTC timestamps")
    if (df["demand_mw"].dropna() < 0).any():
        raise ValueError("Demand contains negative values; inspect source before continuing")
