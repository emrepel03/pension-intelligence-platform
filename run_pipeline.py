import subprocess
import sys
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent


def run_step(name, command):

    print("\n" + "=" * 65)
    print(f"STARTING: {name}")
    print("=" * 65)

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        print(f"\nFAILED: {name}")
        sys.exit(result.returncode)

    print(f"\nSUCCESS: {name}")


def main():

    start_time = datetime.now()

    print("=" * 65)
    print("PENSION INTELLIGENCE PLATFORM")
    print("END-TO-END DATA PIPELINE")
    print("=" * 65)

    run_step(
        "CBS DATA INGESTION",
        [sys.executable, "src/ingestion/extract_cbs_data.py"]
    )

    run_step(
        "WAREHOUSE LOADING",
        [sys.executable, "src/transformation/load_warehouse.py"]
    )

    run_step(
        "SQL BUSINESS ANALYSIS",
        [sys.executable, "src/transformation/run_analysis.py"]
    )

    run_step(
        "DATA QUALITY CHECKS",
        [sys.executable, "src/quality/run_quality_checks.py"]
    )

    run_step(
        "RECONCILIATION REPORT",
        [sys.executable, "src/quality/generate_reconciliation_report.py"]
    )

    run_step(
        "AUTOMATED TESTS",
        [sys.executable, "-m", "pytest", "-v"]
    )

    duration = datetime.now() - start_time

    print("\n" + "=" * 65)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print(f"Execution time: {duration}")
    print("All pipeline stages completed successfully.")


if __name__ == "__main__":

    main()