FROM python:3.11-slim

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY ingestion ingestion
COPY qa qa
COPY analytics analytics
COPY ml ml
COPY utils utils
COPY db db

# Default command (override in Airflow)
CMD ["python", "-m", "ingestion.ingestion_listening"]
