import requests
import json
import logging

from pathlib import Path
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

DATASET_ID = "84184NED"

BASE_URL = (
    f"https://datasets.cbs.nl/odata/v1/CBS/{DATASET_ID}"
)

HEADERS = {
    "Accept": "application/json"
}

REQUEST_TIMEOUT = 120


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


def create_session():
    """Create an HTTP session with automatic retries."""

    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)

    return session


def fetch_all(endpoint, session):
    """Retrieve all pages from a CBS OData endpoint."""

    url = f"{BASE_URL}/{endpoint}"

    records = []
    page_number = 0

    while url:

        response = session.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON response from endpoint: {endpoint}"
            ) from error

        if not isinstance(data, dict):
            raise ValueError(
                f"Unexpected API response structure: {endpoint}"
            )

        if "value" not in data or not isinstance(data["value"], list):
            raise ValueError(
                f"Missing or invalid 'value' field: {endpoint}"
            )

        page_records = data["value"]

        records.extend(page_records)

        page_number += 1

        logger.info(
            "%s | Page %s | Retrieved %s records | Total: %s",
            endpoint,
            page_number,
            len(page_records),
            len(records)
        )

        url = data.get("@odata.nextLink")

    logger.info(
        "Completed extraction of %s: %s records across %s pages",
        endpoint,
        len(records),
        page_number
    )

    return {
        "records": records,
        "pages": page_number
    }


def save_json(filename, records):
    """Save extracted data using a temporary file."""

    output_file = RAW_DATA_DIR / filename
    temporary_file = output_file.with_suffix(".tmp")

    with open(temporary_file, "w", encoding="utf-8") as file:

        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False
        )

    temporary_file.replace(output_file)

    logger.info(
        "Saved %s records to %s",
        len(records),
        output_file
    )


def main():

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    extraction_start = datetime.now(timezone.utc)

    logger.info("Starting CBS data extraction")
    logger.info("Dataset: %s", DATASET_ID)

    endpoints = {
        "observations": "Observations",
        "pension_schemes": "PensioenregelingenCodes",
        "pension_providers": "PensioenuitvoerdersCodes",
        "claim_statuses": "StatusPensioenaansprakenCodes",
    }

    session = create_session()

    extraction_summary = {}

    try:

        for filename, endpoint in endpoints.items():

            logger.info("Extracting endpoint: %s", endpoint)

            result = fetch_all(endpoint, session)

            records = result["records"]

            save_json(
                f"{DATASET_ID}_{filename}.json",
                records
            )

            extraction_summary[endpoint] = {
                "records": len(records),
                "pages": result["pages"]
            }

    finally:
        session.close()

    metadata = {
        "dataset": DATASET_ID,
        "source": "CBS Open Data API",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "started_at": extraction_start.isoformat(),
        "endpoints": extraction_summary,
        "total_records": sum(
            endpoint["records"]
            for endpoint in extraction_summary.values()
        )
    }

    save_json(
        f"{DATASET_ID}_extraction_metadata.json",
        metadata
    )

    logger.info("CBS extraction completed successfully")
    logger.info("Total records extracted: %s", metadata["total_records"])


if __name__ == "__main__":
    main()