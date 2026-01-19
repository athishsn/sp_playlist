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
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,   
    )
    
    try:
        
        with conn.cursor() as cur :
            cur.execute(
                """
                SELECT
                  SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) AS fail_count,
                  SUM(CASE WHEN status = 'WARN' THEN 1 ELSE 0 END) AS warn_count
                FROM qa_validation_results
                WHERE run_id = %s
                """,
                (run_id,),
            )
            
            fail_count, warn_count = cur.fetchone()
            
            fail_count = fail_count or 0 
            warn_count = warn_count or 0 
            
            if fail_count >0:
                return "FAILED" , fail_count
            
            if warn_count > 0 :
                return "PARTIAl", 0
            
            
            return "SUCCESS", 0 
        
    finally:
        conn.close()