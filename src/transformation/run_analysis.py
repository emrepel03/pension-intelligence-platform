import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE = PROJECT_ROOT / "data" / "warehouse" / "pension_analytics.db"
QUERIES_FILE = PROJECT_ROOT / "sql" / "analysis_queries.sql"


def main():
    connection = sqlite3.connect(DATABASE)

    sql = QUERIES_FILE.read_text(encoding="utf-8")

    queries = [
        query.strip()
        for query in sql.split(";")
        if query.strip()
    ]

    for index, query in enumerate(queries, start=1):
        print("\n" + "=" * 65)
        print(f"ANALYSIS {index}")
        print("=" * 65)

        cursor = connection.execute(query)

        columns = [description[0] for description in cursor.description]

        print(" | ".join(columns))
        print("-" * 65)

        for row in cursor.fetchall():
            print(" | ".join(str(value) for value in row))

    connection.close()


if __name__ == "__main__":
    main()