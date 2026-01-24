# 🎧 Spotify Listening Analytics Platform

## End-to-End Data Engineering & Applied ML System

### Overview

This project is a production-style data platform that ingests Spotify listening data, validates it, transforms it into analytics-ready tables, applies machine learning to understand listening behavior, and surfaces insights through dashboards and recommendations.

The system is designed with real-world data engineering principles:

Incremental ingestion

Idempotent pipelines

QA & data validation

Analytics modeling

ML feature engineering

Orchestration-ready architecture

Spotify is treated as an external, best-effort data source, similar to how third-party APIs are handled in production.


## High-Level Architecture

        Spotify API
            ↓
        Ingestion Layer (Python)
            ↓
        Raw Tables (Postgres)
            ↓
        QA & Validation Layer
            ↓
        Analytics Tables
            ↓
        ML Feature Engineering
            ↓
        Clustering & Recommendations
            ↓
        Dashboards (Marimo)

## Repository Structure

        spotify_playlist/
        │
        ├── ingestion/                # Data ingestion layer
        │   ├── spotify_client.py     # Spotify API client
        │   ├── ingestion_listening.py# Recently-played ingestion job
        │   ├── ingest_audio_features.py (best-effort)
        │   ├── state_store.py        # Incremental ingestion state
        │   ├── config.py             # Environment configuration
        │   └── __init__.py
        │
        ├── db/                       # Database schemas
        │   ├── schema.sql            # Raw tables
        │   ├── analytics.sql         # Analytics tables
        │   └── audio_features.sql    # Audio feature table
        │
        ├── qa/                       # Data quality framework
        │   ├── qa_engine.py          # Generic QA execution engine
        │   ├── checks.py             # Table-specific checks
        │   ├── run_qa.py             # QA entrypoint
        │   └── __init__.py
        │
        ├── analytics/
        │   ├── sql/                  # Analytics SQL transformations
        │   ├── pipelines/            # Analytics build scripts
        │   └── dashboards/           # Marimo dashboards
        │
        ├── ml/
        │   ├── features/             # Feature engineering
        │   ├── clustering/           # Session clustering & personas
        │   └── recommenders/         # Playlist generation logic
        │
        ├── utils/
        │   └── db.py                 # Shared DB utilities
        │
        ├── docker-compose.yml        # Local Postgres
        ├── Dockerfile                # (to be added)
        ├── requirements.txt
        └── README.md



## Database Layer
### Postgres (Dockerized)

Local Postgres runs via Docker for reproducibility.

** Start DB **

        docker compose up -d


** Connect **

        docker exec -it spotify_postgres psql -U postgres -d spotify

#### Core Tables
- Raw Listening Events
    raw_listening_events


    Stores raw Spotify listening events exactly as received.

    Purpose:

    Immutable source of truth

    Enables replay & reprocessing

- Ingestion State
    ingestion_state


    Tracks the last successfully ingested timestamp per pipeline.

    Purpose:

    Incremental ingestion

    Safe retries

    No duplicate ingestion

#### QA Results
- qa_validation_results

    Stores results of QA checks (PASS / WARN / FAIL).

    Purpose:

    Data observability

    Pipeline health tracking

- Analytics Tables
    analytics.analytics_listening_events
    analytics.analytics_user_metrics


    Purpose:

    Clean, analytics-ready views

    Downstream ML consumption

## Ingestion Layer

- spotify_client.py

Encapsulates all Spotify API interactions.

Responsibilities:
OAuth token refresh
Rate-limit handling
API retries
Endpoint isolation

- ingestion_listening.py

Incrementally ingests recently played tracks.
Flow:

Read last timestamp from ingestion_state
Call Spotify API with after cursor
Insert new events into raw_listening_events
Update ingestion state


**Run**
        python -m ingestion.ingestion_listening

- ingest_audio_features.py (Best-Effort)

    Fetches track-level audio features when permitted.

Notes:
Batched (100 IDs max)
Idempotent inserts
Non-blocking for core pipeline

**Run**

    python -m ingestion.ingest_audio_features


Failures here do not break the platform.

## QA & Validation Layer

- qa_engine.py

A generic QA execution engine.

Supports:

Boolean checks (table exists)
Count checks (row count > 0)
Null checks
Duplicate checks
Severity levels (PASS / WARN / FAIL)
Results are persisted to Postgres.

- checks.py

Declarative QA rules per table.

Example:

{
  "check_type": "null_track_id",
  "sql": "SELECT COUNT(*) FROM raw_listening_events WHERE track_id IS NULL",
  "severity": "FAIL",
  "mode": "count"
}

**Run QA**
        python -m qa.run_qa

## Analytics Layer
Purpose

Transform raw data into stable, queryable analytics tables.

analytics/sql/*.sql

Contains pure SQL transformations:

Daily listening trends

User-level aggregates

Artist-level stats

Build Analytics Tables

        python -m analytics.pipelines.build_analytics_tables
        python -m analytics.pipelines.refresh_user_metrics


## ML & Feature Engineering

Sessionization

Listening events are grouped into sessions using a time gap heuristic.

Used for:
Behavioral analysis
Contextual clustering

## Feature Engineering

Located in ml/features/

Features include:
    Session length
    Unique artists
    Start hour
    Recency decay

**Run**

        python -m ml.features.build_user_features

### Clustering & Personas

Located in ml/clustering/

#### KMeans clustering on sessions

Dynamic cluster sizing

Human-readable persona labels

**Run**

        python -m ml.clustering.session_clustering
        python -m ml.clustering.persona_labels

## Recommendations

Approach

Session-based behavioral similarity

Persona-aware rules
Explainable logic (no black boxes)


- playlist_generator.py

Generates playlists based on:

Recent persona
Listening history
Artist co-occurrence

**Run**

        python -m ml.recommenders.playlist_generator

## Dashboards (Marimo)
Why Marimo?

Deterministic execution

Declarative UI

Production-friendly notebooks

Available Dashboards

Listening overview

Trends

Personas

Playlists

**Run**

        marimo run analytics/dashboards/overview.py
        marimo run analytics/dashboards/playlist.py

-------------------------------------------------------------------------------

        🔁 Typical End-to-End Flow
        # 1. Start DB
        docker compose up -d

        # 2. Ingest data
        python -m ingestion.ingestion_listening

        # 3. Run QA
        python -m qa.run_qa

        # 4. Build analytics
        python -m analytics.pipelines.build_analytics_tables
        python -m analytics.pipelines.refresh_user_metrics

        # 5. Build ML features
        python -m ml.features.build_user_features

        # 6. Cluster sessions
        python -m ml.clustering.session_clustering
        python -m ml.clustering.persona_labels

        # 7. Generate playlist
        python -m ml.recommenders.playlist_generator

        # 8. Launch dashboards
        marimo run analytics/dashboards/overview.py
