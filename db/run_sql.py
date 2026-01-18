import psycopg2
from typing import List, Dict , Tuple, Optional

from ingestion.config import (
    DB_HOST, 
    DB_NAME, 
    DB_PASSWORD, 
    DB_PORT, 
    DB_USER
)


def run_sql (
    query :str,
    params : Optional[tuple] = None,
    fetch:bool = True, 
    
) -> Optional[List[Tuple]]:
    
    conn = psycopg2.connect(
        host= DB_HOST,
        port = DB_PORT, 
        dbname = DB_NAME,
        user = DB_USER, 
        password = DB_PASSWORD
    )
    
    try: 
        with conn.cursor() as cur:
            cur.execute(query, params)
            
            if fetch: 
                result = cur.fetchall()
            else:
                result = None
                
        conn.commit()
        return result
            
        
    except Exception as e : 
        print(f"error while querying the sql query: {e}")
    
    finally:
        conn.close()