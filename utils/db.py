import psycopg2
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
    sql = Path(path).read_text()
    
    conn = get_connection()
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        
    finally:
        conn.close()
    