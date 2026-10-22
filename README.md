# GridLens: Power Demand & Weather Intelligence

An end-to-end data analytics project exploring Germany's historical electricity demand and weather patterns using Python, SQLite, and Power BI.

## Project Overview

GridLens transforms historical electricity demand and weather data into an analysis-ready dataset, performs data-quality checks, calculates descriptive statistics, and presents the findings in an interactive Power BI dashboard.

The project focuses on understanding how electricity demand varies by hour, weekday, month, and temperature. It emphasizes reproducible data preparation, reliable analysis, and transparent reporting of data limitations.

## Project Objectives

- Build a reproducible data ingestion and preparation pipeline.
- Validate timestamps, duplicates, missing values, and source-data coverage.
- Store prepared data in CSV and SQLite formats.
- Analyze demand patterns by hour, weekday, month, and temperature.
- Build an interactive Power BI dashboard.
- Test core data-processing and validation functions.

## Technology Stack

- **Python:** data preparation and analysis
- **Pandas and NumPy:** data manipulation and numerical analysis
- **SQLite:** structured analytical storage
- **Power BI:** interactive dashboards
- **Matplotlib:** exploratory visualizations
- **Pytest:** automated testing
- **Git and GitHub:** version control


## Data Sources

The project uses historical electricity demand and weather data published by Open Power System Data (OPSD).

- **Electricity data:** Time series dataset, version 2020-10-06.
- **Weather data:** Weather dataset, version 2020-09-16.
- **Geographic scope:** Germany (`DE`).
- **Local timezone:** `Europe/Berlin`.

### Source Attribution

Open Power System Data. 2020. *Data Package Time series*. Version 2020-10-06. https://doi.org/10.25832/time_series/2020-10-06.

Open Power System Data. 2020. *Data Package Weather Data*. Version 2020-09-16. https://doi.org/10.25832/weather_data/2020-09-16.

The source files are downloaded by the project pipeline and are not required to be committed to the repository. Consult the original dataset documentation and licensing terms when reusing the data.

## Project Workflow

1. Download the electricity and weather source files.
2. Validate source schemas and required columns.
3. Parse timestamps and align the datasets.
4. Convert timestamps into the `Europe/Berlin` timezone for local calendar features.
5. Prepare hourly demand and weather observations.
6. Check data quality and missing values.
7. Generate descriptive analyses and visualizations.
8. Export prepared data to CSV and SQLite.
9. Review results in Power BI and run automated tests.

## Repository Structure

```text
GridLens/
├── config/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── powerbi/
│   └── GridLens_Dashboard.pbix
├── scripts/
│   ├── download_data.py
│   ├── prepare_data.py
│   └── run_analysis.py
├── tests/
├── README.md
├── pyproject.toml
└── requirements.txt
```

The exact contents of supporting directories may change as the project evolves. Generated datasets and raw source files should be handled according to the repository's Git ignore rules.

## Key Findings

The prepared dataset contains **50,401 hourly records**, covering 31 December 2014 through 30 September 2020 in UTC.

### Electricity demand

| Metric | Result |
|---|---:|
| Valid demand observations | 50,400 |
| Average demand | 55,492.47 MW |
| Median demand | 55,092 MW |
| Minimum demand | 31,307 MW |
| Maximum demand | 77,549 MW |
| Date and local time of maximum | 13 December 2017, 17:00 |
| Highest average demand by hour | 11:00 — 64,033.85 MW |
| Lowest average demand by hour | 02:00 — 43,525.37 MW |
| Highest average weekday | Wednesday — 59,449.26 MW |
| Lowest average weekday | Sunday — 45,808.58 MW |
| Highest average month reported | February — 59,974.17 MW |
| Lowest average month reported | May — 52,284.02 MW |

These are descriptive statistics for the selected historical period, not forecasts or causal estimates.

### Data quality and weather coverage

| Check | Result |
|---|---:|
| Prepared hourly records | 50,401 |
| Missing demand values | 1 |
| Missing temperature values | 6,576 |
| Invalid timestamps reported | 0 |
| Duplicate timestamps reported | 0 |
| Rows with matched weather timestamps | 43,825 |
| Weather timestamp match rate | 86.95% |
| Observations with both valid demand and temperature | 43,824 |

