import psycopg2
import subprocess
import time
from pathlib import Path 

from ingestion.config import (
    DB_HOST, 
    DB_NAME, 
    DB_PASSWORD, 
    DB_PORT, 
    DB_USER
)


def get_connection():
    return psycopg2.connect(
        host = DB_HOST, 
        port = DB_PORT, 
        dbname = DB_NAME,
        user = DB_USER, 
        password = DB_PASSWORD
    )
    
def run_sql_file(path):
    sql_path = Path(path)
    sql = None
    last_error = None

    # macOS Docker bind mounts can intermittently raise EDEADLK (Errno 35) on reads.
    for attempt in range(5):
        try:
            sql = sql_path.read_text(encoding="utf-8")
            break
        except OSError as exc:
            last_error = exc
            if exc.errno == 35:
                time.sleep(0.2 * (attempt + 1))
                continue
            break

    # Fallback: use shell utilities to copy/read through /tmp when pathlib reads fail.
    if sql is None:
        for attempt in range(5):
            try:
                tmp_path = Path(f"/tmp/{sql_path.name}.tmp")
                subprocess.run(
                    ["/bin/cp", str(sql_path), str(tmp_path)],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                sql = subprocess.check_output(
                    ["/bin/cat", str(tmp_path)],
                    text=True,
                )
                break
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if attempt < 4:
                    time.sleep(0.2 * (attempt + 1))
                    continue
                raise

    if sql is None:
        raise RuntimeError(f"Failed to read SQL file: {sql_path}") from last_error
    
    conn = get_connection()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        
    finally:
        conn.close()
    
