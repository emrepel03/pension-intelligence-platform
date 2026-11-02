import sqlite3
import pandas as pd

DB_PATH = "data/warehouse/pension_analytics.db"
OUTPUT_PATH = "data/processed/reconciliation_exceptions.csv"


def run_reconciliation(
    conn,
    check_name,
    dimension_column,
    total_code,
    detail_codes,
    filter_column,
    filter_code
):

    placeholders = ", ".join(["?"] * len(detail_codes))

    query = f"""
        SELECT
            p.year,

            SUM(CASE
                WHEN {dimension_column} = ?
                THEN f.value ELSE 0
            END) AS cbs_total,

            SUM(CASE
                WHEN {dimension_column} IN ({placeholders})
                THEN f.value ELSE 0
            END) AS calculated_total

        FROM fact_pension_claims f

        JOIN dim_pension_scheme ps
            ON f.scheme_key = ps.scheme_key

        JOIN dim_pension_provider pp
            ON f.provider_key = pp.provider_key

        JOIN dim_claim_status cs
            ON f.status_key = cs.status_key

        JOIN dim_period p
            ON f.period_key = p.period_key

        WHERE
            f.measure_code = 'M002011'
            AND pp.provider_code = 'T001424'
            AND {filter_column} = ?

        GROUP BY p.year
        ORDER BY p.year
    """

    params = [total_code] + detail_codes + [filter_code]

    df = pd.read_sql_query(query, conn, params=params)

    df["difference"] = df["cbs_total"] - df["calculated_total"]

    df["check_name"] = check_name

    df["status"] = df["difference"].apply(
        lambda x: "PASS" if x == 0 else "WARNING"
    )

    return df[
        [
            "check_name",
            "year",
            "cbs_total",
            "calculated_total",
            "difference",
            "status"
        ]
    ]


def main():

    with sqlite3.connect(DB_PATH) as conn:

        status_report = run_reconciliation(
            conn,
            "Claim status reconciliation",
            "cs.status_code",
            "T001470",
            ["A046444", "A046445", "A049749"],
            "ps.scheme_code",
            "T001425"
        )

        scheme_report = run_reconciliation(
            conn,
            "Pension scheme reconciliation",
            "ps.scheme_code",
            "T001425",
            ["A045413", "A045414", "A049748"],
            "cs.status_code",
            "T001470"
        )

        report = pd.concat(
            [status_report, scheme_report],
            ignore_index=True
        )

        report.to_csv(OUTPUT_PATH, index=False)

        print("\nRECONCILIATION REPORT")
        print("=" * 65)
        print(report.to_string(index=False))

        print("\nSUMMARY")
        print("=" * 65)
        print("Total checks:", len(report))
        print("Passed:", (report["status"] == "PASS").sum())
        print("Warnings:", (report["status"] == "WARNING").sum())

        print(f"\nReport saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()