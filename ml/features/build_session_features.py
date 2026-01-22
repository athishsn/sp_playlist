import psycopg2 
import pandas as pd 

from ingestion.config import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
)

SESSION_GAP_MINUTES = 30 


def main():
    
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    
    df = pd.read_sql("""
        SELECT 
            user_id, 
            track_id, 
            artist_name, 
            played_at, 
        FROM analytics.analytics_listening_events
        ORDER BY user_id, played_at 
                     """, conn)
    
    
    conn.close()
    
    # time difference between each song played
    df['time_diff'] = df.groupby('user_id')['played_at'].diff()
    #calculating session based on time diff between each song played
    df['new_session'] = df['time_diff'].dt.total_seconds().fillna(0) > (SESSION_GAP_MINUTES * 60)
    #cumulative sum for each userid based on new session
    df['session_id'] = df.groupby('user_id')['new_session'].cumsum()
    
    # group by on session length- count of songs
    # unique artists and start hour of sessions based on user id
    sessions = df.groupby(['user_id']['session_id']).agg(
        session_length=('track_id','count'),
        unique_artists = ('artist_name','nuninque'),
        session_start_hour=('played_at',lambda x:x.iloc[0].hour),
    ).reset_index()
    
    print(sessions.head())
    
    sessions.to_csv('ml_session_features.csv', index=False)
    print('saved ml_session_features.csv')
    
if __name__ == "__main__":
    main()
    