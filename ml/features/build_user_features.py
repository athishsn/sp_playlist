#feature 2 - user features 

import psycopg2 
import pandas as pd 
from datetime import datetime, timezone

from ingestion.config import (
    DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
)

from ml.features.time_decay import exponential_decay


def main():
    
    conn = psycopg2.connect(
        host = DB_HOST, 
        port = DB_PORT, 
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD
    )
    
    df = pd.read_sql("""
        SELECT 
            user_id, 
            artist_name,
            track_id, 
            played_at
        FROM analytics.analtyics_listening_events     
                     """, conn)
    
    conn.close()
    
    if df.empty:
        print("No data to build features.")
        return
    
    now = datetime.now(timezone.utc)
    
    # recency weights 
    
    df['recency_weights'] = df['played_at'].apply(
        lambda x:exponential_decay(x,now)
    )   
    
    user_features = []
    
    for user_id, g in df.groupby('user_id'):
        total_plays = len(g)
        unique_artists = g['artist_name'].nunique()
        unique_tracks = g['track_id'].nunique()
        
        exploration_ratio = unique_tracks/max(total_plays,1)
        
        night_ratio = (
            g['played_at'].dt.hour.isin([22, 23, 0,1,2,3]).mean()
        )
        
        recency_weighted_plays = g['recency_weights'].sum()
        
        user_features.append({
            'user_id':user_id,
            'total_plays':total_plays,
            'unique_artist':unique_artists,
            'unique_tracks':unique_tracks,
            'exploration_ratio':round(exploration_ratio,3),
            'night_listening_ratio':round(night_ratio,3),
            'recency_weighted_plays':round(recency_weighted_plays,2),
        })
        
        
    features_df = pd.DataFrame(user_features)
    
    print(features_df.head())
    features_df.to_csv("ml_user_features.csv", index=False)
    print("Saved ml_user_features.csv")


if __name__ == "__main__":
    main()
    
    