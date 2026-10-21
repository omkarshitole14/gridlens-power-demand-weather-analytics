from pathlib import Path

import requests

from gridlens.config import ROOT, load_config, ensure_project_dirs

def has_expected_schema(path: Path, required_columns: set[str]) -> bool:
    import pandas as pd

    try:
        columns = set(pd.read_csv(path, nrows=0).columns)
        return required_columns.issubset(columns)
    except (OSError, ValueError, pd.errors.ParserError):
        return False
def download(
    url: str,
    destination: Path,
    required_columns: set[str],
) -> None:
    if destination.exists() and destination.stat().st_size > 0:
        if has_expected_schema(destination, required_columns):
            print(
                f"Already downloaded and validated: {destination} "
                f"({destination.stat().st_size:,} bytes)"
            )
            return

        print(f"Existing file has an invalid schema; downloading again: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = destination.with_name(destination.name + ".part")

    print(f"Downloading {url}")

    try:
        with requests.get(url, stream=True, timeout=(20, 180)) as response:
            response.raise_for_status()

            with temporary_file.open("wb") as output:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        output.write(chunk)

        if temporary_file.stat().st_size == 0:
            raise ValueError(f"Downloaded file is empty: {url}")

        temporary_file.replace(destination)

    except Exception:
        temporary_file.unlink(missing_ok=True)
        raise

    print(f"Saved: {destination} ({destination.stat().st_size:,} bytes)")


def main() -> None:
    ensure_project_dirs()
    config = load_config()

    download(
        config["electricity_url"],
        ROOT / "data/raw" / config["electricity_filename"],
        {
            "utc_timestamp",
            f"{config['country']}_load_actual_entsoe_transparency",
        },
    )

    download(
        config["weather_url"],
        ROOT / "data/raw" / config["weather_filename"],
        {
            "utc_timestamp",
            f"{config['country']}_temperature",
        },
    )

if __name__ == "__main__":
    main()
