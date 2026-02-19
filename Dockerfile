# -------------------------------------------------------------
# Dockerfile  – builds the ETL image that runs the Python scripts
# -------------------------------------------------------------
FROM python:3.11-slim

# ---- System dependencies (needed for psycopg2) ----------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# ---- Working directory ----------------------------------------
WORKDIR /Junior-Data-Scientist

# ---- Install Python requirements -------------------------------
# Create a requirements.txt file in the project root (see below)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy source code -----------------------------------------
# The `scripts/` folder contains all .py files (models.py, create_tables.py, …)
COPY scripts/ ./scripts/
# The `data/` folder contains the Excel and JSON files you’ll load
COPY data/   ./data/

# ---- Default command (can be overridden by compose) ----------
# When you run `docker compose run etl <script>.py` the entrypoint below
# makes it behave like `python <script>.py`.
ENTRYPOINT ["python"]