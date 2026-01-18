import psycopg2 
from ingestion.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def evaluate_run_status(run_id):
    
    conn = psycopg2.connect(
        host = DB_HOST,
        port = DB_PORT,
        
    )