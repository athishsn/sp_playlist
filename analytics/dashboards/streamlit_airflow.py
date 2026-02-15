import os
import pandas as pd
import psycopg2
import streamlit as st

st.set_page_config(page_title="Spotify Analytics", layout="wide")
st.title("Spotify Analytics (Airflow DB)")

cfg = {
    "host": os.getenv("AIRFLOW_DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("AIRFLOW_DB_PORT", "5434")),
    "dbname": os.getenv("AIRFLOW_DB_NAME", "airflow"),
    "user": os.getenv("AIRFLOW_DB_USER", "airflow"),
    "password": os.getenv("AIRFLOW_DB_PASSWORD", "airflow"),
}

st.caption(f"DB: {cfg['host']}:{cfg['port']}/{cfg['dbname']}")

with psycopg2.connect(**cfg) as conn:
    freshness = pd.read_sql_query(
        "SELECT COUNT(*) AS row_count, MAX(played_at) AS latest_played_at FROM analytics.analytics_listening_events",
        conn,
    )
    trend = pd.read_sql_query(
        "SELECT DATE(played_at) AS day, COUNT(*) AS listens FROM analytics.analytics_listening_events GROUP BY day ORDER BY day",
        conn,
    )
    top_artists = pd.read_sql_query(
        "SELECT artist_name, COUNT(*) AS plays FROM analytics.analytics_listening_events GROUP BY artist_name ORDER BY plays DESC LIMIT 10",
        conn,
    )
    user_metrics = pd.read_sql_query(
        "SELECT * FROM analytics.analytics_user_metrics ORDER BY total_plays DESC",
        conn,
    )

st.metric("Rows", int(freshness["row_count"].iloc[0]))
st.metric("Latest Played At", str(freshness["latest_played_at"].iloc[0]))

st.subheader("Trend")
st.dataframe(trend, use_container_width=True)

st.subheader("Top Artists")
st.dataframe(top_artists, use_container_width=True)

st.subheader("User Metrics")
st.dataframe(user_metrics, use_container_width=True)
