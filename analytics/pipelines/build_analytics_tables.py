from utils.db import get_connection


CREATE_ANALYTICS_TABLES_SQL = """
CREATE SCHEMA IF NOT EXISTS analytics;
DROP TABLE IF EXISTS analytics.analytics_listening_events;
DROP TABLE IF EXISTS analytics.analytics_user_metrics;
"""

ANALYTICS_LISTENING_EVENTS_SQL = """
CREATE TABLE analytics.analytics_listening_events AS
SELECT DISTINCT
    r.user_id,
    r.track_id,
    r.played_at,
    r.ingested_at,
    r.raw_payload -> 'track' ->> 'name' as track_name,
    r.raw_payload -> 'track' -> 'album' ->> 'name'  as album_name,
    r.raw_payload -> 'track' -> 'artists' -> 0 ->> 'name' as artist_name,
    (r.raw_payload -> 'track' ->> 'duration_ms')::INT as duration_ms
FROM raw_listening_events r
WHERE r.track_id IS NOT NULL;
"""

ANALYTICS_USER_METRICS_SQL = """
DROP TABLE IF EXISTS analytics.analytics_user_metrics;
CREATE TABLE analytics.analytics_user_metrics AS
SELECT
    user_id,
    COUNT(*) AS total_plays,
    COUNT(DISTINCT artist_name) AS unique_artists,
    COUNT(DISTINCT track_id) AS unique_tracks,
    MIN(played_at) AS first_listen,
    MAX(played_at) AS last_listen
FROM analytics.analytics_listening_events
GROUP BY user_id;
"""


def run_sql(sql: str) -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    finally:
        conn.close()

def main():
    print("Building analytics tables.")

    run_sql(CREATE_ANALYTICS_TABLES_SQL)
    run_sql(ANALYTICS_LISTENING_EVENTS_SQL)
    run_sql(ANALYTICS_USER_METRICS_SQL)

    print("analytics tables built successfully.")
    
if __name__ == "__main__":
    main()
