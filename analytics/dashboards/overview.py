import marimo as mo

app = mo.App()


@app.cell
def _():
    import sys
    import os
    import psycopg2
    import pandas as pd


    # Get project root (two levels up from this file)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Debug (you can remove later)
    print("Project root added to sys.path:", project_root)

    
    
    # Now the import will succeed
    from ingestion.config import (
        DB_HOST,
        DB_PORT,
        DB_NAME,
        DB_USER,
        DB_PASSWORD,
    )

    # DB connection
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    user_metrics = pd.read_sql(
        """
        SELECT *
        FROM analytics.analytics_user_metrics
        LIMIT 1
        """,
        conn,
    )

    trend = pd.read_sql(
        """
        SELECT
            DATE(played_at) AS day,
            COUNT(*) AS listens
        FROM analytics.analytics_listening_events
        GROUP BY day
        ORDER BY day
        """,
        conn,
    )

    top_artists = pd.read_sql(
        """
        SELECT
            artist_name,
            COUNT(*) AS play_count
        FROM analytics.analytics_listening_events
        GROUP BY artist_name
        ORDER BY play_count DESC
        LIMIT 10
        """,
        conn,
    )
    
    hourly = pd.read_sql(
        """
        select 
            extract(hour from played_at) as hour, 
            count(*) as listens 
        from analytics.analytics_listening_events
        group by hour 
        order by hour
        """, 
        conn
    )
    
    # Weekday vs weekend
    weekday_weekend = pd.read_sql(
        """
        SELECT
            CASE
                WHEN EXTRACT(DOW FROM played_at) IN (0, 6)
                THEN 'Weekend'
                ELSE 'Weekday'
            END AS day_type,
            COUNT(*) AS listens
        FROM analytics.analytics_listening_events
        GROUP BY day_type
        """,
        conn,
    )

    conn.close()

    return (
        DB_HOST,
        DB_NAME,
        DB_PASSWORD,
        DB_PORT,
        DB_USER,
        conn,
        current_dir,
        os,
        pd,
        psycopg2,
        sys,
        top_artists,
        trend,
        user_metrics,
        hourly, 
        weekday_weekend
        
    )


@app.cell
def _(user_metrics, hourly):
    # Check if metrics exist to avoid crashing on empty DB
    if not user_metrics.empty:
        total_plays = int(user_metrics["total_plays"].iloc[0])
        unique_artists = int(user_metrics["unique_artists"].iloc[0])

        if unique_artists / max(total_plays, 1) < 0.3:
            insight = (
                f"You played {total_plays} tracks from "
                f"**{unique_artists} unique artists**. "
                f"You tend to replay your favorites."
            )
        else:
            insight = (
                f"You’re an explorer! You played "
                f"**{unique_artists} artists** across "
                f"**{total_plays} listens**."
            )
    else:
        insight = "No listening data available yet. Run the ingestion pipeline!"
        total_plays = 0
        unique_artists = 0
        
    peak_hour = int(hourly.sort_values("listens", ascending=False).iloc[0]["hour"])

    if 5 <= peak_hour <= 11:
        persona = "🌅 Morning Listener"
    elif 12 <= peak_hour <= 17:
        persona = "☀️ Afternoon Listener"
    elif 18 <= peak_hour <= 22:
        persona = "🌆 Evening Listener"
    else:
        persona = "🌙 Night Owl"

    insight = f"Your peak listening hour is around **{peak_hour}:00**. You are a **{persona}**."


    return insight, total_plays, unique_artists, persona, insight

    



@app.cell
def _(insight, top_artists, trend, user_metrics, hourly, weekday_weekend, persona, insight):
    import marimo as mo

    mo.vstack([
        mo.md("# 🎶 Your Listening Overview"),
        
        mo.md("## 📊 Summary"),
        mo.ui.table(user_metrics),

        mo.md("## 📈 Listening Trend"),
        mo.ui.table(trend),

        mo.md("## 🎤 Top Artists"),
        mo.ui.table(top_artists),

        mo.md("## 🧠 Personal Insight"),
        mo.md(insight),
        
        mo.md("# ⏰ Listening Habits"),
        
        mo.md("## 🧠 Your Listening Persona"),
        mo.md(insight),

        mo.md("## 🕒 Listening by Hour"),
        mo.ui.table(hourly),

        mo.md("## 📅 Weekday vs Weekend"),
        mo.ui.table(weekday_weekend),
    ])



if __name__ == "__main__":
    app.run()