-- create analytics schema if not exists 

CREATE SCHEMA IF NOT EXISTS analytics;


-- Drop existing tables if present 
DROP TABLE IF EXISTS analytics.analytics_listening_events;
DROP TABLE IF EXISTS analytics.analytics_user_metrics;