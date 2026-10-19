# Data dictionary (expected prepared table)

| Column | Meaning | Unit / type |
|---|---|---|
| timestamp_utc | Hourly timestamp in UTC | ISO timestamp |
| timestamp_local | Timestamp converted to Europe/Berlin | ISO timestamp with timezone |
| country | OPSD country code | text (`DE`) |
| demand_mw | Reported actual electricity load | MW, verified from source metadata before interpretation |
| temperature_c | Country-level temperature from OPSD weather | degrees Celsius |
| hour_local | Local hour (0–23) | integer |
| weekday | Local weekday name | text |
| month | Local month number | integer |
| season | Meteorological season in local time | text |
| is_weekend | Whether local day is Saturday/Sunday | boolean |

The preparation script discovers the source load column dynamically and preserves source nulls. Always inspect the source metadata before assuming measurement semantics beyond the documented load definition.
