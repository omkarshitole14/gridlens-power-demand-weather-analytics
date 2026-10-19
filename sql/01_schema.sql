-- The Python pipeline creates this table. This file documents the expected structure.
-- Use INTEGER/REAL/TEXT types suitable for SQLite.
CREATE TABLE IF NOT EXISTS hourly_demand_weather (
    timestamp_utc TEXT NOT NULL UNIQUE,
    timestamp_local TEXT NOT NULL,
    country TEXT NOT NULL,
    demand_mw REAL,
    temperature_c REAL,
    hour_local INTEGER NOT NULL,
    weekday TEXT NOT NULL,
    month INTEGER NOT NULL,
    season TEXT NOT NULL,
    is_weekend INTEGER NOT NULL
);
