import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "cbs_pension_datasets.json"
)


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        datasets = json.load(file)

    print(f"Total datasets: {len(datasets)}\n")

    for dataset in datasets:
        print("=" * 80)
        print(f"Identifier: {dataset.get('Identifier')}")
        print(f"Title: {dataset.get('Title')}")
        print(f"Modified: {dataset.get('Modified')}")
        print(f"Status: {dataset.get('Status')}")


if __name__ == "__main__":
    main()