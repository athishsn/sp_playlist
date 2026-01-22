import uuid
import psycopg2
from typing import List, Dict, Any

from ingestion.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def run_checks(checks: List[Dict[str, Any]], table_name: str):
    """
    Executes QA checks and writes results to qa_validation_results.
    Returns list of tuples for logging / debugging.
    """

    run_id = str(uuid.uuid4())
    results = []

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    try:
        with conn.cursor() as cur:
            for check in checks:
                cur.execute(check["sql"])
                value = cur.fetchone()[0]

                status = "PASS"
                reason = None
                failed_row_count = 0

                mode = check.get("mode")
                severity = check.get("severity", "FAIL")

                # ----------------------------
                # BOOLEAN CHECKS
                # ----------------------------
                if mode == "boolean":
                    if not bool(value):
                        status = severity
                        reason = "boolean check failed"

                # ----------------------------
                # COUNT / NUMERIC CHECKS
                # ----------------------------
                elif mode == "count":
                    count_value = int(value)

                    comparison = check.get("comparison")
                    threshold = check.get("threshold")

                    # Health check (e.g. row_count > 0)
                    if comparison == "greater_than":
                        if count_value <= threshold:
                            status = severity
                            reason = f"value={count_value} <= threshold={threshold}"
                            failed_row_count = count_value
                        else:
                            status = "PASS"
                            failed_row_count = 0

                    # Failure count check (e.g. nulls, duplicates)
                    else:
                        failed_row_count = count_value
                        if failed_row_count > 0:
                            status = severity
                            reason = f"failed_rows={failed_row_count}"

                else:
                    raise ValueError(
                        f"Invalid mode '{mode}' for check '{check['check-type']}'"
                    )

                # Persist QA result
                cur.execute(
                    """
                    INSERT INTO qa_validation_results (
                        run_id,
                        table_name,
                        check_type,
                        status,
                        failure_reason,
                        failed_row_count
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (   
                        run_id,
                        table_name,
                        check["check_type"],
                        status,
                        reason,
                        failed_row_count,
                    ),
                )

                results.append(
                    (
                        run_id,
                        table_name,
                        check["check_type"],
                        status,
                        reason,
                        failed_row_count,
                    )
                )

        conn.commit()

    finally:
        conn.close()

    return results
