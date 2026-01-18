CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE raw_listening_events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    track_id TEXT NOT NULL,
    played_at TIMESTAMP NOT NULL,
    ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    source TEXT NOT NULL,
    raw_payload JSONB NOT NULL
);

CREATE INDEX idx_raw_listening_user_time
ON raw_listening_events (user_id, played_at);



CREATE TABLE raw_tracks (
    track_id TEXT PRIMARY KEY,
    ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    raw_payload JSONB NOT NULL 
);


CREATE TABLE raw_audio_features (
    track_id TEXT PRIMARY KEY,
    ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    raw_payload JSONB NOT NULL 
);



-- STAGING TABLES 

CREATE TABLE stg_listening_events (
    event_id UUID PRIMARY KEY,
    user_id TEXT NOT NULL,
    track_id TEXT NOT NULL,
    played_at_utc TIMESTAMP NOT NULL,
    play_hour INT NOT NULL CHECK (play_hour BETWEEN 0 AND 23),
    play_day TEXT NOT NULL,
    is_valid BOOLEAN NOT NULL DEFAULT TRUE,
    cleaned_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_stg_listening_time
ON stg_listening_events (played_at_utc);



CREATE TABLE stg_audio_features (
    track_id TEXT PRIMARY KEY, 
    danceability FLOAT CHECK (danceability BETWEEN 0 AND 1),
    energy FLOAT CHECK (energy BETWEEN 0 AND 1),
    valence FLOAT CHECK (valence BETWEEN 0 and 1),
    tempo FLOAT CHECK (tempo BETWEEN 0 AND 300),
    loudness FLOAT, 
    acousticness FLOAT CHECK (valence BETWEEN 0 and 1),
    instrumentalness FLOAT CHECK (valence BETWEEN 0 and 1),
    speechiness FLOAT CHECK (valence BETWEEN 0 and 1),
    liveness FLOAT CHECK (valence BETWEEN 0 and 1),
    feature_missing_flag BOOLEAN NOT NULL DEFAULT FALSE, 
    cleaned_at TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE core_listening_events (
    event_id UUID PRIMARY KEY,
    user_id TEXT NOT NULL, 
    track_id TEXT NOT NULL, 
    played_at_utc TIMESTAMP NOT NULL, 
    play_hour INT NOT NULL, 
    play_day TEXT NOT NULL, 
    loaded_at TIMESTAMP NOT NULL DEFAULT NOW() 

);

CREATE UNIQUE INDEX uniq_core_event 
ON core_listening_events (user_id, track_id, played_at_utc);


CREATE TABLE core_tracks (
    track_id TEXT PRIMARY KEY, 
    artist_id TEXT, 
    duration_ms INT CHECK(duration_ms > 0),
    explicit BOOLEAN, 
    loaded_at TIMESTAMP NOT NULL DEFAULT NOW() 

);


-- QA and Data Validation tables 

CREATE TABLE qa_validation_results (
    run_id UUID, 
    table_name TEXT NOT NULL, 
    check_type TEXT NOT NULL, 
    status TEXT NOT NULL CHECK( status IN ('PASS','WARN','FAIL')),
    failure_reason TEXT, 
    failed_row_count INT DEFAULT 0, 
    checked_at TIMESTAMP NOT NULL DEFAULT NOW()
);


-- pipeline throughput metrics 


CREATE TABLE pipeline_run_metrics (
    run_id UUID PRIMARY KEY, 
    pipeline_name TEXT NOT NULL, 
    records_fetched INT NOT NULL, 
    records_inserted INT NOT NULL, 
    records_dropped INT NOT NULL,
    api_calls INT NOT NULL, 
    ingestion_latency_sec FLOAT, 
    duplicate_rate FLOAT, 
    qa_failures INT, 
    run_status TEXT CHECK(run_status IN ('SUCCESS','PARTIAL','FAILED')),
    run_timestamp TIMESTAMP NOT NULL DEFAULT NOW() 
);

-- state manangement table


CREATE TABLE ingestion_state (
    pipeline_name TEXT PRIMARY KEY,
    last_successful_timestamp TIMESTAMP, 
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);