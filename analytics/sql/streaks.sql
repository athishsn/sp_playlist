with daily_activity as (
    select distinct 
        date(played_at) as day 
    from analytics.analytics_listening_events
),
gaps as (
    select 
        day,
        day - LAG(day) OVER (ORDER BY day) AS gap 
    from daily_activity
)

select 
    count(*) filter (where gap= interval '1 day') as consecutive_days
from gaps;