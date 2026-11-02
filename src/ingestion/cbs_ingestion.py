import requests
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://datasets.cbs.nl/odata/v1/CBS/Datasets"


def get_pension_datasets():
    """Retrieve CBS datasets related to pensions."""

    params = {
        "$filter": "contains(Title,'pensioen')",
        "$select": "Identifier,Title,Modified,Status",
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    return response.json()["value"]


def main():
    print("Connecting to the CBS OData v4 API...")

    datasets = get_pension_datasets()

    output_file = RAW_DATA_DIR / "cbs_pension_datasets.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(datasets, file, indent=4, ensure_ascii=False)

    print(f"\nFound {len(datasets)} pension-related datasets.")

    for dataset in datasets[:10]:
        print(
            dataset.get("Identifier"),
            "-",
            dataset.get("Title")
        )

    print(f"\nSaved raw data to: {output_file}")
    print(f"Retrieved at: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()