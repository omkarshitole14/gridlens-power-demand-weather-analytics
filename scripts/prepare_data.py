from pathlib import Path
import json
import pandas as pd
from gridlens.config import ROOT, load_config, ensure_project_dirs
from gridlens.data_quality import quality_report, validate_hourly_table
from gridlens.features import add_time_features
from gridlens.database import write_database
def count_invalid_timestamps(timestamps: pd.Series) -> int:
    """Count timestamps that could not be parsed."""
    return int(timestamps.isna().sum())

def find_load_column(columns: list[str], country: str) -> str:
    # Use Germany-wide actual demand, not individual transmission operators.
    preferred = f"{country}_load_actual_entsoe_transparency"

    if preferred in columns:
        return preferred

    raise ValueError(
        f"Required country-wide actual-load column not found: {preferred}"
    )


def main() -> None:
    ensure_project_dirs()
    config = load_config()
    electricity_path = ROOT / "data/raw" / config["electricity_filename"]
    weather_path = ROOT / "data/raw" / config["weather_filename"]
    if not electricity_path.exists() or not weather_path.exists():
        raise FileNotFoundError("Raw files are missing. Run `python scripts/download_data.py` first.")
    # Read only header first to discover source schema; then load only needed columns.
    header = pd.read_csv(electricity_path, nrows=0).columns.tolist()
    if "utc_timestamp" not in header:
        raise ValueError("Electricity source does not contain utc_timestamp; inspect package documentation before adapting the join.")
    load_column = find_load_column(header, config["country"])
    electricity = pd.read_csv(electricity_path, usecols=["utc_timestamp", load_column], low_memory=False)
    weather_header = pd.read_csv(weather_path, nrows=0).columns.tolist()
    weather_column = f"{config['country']}_temperature"
    if "utc_timestamp" not in weather_header or weather_column not in weather_header:
        raise ValueError(f"Weather schema mismatch. Required utc_timestamp and {weather_column}; found header sample: {weather_header[:20]}")
    weather = pd.read_csv(weather_path, usecols=["utc_timestamp", weather_column], low_memory=False)
    electricity["timestamp_utc"] = pd.to_datetime(electricity["utc_timestamp"], utc=True, errors="coerce")
    weather["timestamp_utc"] = pd.to_datetime(weather["utc_timestamp"], utc=True, errors="coerce")
    electricity_invalid_timestamps = count_invalid_timestamps(
        electricity["timestamp_utc"]
    )
    weather_invalid_timestamps = count_invalid_timestamps(
        weather["timestamp_utc"]
    )
    electricity["demand_mw"] = pd.to_numeric(electricity[load_column], errors="coerce")
    weather["temperature_c"] = pd.to_numeric(weather[weather_column], errors="coerce")
    electricity = electricity[["timestamp_utc", "demand_mw"]].dropna(subset=["timestamp_utc"])
    weather = weather[["timestamp_utc", "temperature_c"]].dropna(subset=["timestamp_utc"])
    if electricity["timestamp_utc"].duplicated().any():
        raise ValueError("Electricity file contains duplicate UTC timestamps. Inspect daylight-saving/time handling before joining.")
    if weather["timestamp_utc"].duplicated().any():
        raise ValueError("Weather file contains duplicate UTC timestamps.")
    merged = electricity.merge(weather, on="timestamp_utc", how="left", validate="one_to_one", indicator=True)
    matched = int((merged["_merge"] == "both").sum())
    merged = merged.drop(columns="_merge")
    merged["country"] = config["country"]
    merged = add_time_features(merged, config["timezone"])
    merged = merged[["timestamp_utc", "timestamp_local", "country", "demand_mw", "temperature_c", "hour_local", "weekday", "month", "season", "is_weekend"]]
    validate_hourly_table(merged)
    output_csv = ROOT / config["output_csv"]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(output_csv, index=False)
    database_path = ROOT / config["database_path"]
    write_database(merged, database_path)
    report = quality_report(merged)
    report.update({
        "source_load_column": load_column,
        "source_weather_column": weather_column,
        "source_electricity_file": electricity_path.name,
        "source_weather_file": weather_path.name,
        "electricity_invalid_timestamps": electricity_invalid_timestamps,
        "weather_invalid_timestamps": weather_invalid_timestamps,
        "weather_matched_rows": matched,
        "weather_match_rate": None if len(merged) == 0 else matched / len(merged),
    })

    (ROOT / "reports/data_quality.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
    print(f"Prepared {len(merged):,} rows -> {output_csv}")
    print(f"SQLite database -> {database_path}")
    print(f"Weather match rate: {report['weather_match_rate']:.1%}" if report["weather_match_rate"] is not None else "No rows to match")
    print("Review reports/data_quality.json before interpreting results.")

if __name__ == "__main__":
    main()
