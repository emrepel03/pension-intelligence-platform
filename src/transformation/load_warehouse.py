import json
import sqlite3
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
WAREHOUSE_DIR = PROJECT_ROOT / "data" / "warehouse"
DATABASE = WAREHOUSE_DIR / "pension_analytics.db"


def load_json(filename):
    with open(RAW_DIR / filename, encoding="utf-8") as file:
        return json.load(file)

def validate_observations(observations):
    """Validate raw CBS observations before warehouse loading."""

    required_fields = [
        "Id",
        "Measure",
        "Value",
        "Pensioenregelingen",
        "Pensioenuitvoerders",
        "StatusPensioenaanspraken",
        "Perioden"
    ]

    for index, item in enumerate(observations):

        missing_fields = [
            field for field in required_fields
            if field not in item or item[field] is None
        ]

        if missing_fields:
            raise ValueError(
                f"Observation {index} is missing fields: {missing_fields}"
            )

        if not isinstance(item["Value"], (int, float)):
            raise ValueError(
                f"Observation {item['Id']} has an invalid numeric value."
            )

        if not isinstance(item["Perioden"], str):
            raise ValueError(
                f"Observation {item['Id']} has an invalid period."
            )

    observation_ids = [
        item["Id"] for item in observations
    ]

    if len(observation_ids) != len(set(observation_ids)):
        raise ValueError("Duplicate observation IDs found in source data.")

    print(
        f"Source validation passed: {len(observations):,} observations."
    )

def validate_dimension_references(
    observations,
    scheme_lookup,
    provider_lookup,
    status_lookup,
    period_lookup
):
    """Ensure every observation references existing dimension records."""

    references = {
        "Pensioenregelingen": scheme_lookup,
        "Pensioenuitvoerders": provider_lookup,
        "StatusPensioenaanspraken": status_lookup,
        "Perioden": period_lookup
    }

    for field, lookup in references.items():

        source_codes = {
            item[field] for item in observations
        }

        missing_codes = source_codes - set(lookup.keys())

        if missing_codes:
            raise ValueError(
                f"Unknown {field} codes found: "
                f"{sorted(missing_codes)}"
            )

    print("Dimension reference validation passed.")

def extract_year(period_code):
    match = re.match(r"^(\d{4})", period_code)
    if not match:
        raise ValueError(f"Invalid period code: {period_code}")
    return int(match.group(1))


def main():
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    observations = load_json("84184NED_observations.json")
    schemes = load_json("84184NED_pension_schemes.json")
    providers = load_json("84184NED_pension_providers.json")
    statuses = load_json("84184NED_claim_statuses.json")

    validate_observations(observations)

    connection = sqlite3.connect(DATABASE)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        schema = (PROJECT_ROOT / "sql" / "schema.sql").read_text()
        connection.executescript(schema)

        connection.executemany("""
            INSERT INTO dim_pension_scheme (scheme_code, scheme_name)
            VALUES (?, ?)
            ON CONFLICT(scheme_code)
            DO UPDATE SET scheme_name = excluded.scheme_name
        """, [
            (item["Identifier"], item["Title"].strip())
            for item in schemes
        ])

        connection.executemany("""
            INSERT INTO dim_pension_provider (provider_code, provider_name)
            VALUES (?, ?)
            ON CONFLICT(provider_code)
            DO UPDATE SET provider_name = excluded.provider_name
        """, [
            (item["Identifier"], item["Title"].strip())
            for item in providers
        ])

        connection.executemany("""
            INSERT INTO dim_claim_status (status_code, status_name)
            VALUES (?, ?)
            ON CONFLICT(status_code)
            DO UPDATE SET status_name = excluded.status_name
        """, [
            (item["Identifier"], item["Title"].strip())
            for item in statuses
        ])

        periods = sorted({item["Perioden"] for item in observations})

        connection.executemany("""
            INSERT INTO dim_period (period_code, year)
            VALUES (?, ?)
            ON CONFLICT(period_code)
            DO UPDATE SET year = excluded.year
        """, [
            (period, extract_year(period))
            for period in periods
        ])

        scheme_lookup = dict(connection.execute(
            "SELECT scheme_code, scheme_key FROM dim_pension_scheme"
        ).fetchall())

        provider_lookup = dict(connection.execute(
            "SELECT provider_code, provider_key FROM dim_pension_provider"
        ).fetchall())

        status_lookup = dict(connection.execute(
            "SELECT status_code, status_key FROM dim_claim_status"
        ).fetchall())

        period_lookup = dict(connection.execute(
            "SELECT period_code, period_key FROM dim_period"
        ).fetchall())

        validate_dimension_references(
            observations,
            scheme_lookup,
            provider_lookup,
            status_lookup,
            period_lookup
        )

        fact_rows = [
            (
                item["Id"],
                item["Measure"],
                item["Value"],
                scheme_lookup[item["Pensioenregelingen"]],
                provider_lookup[item["Pensioenuitvoerders"]],
                status_lookup[item["StatusPensioenaanspraken"]],
                period_lookup[item["Perioden"]]
            )
            for item in observations
        ]

        connection.executemany("""
            INSERT INTO fact_pension_claims
            (
                observation_id, measure_code, value,
                scheme_key, provider_key, status_key, period_key
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(observation_id)
            DO UPDATE SET
                measure_code = excluded.measure_code,
                value = excluded.value,
                scheme_key = excluded.scheme_key,
                provider_key = excluded.provider_key,
                status_key = excluded.status_key,
                period_key = excluded.period_key
        """, fact_rows)

        connection.commit()

        print("Warehouse loaded successfully.")
        print(f"Fact records processed: {len(fact_rows):,}")

        for table in [
            "dim_pension_scheme",
            "dim_pension_provider",
            "dim_claim_status",
            "dim_period",
            "fact_pension_claims"
        ]:
            count = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            print(f"{table}: {count:,} records")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()