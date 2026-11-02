import json
import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

DATASET_ID = "84184NED"

BASE_URL = (
    f"https://datasets.cbs.nl/odata/v1/CBS/{DATASET_ID}"
)

HEADERS = {
    "Accept": "application/json"
}


def fetch_endpoint(endpoint, params=None):
    """Retrieve data from a CBS OData endpoint."""

    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    return response.json()


def save_json(filename, data):
    """Save API response as raw JSON."""

    output_file = RAW_DATA_DIR / filename

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Saved: {output_file}")


def main():

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Inspecting CBS dataset: {DATASET_ID}")

    # Dataset properties
    properties = fetch_endpoint("Properties")
    save_json(f"{DATASET_ID}_properties.json", properties)

    # Available dimensions
    dimensions = fetch_endpoint("Dimensions")
    save_json(f"{DATASET_ID}_dimensions.json", dimensions)

    # Available measures
    measures = fetch_endpoint("MeasureCodes")
    save_json(f"{DATASET_ID}_measure_codes.json", measures)

    # Sample observations
    observations = fetch_endpoint(
        "Observations",
        params={"$top": 5}
    )
    save_json(f"{DATASET_ID}_sample.json", observations)

    print("\nDATASET DIMENSIONS")

    for item in dimensions.get("value", []):
        print(item)

    print("\nAVAILABLE MEASURES")

    for item in measures.get("value", [])[:15]:
        print(item)

    print("\nSAMPLE OBSERVATIONS")

    for item in observations.get("value", []):
        print(item)


if __name__ == "__main__":
    main()