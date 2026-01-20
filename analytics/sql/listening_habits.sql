SELECT 
    CASE 
        WHEN EXTRACT(HOUR FROM played_at) BETWEEN 5 AND 11 THEN 'Morning Listener'
        WHEN EXTRACT(HOUR FROM played_at) BETWEEN 12 AND 17 THEN 'Afternoon Listener'
        WHEN EXTRACT(HOUR FROM played_at) BETWEEN 18 AND 22 THEN 'Night Listener'
        ELSE 'Night Owl'
    END AS listening_persona,
    COUNT(*) AS listens 
FROM analytics.analytics_listening_events
GROUP BY listening_persona
ORDER BY listens DESC;
