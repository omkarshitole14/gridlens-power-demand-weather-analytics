from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "project_config.json"

def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as file:
        return json.load(file)

def ensure_project_dirs() -> None:
    for relative in ("data/raw", "data/processed", "data/metadata", "reports/figures"):
        (ROOT / relative).mkdir(parents=True, exist_ok=True)
