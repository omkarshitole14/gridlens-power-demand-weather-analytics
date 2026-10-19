# \# GridLens: Power Demand \& Weather Intelligence

# 

# GridLens is a reproducible data analytics project investigating hourly electricity demand in Germany and its relationship with weather. It demonstrates data preparation, data-quality validation, Python analysis, SQL querying, statistical interpretation, and Power BI dashboard development.

# 

# The project focuses on identifying demand patterns and exploring weather-related relationships in historical data. It does not treat high demand as proof of a supply shortage or infer causation from correlation.

# 

# \## Project Objectives

# 

# \- Analyze electricity demand across hours, weekdays, and months.

# \- Validate timestamps, missing values, duplicate records, and weather coverage.

# \- Explore demand patterns across temperature ranges.

# \- Use Python and SQL to produce reproducible analytical outputs.

# \- Present key findings through an interactive Power BI dashboard.

# \- Document data limitations and distinguish observed results from recommendations.

# 

# \## Data Sources

# 

# The project uses historical data from Open Power System Data (OPSD).

# 

# \- \*\*Electricity load:\*\* \[OPSD Time Series — 2020-10-06](https://data.open-power-system-data.org/time\_series/2020-10-06/)

# \- \*\*Weather data:\*\* \[OPSD Weather Data — 2020-09-16](https://data.open-power-system-data.org/weather\_data/2020-09-16/)

# 

# Selected source variables:

# \- Electricity demand: `DE\_load\_actual\_entsoe\_transparency`

# \- Temperature: `DE\_temperature`

# 

# \### Source attribution

# 

# Open Power System Data. 2020. \*Data Package Time series\*. Version 2020-10-06. https://doi.org/10.25832/time\_series/2020-10-06.

# 

# Open Power System Data. 2020. \*Data Package Weather Data\*. Version 2020-09-16. https://doi.org/10.25832/weather\_data/2020-09-16.

# 

# The source packages aggregate data from their documented primary sources. Review the package documentation and applicable terms before redistributing source data. Original raw files are excluded from the project repository.

# 

# \## Technology Stack

# 

# \- \*\*Python:\*\* data preparation, validation, and analysis

# \- \*\*Pandas and NumPy:\*\* data processing and numerical calculations

# \- \*\*SQL and SQLite:\*\* analytical queries and structured storage

# \- \*\*Power BI Desktop:\*\* dashboard development and visualization

# \- \*\*Matplotlib:\*\* analytical charts

# \- \*\*Pytest:\*\* automated tests

# \- \*\*Git:\*\* version control

# 

# \## Project Workflow

# 

# 1\. \*\*Data preparation:\*\* inspect source columns, select Germany's electricity load and temperature data, normalize timestamps, and join the datasets.

# 2\. \*\*Data validation:\*\* check missing values, duplicate timestamps, timestamp validity, and weather coverage.

# 3\. \*\*Python analysis:\*\* calculate summary statistics and aggregate demand by hour, weekday, and month.

# 4\. \*\*SQL analysis:\*\* query demand patterns and compare observations across temperature ranges.

# 5\. \*\*Dashboard development:\*\* visualize demand patterns and explore the relationship between temperature and demand.

# 6\. \*\*Reporting:\*\* document findings, data-quality limitations, and potential follow-up analysis.

# 

# \## Repository Structure

# 

# ```text

# GridLens/

# ├── config/

# ├── data/

# │   ├── raw/

# │   └── processed/

# ├── notebooks/

# ├── powerbi/

# │   ├── GridLens\_Dashboard.pbix

# │   └── dashboard\_guide.md

# ├── reports/

# │   ├── figures/

# │   ├── data\_quality.json

# │   ├── summary\_metrics.json

# │   └── findings\_report.md

# ├── scripts/

# ├── sql/

# ├── src/

# ├── tests/

# ├── .gitignore

# ├── LICENSE

# ├── pyproject.toml

# ├── requirements.txt

# └── README.md

# ```

# 

# \## Key Findings

# 

# The following findings were generated from the current local analysis outputs. They describe the available historical dataset, not current electricity-grid conditions.

# 

# \### Dataset and data quality

# 

# \- \*\*50,401\*\* hourly records in the prepared dataset.

# \- \*\*50,400\*\* records with valid electricity-demand values.

# \- \*\*1\*\* missing electricity-demand value.

# \- \*\*6,576\*\* missing temperature values.

# \- \*\*43,824\*\* paired observations with both valid demand and temperature.

# \- \*\*0\*\* invalid timestamps and \*\*0\*\* duplicate timestamps in the reported quality checks.

# \- Observed coverage runs from December 31, 2014, to September 30, 2020, in UTC.

# 

# Weather coverage is incomplete near the end of the study period. Temperature-based findings therefore use paired observations only; demand-only analysis can include valid demand observations without temperature data.

# 

# \### Electricity demand patterns

# 

# \- \*\*Average demand:\*\* 55,492.47 MW.

# \- \*\*Maximum observed demand:\*\* 77,549 MW on December 13, 2017, at 17:00 local time.

# \- \*\*Highest average hourly demand:\*\* 64,033.85 MW at 11:00.

# \- \*\*Lowest average hourly demand:\*\* 43,525.37 MW at 02:00.

# \- \*\*Highest average weekday demand:\*\* Wednesday, at 59,449.26 MW.

# \- \*\*Lowest average weekday demand:\*\* Sunday, at 45,808.58 MW.

# \- February had the highest monthly average among the reported months, at 59,974.17 MW; May had the lowest, at 52,284.02 MW.

