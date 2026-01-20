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
    where r.track_id IS NOT NULL;

    