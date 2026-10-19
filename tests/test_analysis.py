import pandas as pd
from gridlens.analysis import summary_metrics, demand_by_hour

def test_summary_metrics_use_valid_pairs_for_correlation():
    df = pd.DataFrame({"demand_mw": [10, 20, 30], "temperature_c": [1, 2, 3], "hour_local": [0, 1, 2]})
    result = summary_metrics(df)
    assert result["mean_demand_mw"] == 20
    assert result["maximum_demand_mw"] == 30
    assert result["temperature_demand_pearson_correlation"] == 1.0
    assert result["paired_weather_demand_rows"] == 3

def test_demand_by_hour_counts_non_missing_demand():
    df = pd.DataFrame({"hour_local": [0, 0, 1], "demand_mw": [10, None, 20]})
    result = demand_by_hour(df).set_index("hour_local")
    assert result.loc[0, "count"] == 1
    assert result.loc[1, "mean"] == 20
