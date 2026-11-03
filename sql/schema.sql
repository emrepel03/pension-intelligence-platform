PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dim_pension_scheme (
    scheme_key INTEGER PRIMARY KEY,
    scheme_code TEXT UNIQUE NOT NULL,
    scheme_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_pension_provider (
    provider_key INTEGER PRIMARY KEY,
    provider_code TEXT UNIQUE NOT NULL,
    provider_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_claim_status (
    status_key INTEGER PRIMARY KEY,
    status_code TEXT UNIQUE NOT NULL,
    status_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_period (
    period_key INTEGER PRIMARY KEY,
    period_code TEXT UNIQUE NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_pension_claims (
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
);