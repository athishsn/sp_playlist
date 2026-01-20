WITH track_counts as (
    SELECT 
        track_id, 
        count(*) as plays
    from analytics.analytics_listening_events
    group by track_id
)

select 
    round(
        sum( case when plays=1 then 1 else 0 end)::numeric /
        count(*), 3
    ) as exploration_ratio 
from track_counts;