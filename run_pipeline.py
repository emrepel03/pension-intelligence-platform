import subprocess
import sys
from pathlib import Path
from datetime import datetime
import time


PROJECT_ROOT = Path(__file__).resolve().parent


def run_step(name, command):

    print("\n" + "=" * 65)
    print(f"STARTING: {name}")
    print("=" * 65)

    step_start = time.perf_counter()

    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            check=False
        )

    except OSError as error:
        print(f"\nFAILED: {name}")
        print(f"Reason: {error}")
        sys.exit(1)

    duration = time.perf_counter() - step_start

    if result.returncode != 0:
        print(f"\nFAILED: {name}")
        print(f"Exit code: {result.returncode}")
        sys.exit(result.returncode)

    print(f"\nSUCCESS: {name}")
    print(f"Duration: {duration:.2f} seconds")


def main():

    start_time = time.perf_counter()

    print("=" * 65)
    print("PENSION INTELLIGENCE PLATFORM")
    print("END-TO-END DATA PIPELINE")
    print("=" * 65)

    steps = [
        (
            "CBS DATA INGESTION",
            [sys.executable, "src/ingestion/extract_cbs_data.py"]
        ),
        (
            "WAREHOUSE LOADING",
            [sys.executable, "src/transformation/load_warehouse.py"]
        ),
        (
            "SQL BUSINESS ANALYSIS",
            [sys.executable, "src/transformation/run_analysis.py"]
        ),
        (
            "DATA QUALITY CHECKS",
            [sys.executable, "src/quality/run_quality_checks.py"]
        ),
        (
            "RECONCILIATION REPORT",
            [sys.executable, "src/quality/generate_reconciliation_report.py"]
        ),
        (
            "POWER BI DATA EXPORT",
            [sys.executable, "src/transformation/export_powerbi_data.py"]
        ),
        (
            "AUTOMATED TESTS",
            [sys.executable, "-m", "pytest", "-v"]
        )
    ]

    for name, command in steps:
        run_step(name, command)

    duration = time.perf_counter() - start_time

    print("\n" + "=" * 65)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print(f"Total execution time: {duration:.2f} seconds")
    print(f"Completed stages: {len(steps)}")
    print("All pipeline stages completed successfully.")


if __name__ == "__main__":
    main()