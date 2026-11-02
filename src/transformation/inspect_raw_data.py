import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def load_json(filename):
    with open(RAW_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


def inspect_file(filename):
    data = load_json(filename)

    print(f"\n{'=' * 70}")
    print(filename)
    print(f"Number of records: {len(data)}")

    if data:
        print("\nFirst record:")
        print(json.dumps(data[0], indent=4, ensure_ascii=False))


def main():

    files = [
        "84184NED_observations.json",
        "84184NED_pension_schemes.json",
        "84184NED_pension_providers.json",
        "84184NED_claim_statuses.json",
    ]

    for filename in files:
        inspect_file(filename)


if __name__ == "__main__":
    main()