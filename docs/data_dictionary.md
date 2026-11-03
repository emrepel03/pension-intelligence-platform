### Dimension tables

#### dim_pension_scheme

Describes the type of pension scheme.

| Column | Description |
|---|---|
| scheme_key | Primary key |
| scheme_code | Unique CBS scheme identifier |
| scheme_name | Human-readable scheme description |

#### dim_pension_provider

Describes the type of pension provider.

| Column | Description |
|---|---|
| provider_key | Primary key |
| provider_code | Unique CBS provider identifier |
| provider_name | Human-readable provider description |

#### dim_claim_status

Describes the status of a pension claim.

| Column | Description |
|---|---|
| status_key | Primary key |
| status_code | Unique CBS status identifier |
| status_name | Human-readable status description |

#### dim_period

Contains the reporting year associated with each observation.

| Column | Description |
|---|---|
| period_key | Primary key |
| period_code | Unique CBS reporting period identifier |
| year | Reporting year |