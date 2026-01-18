import psycopg2
from datetime import datetime
from ingestion.config import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
)

class StateStore:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

    def get_last_timestamp(self, pipeline_name: str):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT last_successful_timestamp
                FROM ingestion_state
                WHERE pipeline_name = %s
                """,
                (pipeline_name,)
            )
            row = cur.fetchone()
            return row[0] if row else None

    def update_timestamp(self, pipeline_name: str, ts: datetime):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ingestion_state (pipeline_name, last_successful_timestamp)
                VALUES (%s, %s)
                ON CONFLICT (pipeline_name)
                DO UPDATE SET
                    last_successful_timestamp = EXCLUDED.last_successful_timestamp,
                    updated_at = NOW()
                """,
                (pipeline_name, ts)
            )
        self.conn.commit()
