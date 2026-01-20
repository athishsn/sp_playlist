CREATE TABLE analytics.analytics_user_metrics AS 

SELECT 
    user_id,
    COUNT(*)            AS total_plays,
    COUNT(DISTINCT artist_name) AS unique_artists,
    COUNT(DISTINCT track_id) AS unique_tracks, 
    MIN(played_at) AS first_listen,
    MAX(played_at) AS last_listen
FROM analytics.analytics_listening_events 
GROUP BY user_id