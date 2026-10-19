from pathlib import Path
import requests
from gridlens.config import ROOT, load_config, ensure_project_dirs

def download(url: str, destination: Path) -> None:
    if destination.exists() and destination.stat().st_size > 0:
        print(f"Already downloaded: {destination} ({destination.stat().st_size:,} bytes)")
        return
    print(f"Downloading {url}")
    with requests.get(url, stream=True, timeout=(20, 180)) as response:
        response.raise_for_status()
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("wb") as output:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output.write(chunk)
    print(f"Saved: {destination} ({destination.stat().st_size:,} bytes)")

def main() -> None:
    ensure_project_dirs()
    config = load_config()
    download(config["electricity_url"], ROOT / "data/raw" / config["electricity_filename"])
    download(config["weather_url"], ROOT / "data/raw" / config["weather_filename"])

if __name__ == "__main__":
    main()
