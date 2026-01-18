RAW_LISTENING_CHECKS = [
    {
        "check_type":"table-exists",
        "sql":
            """
            SELECT COUNT(*) > 0 
            FROM information_schema.tables
            WHERE table_name='raw_listening_events'
            """,
        "severity":"FAIL",
        "mode":"boolean"
    },
    
    {
        "check_type":"row_count",
        "sql":
            """
            SELECT COUNT(*) FROM raw_listening_events
            """,
        "severity":"FAIL",
        "mode":"count",
        "comparison":"greater_than",
        "threshold":0,
        
    },
    {
        "check_type":"null_track_id",
        "sql":
            """
            SELECT COUNT(*) FROM raw_listening_events
            WHERE track_id IS NULL
            """,
        "severity":"FAIL",
        "mode":"count"
    },
    {
        "check_type":"duplicate_events",
        "sql":
            """
            SELECT COUNT(*) FROM 
            (
                SELECT user_id, track_id, played_at, COUNT(*)
                FROM raw_listening_events 
                GROUP BY user_id, track_id, played_at
                HAVING COUNT(*) > 1
            )t
            
            """,
        "severity":"WARN",
        "mode":"count"
    }
       
]