The weather match rate describes timestamp matching; it does not mean that every matched row contains a valid temperature value.

### Temperature and demand

The overall Pearson correlation between temperature and electricity demand is approximately **−0.0272**, indicating a very weak linear relationship across the available paired observations.

This overall correlation does not establish that temperature has no effect on demand. Relationships may vary by season, time of day, and temperature range. Missing weather observations and the combined effects of other variables also limit interpretation.

Temperature-band averages are descriptive comparisons and should not be interpreted as evidence of causation.

The average electricity demand across the available temperature bands was:

| Temperature band | Paired hours | Average demand |
|---|---:|---:|
| Below 0°C | 4,677 | 57,376.27 MW |
| 0–10°C | 18,464 | 56,403.45 MW |
| 10–20°C | 15,256 | 53,654.35 MW |
| 20°C and above | 5,427 | 58,898.99 MW |

These comparisons are descriptive. They do not establish a causal relationship between temperature and electricity demand.

## Power BI Dashboard

The Power BI report contains two pages:

1. **GridLens | Power Demand Intelligence** — overview of electricity demand, summary metrics, and time-based demand patterns.
2. **GridLens | Weather & Demand Analysis** — weather coverage and descriptive comparisons between temperature and demand.

Dashboard figures should be interpreted alongside the data-quality results and limitations described above.

Open `powerbi/GridLens_Dashboard.pbix` in Microsoft Power BI Desktop to explore the report.

## Setup and Execution

The following commands are intended for Windows PowerShell with Python 3.13 installed.

### 1. Clone the repository

```powershell
git clone https://github.com/omkarshitole14/gridlens-power-demand-weather-analytics.git
cd gridlens-power-demand-weather-analytics
```

### 2. Create and activate a virtual environment

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 4. Download source data

```powershell
python scripts/download_data.py
```

### 5. Prepare the dataset

```powershell
python scripts/prepare_data.py
```

### 6. Run the analysis

```powershell
python scripts/run_analysis.py
```

### 7. Run automated tests

```powershell
python -m pytest -q
```

**Latest recorded test result:** 13 passed. Re-run the tests to verify the current checkout.

## Generated Outputs

The pipeline configuration specifies these processed outputs:

- `data/processed/gridlens_hourly.csv`
- `data/processed/gridlens.sqlite`

The CSV provides a portable analytical dataset, while the SQLite database supports structured queries and further analysis.

## Data Definitions and Limitations

- **Electricity demand:** the selected OPSD actual-load series, measured in megawatts (MW). It should not be treated as electricity generation, reserve capacity, or a direct measure of supply-demand imbalance.
- **Temperature:** a weather dataset estimate. It is not necessarily the temperature at every electricity consumer's location.
- **Timezones:** timestamps are aligned using UTC; local calendar features use `Europe/Berlin`. Daylight-saving transitions can create repeated or missing local clock hours.
- **Missing data:** missing values are identified rather than silently treated as zero.
- **Weather coverage:** temperature is unavailable for a portion of the electricity dataset, so weather-related analysis uses the available paired observations.
- **Correlation:** Pearson correlation measures linear association and does not establish causation.
- **Monthly averages:** the dataset begins and ends partway through calendar years, so comparisons should account for incomplete coverage.
- **Historical scope:** the analysis describes past observations; it is not a production forecasting system.

## Possible Future Improvements

- Compare temperature-demand relationships by season and time of day.
- Investigate nonlinear temperature effects.
- Add a time-aware forecasting baseline with a chronological holdout period.
- Expand automated checks for source-data changes and analytical outputs.
- Incorporate additional compatible datasets where they improve the analysis.

## Author

**Omkar Shitole**

GitHub: [omkarshitole14](https://github.com/omkarshitole14)

Project repository: [GridLens — Power Demand & Weather Analytics](https://github.com/omkarshitole14/gridlens-power-demand-weather-analytics)
