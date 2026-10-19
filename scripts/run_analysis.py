from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from gridlens.config import ROOT, load_config, ensure_project_dirs
from gridlens.analysis import summary_metrics, demand_by_hour, demand_by_weekday, demand_by_month

def main() -> None:
    ensure_project_dirs()
    config = load_config()
    data_path = ROOT / config["output_csv"]
    if not data_path.exists():
        raise FileNotFoundError("Prepared dataset not found. Run `python scripts/prepare_data.py` first.")
    df = pd.read_csv(data_path, parse_dates=["timestamp_utc", "timestamp_local"])
    if df.empty:
        raise ValueError("Prepared dataset is empty; do not generate findings from empty data.")
    report_dir = ROOT / "reports"
    figures_dir = report_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "summary_metrics.json").write_text(json.dumps(summary_metrics(df), indent=2), encoding="utf-8")
    demand_by_hour(df).to_csv(report_dir / "demand_by_hour.csv", index=False)
    demand_by_weekday(df).to_csv(report_dir / "demand_by_weekday.csv", index=False)
    demand_by_month(df).to_csv(report_dir / "demand_by_month.csv", index=False)
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 5))
    plt.plot(df["timestamp_utc"], df["demand_mw"], linewidth=0.6)
    plt.title("Germany electricity demand over time")
    plt.xlabel("Timestamp (UTC)")
    plt.ylabel("Reported load (MW)")
    plt.tight_layout(); plt.savefig(figures_dir / "demand_over_time.png", dpi=160); plt.close()
    hourly = demand_by_hour(df)
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=hourly, x="hour_local", y="mean", marker="o")
    plt.title("Average demand by local hour")
    plt.xlabel("Hour (Europe/Berlin)"); plt.ylabel("Mean reported load (MW)")
    plt.tight_layout(); plt.savefig(figures_dir / "mean_demand_by_hour.png", dpi=160); plt.close()
    paired = df[["temperature_c", "demand_mw"]].dropna()
    if not paired.empty:
        sample = paired.sample(min(len(paired), 15000), random_state=42)
        plt.figure(figsize=(9, 5))
        sns.scatterplot(data=sample, x="temperature_c", y="demand_mw", alpha=0.25, s=12)
        plt.title("Demand and country-level temperature (descriptive association)")
        plt.xlabel("Temperature (°C)"); plt.ylabel("Reported load (MW)")
        plt.tight_layout(); plt.savefig(figures_dir / "demand_vs_temperature.png", dpi=160); plt.close()
    print(f"Analysis outputs saved under {report_dir}")
    print("Read summary_metrics.json and inspect data_quality.json before writing conclusions.")

if __name__ == "__main__":
    main()
