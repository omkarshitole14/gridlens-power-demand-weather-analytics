# Power BI dashboard guide

## Connect data
1. Run the Python pipeline and verify `reports/data_quality.json` first.
2. In Power BI Desktop, choose **Get data → Text/CSV** and select `data/processed/gridlens_hourly.csv`. Alternatively, connect to SQLite using an installed SQLite connector; CSV is the simpler portable option.
3. Confirm `timestamp_utc` and `timestamp_local` are parsed as Date/Time, `demand_mw` as Decimal Number, `temperature_c` as Decimal Number, `hour_local` and `month` as Whole Number, and `is_weekend` as True/False.
4. Use `timestamp_local` for local operational time charts and retain `timestamp_utc` for traceable joins.

## Suggested model and measures
The initial dataset is one hourly fact table, so a star schema is not required yet. If adding a calendar dimension, relate its unique hourly/date key carefully and avoid ambiguous many-to-many relationships.

```DAX
Observed Hours = COUNT('hourly_demand_weather'[demand_mw])
Average Demand (MW) = AVERAGE('hourly_demand_weather'[demand_mw])
Peak Demand (MW) = MAX('hourly_demand_weather'[demand_mw])
Average Temperature (C) = AVERAGE('hourly_demand_weather'[temperature_c])
Weather-Demand Paired Hours =
COUNTROWS(
    FILTER(
        'hourly_demand_weather',
        NOT ISBLANK('hourly_demand_weather'[demand_mw])
            && NOT ISBLANK('hourly_demand_weather'[temperature_c])
    )
)
```

These are definitions, not reported findings. Check the column/table names after importing.

## Page 1 — Overview
- KPI cards: average demand, peak demand, observed hours, weather-demand paired hours.
- Line chart: demand over time; use a date slicer and avoid showing every hour label.
- Slicers: date range, season, weekday/weekend.

## Page 2 — Demand patterns
- Line chart: average demand by `hour_local`.
- Bar chart: average demand by weekday.
- Column chart: average demand by month or season.
- Table: top observed demand hours with timestamp and temperature.

## Page 3 — Weather relationship
- Scatter plot: temperature vs demand; add a trend line only as a descriptive aid.
- Column chart: average demand by temperature band, built in Python or Power Query with documented bin boundaries.
- Text note: association is not causation; country-level weather is an approximation.

## Design and publishing
Use a restrained palette, consistent units, meaningful titles, and clear date coverage. Do not infer a supply gap from peak demand. Add a text box with dataset source and known limitations. Save the `.pbix` locally and add screenshots only after validating the visuals. Sharing a `.pbix` in a browser typically requires Power BI Service and suitable licensing/tenant permissions; do not assume a local file is publicly interactive.
