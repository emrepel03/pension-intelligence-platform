import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE = PROJECT_ROOT / "data" / "warehouse" / "pension_analytics.db"
OUTPUT_DIR = PROJECT_ROOT / "powerbi" / "exports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


queries = {

    "annual_pension_trends": """
        SELECT
            p.year,
            f.value AS pension_claims
        FROM fact_pension_claims f
        JOIN dim_period p
            ON f.period_key = p.period_key
        JOIN dim_pension_scheme ps
            ON f.scheme_key = ps.scheme_key
        JOIN dim_pension_provider pp
            ON f.provider_key = pp.provider_key
        JOIN dim_claim_status cs
            ON f.status_key = cs.status_key
        WHERE f.measure_code = 'M002011'
          AND ps.scheme_code = 'T001425'
          AND pp.provider_code = 'T001424'
          AND cs.status_code = 'T001470'
        ORDER BY p.year
    """,

    "annual_accrued_pension": """
        SELECT
            p.year,
            f.value * 1000 AS accrued_pension_euros
        FROM fact_pension_claims f
        JOIN dim_period p
            ON f.period_key = p.period_key
        JOIN dim_pension_scheme ps
            ON f.scheme_key = ps.scheme_key
        JOIN dim_pension_provider pp
            ON f.provider_key = pp.provider_key
        JOIN dim_claim_status cs
            ON f.status_key = cs.status_key
        WHERE f.measure_code = 'M001965'
          AND ps.scheme_code = 'T001425'
          AND pp.provider_code = 'T001424'
          AND cs.status_code = 'T001470'
        ORDER BY p.year
    """,

    "claims_by_status": """
        SELECT
            p.year,
            cs.status_name,
            f.value AS pension_claims
        FROM fact_pension_claims f
        JOIN dim_period p
            ON f.period_key = p.period_key
        JOIN dim_pension_scheme ps
            ON f.scheme_key = ps.scheme_key
        JOIN dim_pension_provider pp
            ON f.provider_key = pp.provider_key
        JOIN dim_claim_status cs
            ON f.status_key = cs.status_key
        WHERE f.measure_code = 'M002011'
          AND ps.scheme_code = 'T001425'
          AND pp.provider_code = 'T001424'
          AND cs.status_code IN ('A046444', 'A046445')
        ORDER BY p.year, cs.status_name
    """,

    "claims_by_scheme": """
        SELECT
            p.year,
            ps.scheme_name,
            f.value AS pension_claims
        FROM fact_pension_claims f
        JOIN dim_period p
            ON f.period_key = p.period_key
        JOIN dim_pension_scheme ps
            ON f.scheme_key = ps.scheme_key
        JOIN dim_pension_provider pp
            ON f.provider_key = pp.provider_key
        JOIN dim_claim_status cs
            ON f.status_key = cs.status_key
        WHERE f.measure_code = 'M002011'
          AND pp.provider_code = 'T001424'
          AND cs.status_code = 'T001470'
          AND ps.scheme_code != 'T001425'
        ORDER BY p.year, ps.scheme_name
    """
}


def main():

    with sqlite3.connect(DATABASE) as connection:

        for filename, query in queries.items():

            df = pd.read_sql_query(query, connection)

            output_file = OUTPUT_DIR / f"{filename}.csv"

            df.to_csv(output_file, index=False)

            print(f"Exported {filename}: {len(df)} rows")


if __name__ == "__main__":
    main()