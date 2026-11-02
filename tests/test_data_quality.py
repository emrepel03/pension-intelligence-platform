import sqlite3
import pandas as pd

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