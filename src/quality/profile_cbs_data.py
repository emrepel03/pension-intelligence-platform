import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
REPORT_DIR = PROJECT_ROOT / "data" / "processed"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(filename):
    with open(RAW_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


def main():

    observations = pd.DataFrame(
        load_json("84184NED_observations.json")
    )

    schemes = pd.DataFrame(
        load_json("84184NED_pension_schemes.json")
    )

    providers = pd.DataFrame(
        load_json("84184NED_pension_providers.json")
    )

    statuses = pd.DataFrame(
        load_json("84184NED_claim_statuses.json")
    )

    print("\n--- DATASET OVERVIEW ---")
    print(f"Total observations: {len(observations):,}")
    print(f"Unique measures: {observations['Measure'].nunique()}")
    print(f"Unique periods: {observations['Perioden'].nunique()}")

    print("\n--- MEASURES ---")
    print(observations["Measure"].value_counts())

    print("\n--- PENSION SCHEMES ---")
    print(schemes[["Identifier", "Title"]].to_string(index=False))

    print("\n--- PENSION PROVIDERS ---")
    print(providers[["Identifier", "Title"]].to_string(index=False))

    print("\n--- CLAIM STATUSES ---")
    print(statuses[["Identifier", "Title"]].to_string(index=False))

    print("\n--- DATA QUALITY ---")

    quality_report = pd.DataFrame({
        "column": observations.columns,
        "missing_values": observations.isna().sum().values,
        "missing_percentage": (
            observations.isna().mean().values * 100
        ),
        "data_type": observations.dtypes.astype(str).values
    })

    print(quality_report.to_string(index=False))

    print("\n--- VALUE ATTRIBUTE DISTRIBUTION ---")
    print(
        observations["ValueAttribute"]
        .value_counts(dropna=False)
    )

    print("\n--- PERIOD DISTRIBUTION ---")
    print(
        observations.groupby("Perioden")
        .size()
        .to_string()
    )

    quality_report.to_csv(
        REPORT_DIR / "data_quality_profile.csv",
        index=False
    )

    print("\nQuality profile saved.")


if __name__ == "__main__":
    main()