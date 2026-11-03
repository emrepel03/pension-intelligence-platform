-- =====================================================
-- 1. Annual development of pension claims
-- =====================================================

SELECT
    p.year,
    SUM(f.value) AS total_pension_claims

FROM fact_pension_claims f

JOIN dim_period p
    ON f.period_key = p.period_key

WHERE f.measure_code = 'M002011'
  AND f.scheme_key = (
      SELECT scheme_key
      FROM dim_pension_scheme
      WHERE scheme_code = 'T001425'
  )
  AND f.provider_key = (
      SELECT provider_key
      FROM dim_pension_provider
      WHERE provider_code = 'T001424'
  )
  AND f.status_key = (
      SELECT status_key
      FROM dim_claim_status
      WHERE status_code = 'T001470'
  )

GROUP BY p.year
ORDER BY p.year;


-- =====================================================
-- 2. Annual development of accrued pension amounts
-- =====================================================

SELECT
    p.year,
    f.value * 1000 AS accrued_pension_euros

FROM fact_pension_claims f

JOIN dim_period p
    ON f.period_key = p.period_key

WHERE f.measure_code = 'M001965'
  AND f.scheme_key = (
      SELECT scheme_key
      FROM dim_pension_scheme
      WHERE scheme_code = 'T001425'
  )
  AND f.provider_key = (
      SELECT provider_key
      FROM dim_pension_provider
      WHERE provider_code = 'T001424'
  )
  AND f.status_key = (
      SELECT status_key
      FROM dim_claim_status
      WHERE status_code = 'T001470'
  )

ORDER BY p.year;


-- =====================================================
-- 3. Active vs inactive pension claims in 2025
-- =====================================================

SELECT
    s.status_name,
    f.value AS pension_claims

FROM fact_pension_claims f

JOIN dim_claim_status s
    ON f.status_key = s.status_key

JOIN dim_period p
    ON f.period_key = p.period_key

WHERE f.measure_code = 'M002011'
  AND p.year = 2025
  AND f.scheme_key = (
      SELECT scheme_key
      FROM dim_pension_scheme
      WHERE scheme_code = 'T001425'
  )
  AND f.provider_key = (
      SELECT provider_key
      FROM dim_pension_provider
      WHERE provider_code = 'T001424'
  )
  AND s.status_code IN ('A046444', 'A046445')

ORDER BY s.status_name;


-- =====================================================
-- 4. Pension claims by pension scheme in 2025
-- =====================================================

SELECT
    s.scheme_name,
    f.value AS pension_claims

FROM fact_pension_claims f

JOIN dim_pension_scheme s
    ON f.scheme_key = s.scheme_key

JOIN dim_period p
    ON f.period_key = p.period_key

WHERE f.measure_code = 'M002011'
  AND p.year = 2025
  AND f.provider_key = (
      SELECT provider_key
      FROM dim_pension_provider
      WHERE provider_code = 'T001424'
  )
  AND f.status_key = (
      SELECT status_key
      FROM dim_claim_status
      WHERE status_code = 'T001470'
  )

ORDER BY f.value DESC;

-- =====================================================
-- 5. DATA QUALITY INVESTIGATION
-- Investigate 2018 claim status reconciliation discrepancy
-- =====================================================

SELECT
    s.status_code,
    s.status_name,
    f.value AS claims
FROM fact_pension_claims f
JOIN dim_claim_status s
    ON f.status_key = s.status_key
JOIN dim_pension_scheme ps
    ON f.scheme_key = ps.scheme_key
JOIN dim_pension_provider pp
    ON f.provider_key = pp.provider_key
JOIN dim_period p
    ON f.period_key = p.period_key
WHERE
    f.measure_code = 'M002011'
    AND p.year = 2018
    AND ps.scheme_code = 'T001425'
    AND pp.provider_code = 'T001424'
ORDER BY s.status_code;