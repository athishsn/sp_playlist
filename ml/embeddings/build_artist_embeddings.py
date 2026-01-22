import psycopg2
import pandas as pd 
from datetime import datetime, timezone


from ingestion.config import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
)

from utils.db import get_connection
from ml.features.time_decay import exponential_decay

def main():
    
    conn = get_connection()
    
    df = pd.read_sql(
        """
        SELECT 
            user_id, 
            artist_name,
            played_at 
        FROM analytics.analytics_listening_events
        
        """, conn
    )
    
    conn.close()
    now = datetime.now(timezone.utc)
    
    df['recency_weight'] = df['played_at'].apply(
        lambda x:exponential_decay(x,now)
    )
    
    #aggregate users contribution per artist 
    
    artist_user_matrix = (
        df.groupby(['artist_name','user_id'])['recency_weight']
        .sum()
        .reset_index()
    )
 
    #pivot -> artist X user matrix 
    
    artist_vector =  artist_user_matrix.pivot(
        index='artist_name',
        columns='user_id',
        values='recency_weight'
    )   
    
    print(artist_vector)
    
    artist_vector.to_csv('artist_embeddings.csv')
    print('saved artist_embeddings.csv')
    
if __name__ == "__main__":
    main()
    
    
    
    