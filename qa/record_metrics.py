import psycopg2

from ingestion.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def record_pipeline_metrics(
    run_id:str, 
    pipeline_name:str,
    records_fetched:int, 
    records_inserted:int, 
    records_dropped:int, 
    api_calls:int, 
    ingestion_latency_sec:float, 
    duplicate_rate:float, 
    qa_failures:int, 
    run_status:str 
):
    
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
                INSERT into pipeline_run_metrics (
                run_id, 
                pipeline_name, 
                records_fetched, 
                records_inserted, 
                records_dropped,
                api_calls, 
                ingestion_latency_sec, 
                duplicate_rate, 
                qa_failures, 
                run_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                
                (
                run_id, 
                pipeline_name, 
                records_fetched, 
                records_inserted, 
                records_dropped,
                api_calls, 
                ingestion_latency_sec, 
                duplicate_rate, 
                qa_failures, 
                run_status
                    ),
            )
            
        conn.commit()
        
    finally:
        conn.close()