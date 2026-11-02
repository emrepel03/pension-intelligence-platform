Pension Intelligence Platform

An end-to-end data engineering and business intelligence project analysing Dutch occupational pension data using Python, SQL and Power BI.

Project Overview

The Pension Intelligence Platform transforms publicly available Dutch pension statistics into structured, validated and analysis-ready data.

The project demonstrates a complete data workflow, from API ingestion and transformation to relational data warehousing, SQL analysis, automated data quality checks and business intelligence reporting.

The analysis covers the period 2016–2025.

Business Objectives

* Analyse the historical development of occupational pension claims.
* Examine accrued gross annual pension amounts.
* Compare active and inactive pension claims.
* Analyse pension claims by pension scheme type.
* Validate data completeness, consistency and reconciliation.
* Present findings through an interactive Power BI dashboard.

Technology Stack

Technology	Purpose
Python	Data ingestion and transformation
Pandas	Data processing
Requests	CBS API integration
SQLite	Relational data warehouse
SQL	Business analysis and data modelling
Pytest	Automated testing
Power BI	Data visualisation and reporting
Git	Version control

Data Source

Statistics Netherlands (CBS).

Dataset: 84184NED — Arbeidsgerelateerd ouderdomspensioen; aanspraken, uitvoerders, regelingen.

The dataset contains annual observations covering 2016–2025.

Data Pipeline

1. Ingestion — Retrieve pension statistics and metadata from the CBS OData API.
2. Transformation — Inspect and prepare the extracted observations.
3. Data Warehousing — Load dimension and fact tables into SQLite.
4. Analysis — Execute SQL queries to identify pension trends and composition.
5. Data Quality — Perform validation and reconciliation checks.
6. Reporting — Export analytical datasets for Power BI.

Key Findings

Based on the extracted CBS data:

* 21.86 million pension claims in 2025.
* Approximately €75.86 billion in accrued gross annual pension amounts in 2025.
* Pension claims increased by approximately 9.9% between 2016 and 2025.
* Accrued gross annual pension amounts increased by approximately 40% over the same period.
* Approximately 61.9% of pension claims were classified as inactive in 2025.

These figures describe pension claims and accrued annual pension amounts, not unique individuals or pension fund assets. The growth in accrued pension amounts is nominal and is not adjusted for inflation.

Data Quality

The project includes automated checks for:

* Duplicate observations.
* Missing numerical values.
* Negative values.
* Reconciliation by pension claim status.
* Reconciliation by pension scheme.

Three source-level reconciliation exceptions were identified in the original CBS observations. These are documented separately rather than silently corrected.

Testing

The project includes automated tests using Pytest.

The current test suite contains six tests covering data quality and reconciliation reporting.

Latest test result: 6 passed.

Project Structure

pension-intelligence-platform/
├── data/
│   ├── raw/
│   ├── processed/
│   └── warehouse/
├── docs/
├── powerbi/
├── sql/
├── src/
│   ├── ingestion/
│   ├── transformation/
│   └── quality/
├── tests/
├── .gitignore
├── README.md
├── requirements.txt
└── run_pipeline.py

Running the Project

1. Install dependencies

pip install -r requirements.txt

2. Run the complete pipeline

python run_pipeline.py

3. Run automated tests

pytest -v

The pipeline retrieves current data from the CBS API, so results may change when the source dataset is updated.

Disclaimer

This is an independent portfolio project using publicly available CBS statistical data. It is intended for educational and analytical purposes and is not affiliated with CBS or any pension administrator.