import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "data" / "warehouse" / "pension_analytics.db"


def main():

    connection = sqlite3.connect(DATABASE)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        with connection:

            connection.execute("""
                CREATE TABLE fact_pension_claims_new (
                    observation_id INTEGER PRIMARY KEY,
                    measure_code TEXT NOT NULL,
                    value REAL NOT NULL,
                    scheme_key INTEGER NOT NULL,
                    provider_key INTEGER NOT NULL,
                    status_key INTEGER NOT NULL,
                    period_key INTEGER NOT NULL,

                    FOREIGN KEY (scheme_key)
                        REFERENCES dim_pension_scheme(scheme_key),

                    FOREIGN KEY (provider_key)
                        REFERENCES dim_pension_provider(provider_key),

                    FOREIGN KEY (status_key)
                        REFERENCES dim_claim_status(status_key),

                    FOREIGN KEY (period_key)
                        REFERENCES dim_period(period_key),

                    UNIQUE (
                        measure_code,
                        scheme_key,
                        provider_key,
                        status_key,
                        period_key
                    )
                )
            """)

            connection.execute("""
                INSERT INTO fact_pension_claims_new
                SELECT
                    observation_id,
                    measure_code,
                    value,
                    scheme_key,
                    provider_key,
                    status_key,
                    period_key
                FROM fact_pension_claims
            """)

            connection.execute("DROP TABLE fact_pension_claims")

            connection.execute("""
                ALTER TABLE fact_pension_claims_new
                RENAME TO fact_pension_claims
            """)

        print("Fact table migration completed successfully.")

        count = connection.execute(
            "SELECT COUNT(*) FROM fact_pension_claims"
        ).fetchone()[0]

        print(f"Preserved records: {count:,}")

        violations = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if violations:
            raise RuntimeError(
                f"Foreign key violations detected: {violations}"
            )

        print("Foreign key validation passed.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()