# 

# Monthly comparisons require caution because the dataset contains partial years and monthly observation counts may differ.

# 

# \### Temperature and demand

# 

# The Pearson correlation between temperature and demand across paired observations was approximately \*\*−0.0272\*\*, indicating a very weak overall linear relationship in this dataset.

# 

# Average demand across temperature bands was:

# 

# | Temperature band | Paired hours | Average demand |

# |---|---:|---:|

# | Below 0°C | 4,677 | 57,376.27 MW |

# | 0–10°C | 18,464 | 56,403.45 MW |

# | 10–20°C | 15,256 | 53,654.35 MW |

# | 20°C and above | 5,427 | 58,898.99 MW |

# 

# These descriptive results suggest that the relationship may not be purely linear. They do not establish that temperature caused the observed changes. Seasonality, calendar effects, and other factors would need further investigation.

# 

# \## Power BI Dashboard

# 

# The Power BI report contains two pages:

# 

# 1\. \*\*GridLens | Power Demand Intelligence\*\* — demand summary indicators and demand patterns over time, by hour, weekday, and month.

# 2\. \*\*GridLens | Weather \& Demand Analysis\*\* — temperature-versus-demand observations, weather-related summary information, and interpretation of data limitations.

# 

# Dashboard file: `powerbi/GridLens\_Dashboard.pbix`

# 

# For data definitions and dashboard guidance, see `powerbi/dashboard\_guide.md`.

# 

# \## Generated Outputs

# 

# | Output | Description |

# |---|---|

# | `data/processed/gridlens\_hourly.csv` | Prepared hourly analysis dataset |

# | `data/processed/gridlens.sqlite` | SQLite database containing `hourly\_demand\_weather` |

# | `reports/data\_quality.json` | Data-quality checks and coverage summary |

# | `reports/summary\_metrics.json` | Summary statistics |

# | `reports/demand\_by\_hour.csv` | Demand aggregated by hour |

# | `reports/demand\_by\_weekday.csv` | Demand aggregated by weekday |

# | `reports/demand\_by\_month.csv` | Demand aggregated by month |

# | `reports/figures/` | Generated analytical charts |

# | `reports/findings\_report.md` | Detailed findings and limitations |

# 

# Generated outputs can be recreated by running the pipeline against the source files.

# 

# \## Setup — Windows PowerShell

# 

# The existing project environment has been tested with Python 3.13.5. The instructions below use Python 3.13; other Python versions should be verified against the project dependencies before use.

# 

# From the project root:

# 

# ```powershell

# py -3.13 -m venv .venv

# .\\.venv\\Scripts\\Activate.ps1

# python -m pip install --upgrade pip

# pip install -r requirements.txt

# pip install -e .

# ```

# 

# If PowerShell blocks environment activation, run the following in the current terminal and try activating again:

# 

# ```powershell

# Set-ExecutionPolicy -ScopeProcess -ExecutionPolicy Bypass

# ```

# 

# This changes the policy only for the current PowerShell process.

# 

# \### Run the pipeline

# 

# Download the source data if it is not already present:

# 

# ```powershell

# python scripts/download\_data.py

# ```

# 

# Prepare the dataset and generate analytical outputs:

# 

# ```powershell

# python scripts/prepare\_data.py

# python scripts/run\_analysis.py

# ```

# 

# Run the automated tests:

# 

# ```powershell

# python -m pytest -q

# ```

# 

# The current recorded test result is \*\*7 passed\*\*. Rerun the tests after changes to confirm the current state.

# 

# \## SQL Analysis

# 

# The SQL scripts are located in `sql/`. They can be executed against `data/processed/gridlens.sqlite` using a SQLite database browser or a compatible SQLite command-line workflow.

# 

# The SQL analysis covers demand patterns and demand across temperature ranges. Refer to the scripts and generated reports for the exact queries and results.

# 

# \## Data Definitions and Limitations

# 

# \- Electricity demand represents the source's reported actual electricity load; it is not a complete measure of grid supply or reserve capacity.

# \- Temperature is a country-level, population-weighted reanalysis estimate and does not represent a measurement at every grid location.

# \- UTC timestamps are used to align the source datasets. Local-time features use the Europe/Berlin time zone.

# \- Daylight-saving transitions can produce repeated or missing local hours.

# \- Missing load and temperature values remain missing rather than being replaced with zero.

# \- Weather-based analysis is limited to records with valid demand and temperature.

# \- The overall correlation is descriptive and does not establish causation.

# \- Monthly averages may be affected by unequal observation counts and partial-year coverage.

# \- The source packages are historical snapshots, not live operational feeds.

# \- Supply-demand imbalance and forecasting are outside the current baseline scope.

# 

# \## Potential Follow-up Work

# 

# \- Investigate nonlinear temperature-demand relationships while controlling for seasonality and calendar effects.

# \- Compare results across seasons and years with consistent data coverage.

# \- Add time-aware forecasting only with an appropriate holdout period, a naive baseline, and checks for data leakage.

# \- Extend the analysis only when additional datasets have compatible definitions, units, and timestamps.

# 

# \## Verification Notes

# 

# The Python preparation and analysis scripts have been executed, and the current automated test suite passed seven tests. The Power BI report has been created locally.

# 

# These checks do not imply that every fresh source download, installation on another machine, or external deployment has been independently tested. Re-run the pipeline and tests when reproducing the project.

# 

# \---

# 

# \*GridLens is an exploratory data analytics project based on historical electricity demand and weather data.\*



