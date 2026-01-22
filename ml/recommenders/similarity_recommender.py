import psycopg2
import pandas as pd
import numpy as np

from ingestion.config import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
)

SESSION_GAP_MINUTES = 30


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (
        np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10
    )


def build_artist_session_matrix(user_id="current_user"):
    """
    Builds artist x session matrix from raw listening events.
    """

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    df = pd.read_sql(
        """
        SELECT
            user_id,
            artist_name,
            played_at
        FROM analytics.analytics_listening_events
        WHERE user_id = %s
        ORDER BY played_at
        """,
        conn,
        params=(user_id,)
    )

    conn.close()

    if df.empty:
        raise ValueError("No listening data found.")

    # Rebuild sessions
    df["time_diff"] = df["played_at"].diff()
    df["new_session"] = (
        df["time_diff"].dt.total_seconds().fillna(0)
        > SESSION_GAP_MINUTES * 60
    )
    df["session_id"] = df["new_session"].cumsum()

    # Artist-session co-occurrence
    artist_session = (
        df.groupby(["artist_name", "session_id"])
        .size()
        .reset_index(name="count")
    )

    matrix = artist_session.pivot(
        index="artist_name",
        columns="session_id",
        values="count"
    ).fillna(0)

    return matrix


def get_similar_artists(seed_artists, top_k=20):
    matrix = build_artist_session_matrix()

    # Only use seed artists that exist in matrix
    seed_artists = [a for a in seed_artists if a in matrix.index]

    if not seed_artists:
        raise ValueError("No seed artists found in session matrix.")

    seed_vec = matrix.loc[seed_artists].sum(axis=0).values

    scores = []
    for artist, row in matrix.iterrows():
        sim = cosine_similarity(seed_vec, row.values)
        scores.append((artist, sim))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]
