-- Temperature bins are descriptive. Values outside the range are placed in edge bins.
WITH binned AS (
    SELECT CASE
             WHEN temperature_c < 0 THEN '< 0°C'
             WHEN temperature_c < 10 THEN '0–10°C'
             WHEN temperature_c < 20 THEN '10–20°C'
             ELSE '20°C+'
           END AS temperature_band,
           demand_mw
    FROM hourly_demand_weather
    WHERE temperature_c IS NOT NULL AND demand_mw IS NOT NULL
)
SELECT temperature_band,
       COUNT(*) AS paired_hours,
       ROUND(AVG(demand_mw), 2) AS average_demand_mw,
       ROUND(MAX(demand_mw), 2) AS maximum_demand_mw
FROM binned
GROUP BY temperature_band
ORDER BY CASE temperature_band WHEN '< 0°C' THEN 1 WHEN '0–10°C' THEN 2
         WHEN '10–20°C' THEN 3 ELSE 4 END;

-- Pearson correlation is calculated in Python, not native SQLite.
-- Do not interpret correlation as causal impact.
