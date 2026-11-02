import sqlite3

DB_PATH = "data/warehouse/pension_analytics.db"

query = """
SELECT
    p.year,
    ps.scheme_name,
    f.value AS pension_claims
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
    AND cs.status_code = 'T001470'
    AND p.year = 2018
ORDER BY ps.scheme_name;
"""

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute(query)

    print("2018 PENSION CLAIMS BY SCHEME")
    print("-" * 65)

    for row in cursor.fetchall():
        print(row)