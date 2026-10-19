-- Row count and coverage
SELECT COUNT(*) AS row_count,
       MIN(timestamp_utc) AS first_timestamp_utc,
       MAX(timestamp_utc) AS last_timestamp_utc,
       SUM(CASE WHEN demand_mw IS NULL THEN 1 ELSE 0 END) AS missing_demand,
       SUM(CASE WHEN temperature_c IS NULL THEN 1 ELSE 0 END) AS missing_temperature
FROM hourly_demand_weather;

-- Duplicate UTC timestamps should be zero
SELECT timestamp_utc, COUNT(*) AS duplicate_count
FROM hourly_demand_weather
GROUP BY timestamp_utc
HAVING COUNT(*) > 1;

-- Demand values requiring source investigation
SELECT COUNT(*) AS negative_demand_rows
FROM hourly_demand_weather
WHERE demand_mw < 0;
