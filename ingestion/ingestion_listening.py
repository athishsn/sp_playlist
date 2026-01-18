import json
import psycopg2

from datetime import datetime, timezone
from ingestion.spotify_client import SpotifyClient
from ingestion.state_store import StateStore
from ingestion.config import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD,
    INGESTION_PIPELINE_NAME
)



def ingest_recently_played():
    
    spotify = SpotifyClient()
    state = StateStore()
    
    conn = psycopg2.connect(
        host = DB_HOST,
        port = DB_PORT, 
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD
    )
    
    last_ts = state.get_last_timestamp(INGESTION_PIPELINE_NAME)
    
    if last_ts and last_ts.tzinfo is None:
        last_ts = last_ts.replace(tzinfo = timezone.utc)
    
    after_ms = int(last_ts.timestamp()* 1000) if last_ts else None
    
    items = spotify.get_recently_played(after_ts_ms=after_ms)
    
    if not items: 
        print("No new records to ingest.")
        return 
    
    max_played_at = last_ts 
    
    with conn.cursor() as cur:
        
        for item in items:
            played_at = datetime.fromisoformat(
                item["played_at"].replace("Z", "+00:00")
            )

            
            cur.execute("""
                INSERT INTO raw_listening_events (
                    user_id, 
                    track_id,
                    played_at,
                    source, 
                    raw_payload
                ) VALUES (%s, %s, %s, %s, %s)
                """,(
                    "current_user",
                    item['track']['id'],
                    played_at,
                    "spotify_api",
                    json.dumps(item)
                    )     
            )
            
            if not max_played_at or played_at >= max_played_at:
                max_played_at = played_at
            
    conn.commit()
    
    if max_played_at : 
        state.update_timestamp(INGESTION_PIPELINE_NAME, max_played_at)
        
    print(f"Ingested {len(items)} records.")
    

if __name__ == "__main__":
    ingest_recently_played()