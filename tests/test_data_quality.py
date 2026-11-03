import sqlite3
import pandas as pd
import pytest

from src.transformation.export_powerbi_data import (
    validate_export,
    expected_columns,
    OUTPUT_DIR,
)

DB_PATH = "data/warehouse/pension_analytics.db"
REPORT_PATH = "data/processed/reconciliation_exceptions.csv"


def test_no_duplicate_observations():
    with sqlite3.connect(DB_PATH) as conn:
        total, unique = conn.execute("""
            SELECT
                COUNT(*),
                COUNT(DISTINCT observation_id)
            FROM fact_pension_claims
        """).fetchone()

    assert total == unique


def test_no_missing_values():
    with sqlite3.connect(DB_PATH) as conn:
        missing = conn.execute("""
            SELECT COUNT(*)
            FROM fact_pension_claims
            WHERE value IS NULL
        """).fetchone()[0]

    assert missing == 0


def test_no_negative_values():
    with sqlite3.connect(DB_PATH) as conn:
        negative = conn.execute("""
            SELECT COUNT(*)
            FROM fact_pension_claims
            WHERE value < 0
        """).fetchone()[0]

    assert negative == 0


def test_reconciliation_report_exists():
    report = pd.read_csv(REPORT_PATH)

    assert len(report) == 20


def test_expected_reconciliation_exceptions():
    report = pd.read_csv(REPORT_PATH)

    warnings = report[report["status"] == "WARNING"]

    expected = {
        ("Claim status reconciliation", 2018),
        ("Pension scheme reconciliation", 2019),
        ("Pension scheme reconciliation", 2024),
    }

    actual = set(
        zip(warnings["check_name"], warnings["year"])
    )

    assert actual == expected


def test_reconciliation_report_has_no_unexpected_warnings():
    report = pd.read_csv(REPORT_PATH)

    assert (report["status"] == "WARNING").sum() == 3
    assert (report["status"] == "PASS").sum() == 17

def test_all_powerbi_exports_exist():
    for filename in expected_columns:
        output_file = OUTPUT_DIR / f"{filename}.csv"
        assert output_file.exists(), f"Missing export: {filename}.csv"


def test_powerbi_exports_are_not_empty():
    for filename in expected_columns:
        output_file = OUTPUT_DIR / f"{filename}.csv"
        df = pd.read_csv(output_file)

        assert not df.empty, f"{filename}.csv is empty"


def test_powerbi_exports_have_expected_columns():
    for filename, columns in expected_columns.items():
        output_file = OUTPUT_DIR / f"{filename}.csv"
        df = pd.read_csv(output_file)

        assert list(df.columns) == columns


def test_export_validation_rejects_missing_values():
    df = pd.DataFrame({
        "year": [2025],
        "pension_claims": [None],
    })

    with pytest.raises(ValueError, match="Missing values"):
        validate_export(
            "test_export",
            df,
            ["year", "pension_claims"],
        )