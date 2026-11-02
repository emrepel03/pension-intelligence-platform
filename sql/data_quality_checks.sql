-- 1. Check duplicate observations

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT observation_id) AS unique_records
FROM fact_pension_claims;


-- 2. Check missing values

SELECT
    COUNT(*) AS missing_values
FROM fact_pension_claims
WHERE value IS NULL;


-- 3. Check negative values

SELECT
    COUNT(*) AS negative_values
FROM fact_pension_claims
WHERE value < 0;


-- DATA QUALITY CHECK 4:
-- Reconcile claim statuses against total claims

SELECT
    p.year,

    SUM(CASE
        WHEN cs.status_code = 'T001470'
        THEN f.value ELSE 0
    END) AS total_claims,

    SUM(CASE
        WHEN cs.status_code IN ('A046444', 'A046445', 'A049749')
        THEN f.value ELSE 0
    END) AS calculated_total,

    SUM(CASE
        WHEN cs.status_code = 'T001470'
        THEN f.value ELSE 0
    END)
    -
    SUM(CASE
        WHEN cs.status_code IN ('A046444', 'A046445', 'A049749')
        THEN f.value ELSE 0
    END) AS difference

FROM fact_pension_claims f
JOIN dim_claim_status cs
    ON f.status_key = cs.status_key
JOIN dim_pension_scheme ps
    ON f.scheme_key = ps.scheme_key
JOIN dim_pension_provider pp
    ON f.provider_key = pp.provider_key
JOIN dim_period p
    ON f.period_key = p.period_key

WHERE
    f.measure_code = 'M002011'
    AND ps.scheme_code = 'T001425'
    AND pp.provider_code = 'T001424'

GROUP BY p.year
ORDER BY p.year;


-- DATA QUALITY CHECK 5:
-- Reconcile individual pension schemes against total claims

SELECT
    p.year,

    SUM(CASE
        WHEN ps.scheme_code = 'T001425'
        THEN f.value ELSE 0
    END) AS total_claims,

    SUM(CASE
        WHEN ps.scheme_code IN ('A045413', 'A045414', 'A049748')
        THEN f.value ELSE 0
    END) AS calculated_total,

    SUM(CASE
        WHEN ps.scheme_code = 'T001425'
        THEN f.value ELSE 0
    END)
    -
    SUM(CASE
        WHEN ps.scheme_code IN ('A045413', 'A045414', 'A049748')
        THEN f.value ELSE 0
    END) AS difference

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

GROUP BY p.year
ORDER BY p.year;