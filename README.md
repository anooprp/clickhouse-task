# Data Engineering : AdTech Data Pipeline

## Overview


The source data is stored in **PostgreSQL** (operational database) and needs to be transformed and loaded into **ClickHouse** (analytical database) for efficient reporting and KPI analysis.

This project provides a complete, Dockerized environment that includes:
- A Flask-based web interface for running ETL processes with a single click.
- Backend scripts for syncing data from PostgreSQL to ClickHouse.
- Predefined SQL for schema creation and KPI calculation.

---

## Features

- 🐳 **Dockerized Setup**: Easily spin up all dependencies using Docker Compose.
- 🧩 **Modular ETL**: Sync individual tables or run batch loads via backend scripts.
- 🖱️ **Web UI**: Start ETL jobs via simple button clicks on a lightweight web app.
- ⚡ **ClickHouse Optimized**: Schemas designed for fast analytical queries.

---

## Prerequisites

Make sure you have the following installed:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python environment tool)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-repo/clickhouse-task.git
cd clickhouse-task
```

### 2. Start the environment

```bash
uv sync
docker-compose up --build
```

This will spin up the necessary services including:
- PostgreSQL
- ClickHouse
- A Python Flask app (on port **8000**)

### 3. Access the Web UI

Once the containers are running, open your browser and navigate to:

```
http://localhost:8000
```

From the UI, you can:
- Trigger ETL syncs for individual tables (`Advertiser`, `Campaign`, `Impressions`, `Clicks`)
- Run a full batch data/reset  for Postgres source system

---

## Project Structure

```
.
├── app.py                 # Flask web server
├── main.py                # Entry point for batch load
├── etl/                   # ETL logic and sync scripts
├── sql/                   # KPI query definitions
├── migrations/            # Source and destination schema
├── templates/*.html       # Web UI template
├── utils/                 # SQL helpers
├── docker-compose.yaml    # Service orchestration
```

---

## ETL Actions

### 🖱️ Via Web UI

Buttons available on the homepage:

- ✅ Sync `Advertiser`
- ✅ Sync `Campaign`
- ✅ Sync `Impressions`
- ✅ Sync `Clicks`
- 🚀 Run full batch load (with random test data in source table)

Each button triggers a subprocess that runs Python scripts via `uv`.

### 🧪 Manually (from CLI)

You can also run syncs directly inside the container:

```bash
# Example: Sync the 'clicks' table with reset
docker exec -it my_python_app /bin/bash

uv run python etl/sync_src_dest.py clicks --reset

# Or run the full batch load:
uv run python main.py batch --advertisers 5 --campaigns 3 --impressions 1000 --ctr 0.07
```

---

## Notes

- All Python commands run using `uv`, which provides isolated virtual environments and faster execution.
- Analytical queries are found in the `sql/` folder.
- ClickHouse and PostgreSQL are initialized with migrations located in the `migrations/` directory.

---

