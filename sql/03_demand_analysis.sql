-- Average and peak load by local hour
SELECT hour_local,
       COUNT(demand_mw) AS observed_hours,
       ROUND(AVG(demand_mw), 2) AS average_demand_mw,
       ROUND(MAX(demand_mw), 2) AS peak_demand_mw
FROM hourly_demand_weather
GROUP BY hour_local
ORDER BY hour_local;

-- Weekday profile
SELECT weekday,
       COUNT(demand_mw) AS observed_hours,
       ROUND(AVG(demand_mw), 2) AS average_demand_mw,
       ROUND(MAX(demand_mw), 2) AS peak_demand_mw
FROM hourly_demand_weather
GROUP BY weekday
ORDER BY CASE weekday WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2
         WHEN 'Wednesday' THEN 3 WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5
         WHEN 'Saturday' THEN 6 WHEN 'Sunday' THEN 7 END;

-- Highest observed demand hours; this ranks observations, not supply shortages
WITH ranked_hours AS (
    SELECT timestamp_local, demand_mw, temperature_c,
           DENSE_RANK() OVER (ORDER BY demand_mw DESC) AS demand_rank
    FROM hourly_demand_weather
    WHERE demand_mw IS NOT NULL
)
SELECT timestamp_local, demand_mw, temperature_c, demand_rank
FROM ranked_hours
WHERE demand_rank <= 20
ORDER BY demand_rank, timestamp_local;

-- Monthly demand profile
SELECT month,
       COUNT(demand_mw) AS observed_hours,
       ROUND(AVG(demand_mw), 2) AS average_demand_mw,
       ROUND(MAX(demand_mw), 2) AS peak_demand_mw
FROM hourly_demand_weather
GROUP BY month
ORDER BY month;
