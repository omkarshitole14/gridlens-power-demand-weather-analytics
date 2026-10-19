import pandas as pd

def summary_metrics(df: pd.DataFrame) -> dict:
    demand = pd.to_numeric(df["demand_mw"], errors="coerce").dropna()
    temperature = pd.to_numeric(df["temperature_c"], errors="coerce")
    paired = pd.DataFrame({"demand_mw": df["demand_mw"], "temperature_c": temperature}).dropna()
    correlation = None if len(paired) < 2 or paired["demand_mw"].nunique() < 2 or paired["temperature_c"].nunique() < 2 else float(paired["demand_mw"].corr(paired["temperature_c"]))
    return {
        "rows": int(len(df)),
        "valid_demand_rows": int(demand.size),
        "mean_demand_mw": None if demand.empty else float(demand.mean()),
        "median_demand_mw": None if demand.empty else float(demand.median()),
        "minimum_demand_mw": None if demand.empty else float(demand.min()),
        "maximum_demand_mw": None if demand.empty else float(demand.max()),
        "temperature_demand_pearson_correlation": correlation,
        "paired_weather_demand_rows": int(len(paired)),
    }

def demand_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("hour_local", dropna=False)["demand_mw"].agg(["count", "mean", "median", "max"]).reset_index()

def demand_by_weekday(df: pd.DataFrame) -> pd.DataFrame:
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    result = df.groupby("weekday")["demand_mw"].agg(["count", "mean", "median", "max"]).reindex(order).reset_index()
    return result

def demand_by_month(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("month")["demand_mw"].agg(["count", "mean", "median", "max"]).reset_index()
