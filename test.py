from db.run_sql import run_sql

query = """
SELECT
    COUNT(*) AS total_rows,
    MIN(played_at) AS min_played_at,
    MAX(played_at) AS max_played_at
FROM raw_listening_events;
"""

result = run_sql(query)

print(result)
