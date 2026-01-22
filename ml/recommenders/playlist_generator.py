import psycopg2
import pandas as pd

from ingestion.config import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
)
from ml.recommenders.persona_rules import PERSONA_RULES
from ml.recommenders.similarity_recommender import get_similar_artists


def get_latest_persona():
    df = pd.read_csv('session_clusters_labeled.csv')
    latest = df.sort_values('session_id').iloc[-1]
    return latest['persona']


def get_user_history(user_id):
    
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    
    df= pd.read_sql("""
        select artist_name, count(*) as plays 
        from analytics.analytics_listening_events
        where user_id = %s    
        group by artist_name
        """, conn, params=(user_id,)
    )
    
    conn.close()
    return df.set_index('artist_name')['plays'].to_dict()


def generate_playlist(user_id='current_user', playlist_size = 15):
     
    persona = get_latest_persona()
    rules = PERSONA_RULES.get(persona, PERSONA_RULES["Balanced Session"]) 
    
    
    history = get_user_history(user_id)
    # candidates = get_similar_artists(user_id, top_k=50)
    
    
    history_artists = list(history.keys())
    candidates = get_similar_artists(history_artists, top_k=50)

    
    playlist = []
    
    for artist, score in candidates: 
        repeats = history.get(artist, 0)
        
        if repeats > rules['max_repeats']:
            continue
        
        playlist.append({
            "artist": artist,
            "similarity_score": round(score, 3),
            "previous_plays": repeats,
            "persona": persona,
        })
        
        if len(playlist) > playlist_size:
            break 
        
    return pd.DataFrame(playlist)

if __name__ == "__main__":
    playlist = generate_playlist()
    print("\n Generated Playlist:\n")
    print(playlist)
    