import psycopg
import os
import clickhouse_connect

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "psql_source")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")

CLICKHOUSE_HOST = os.environ.get("CLICKHOUSE_HOST", "ch_analytics")
CLICKHOUSE_USER = os.environ.get("CLICKHOUSE_USER", "clickhouse")
CLICKHOUSE_PASSWORD = os.environ.get("CLICKHOUSE_PASSWORD", "clickhouse")

# Create Postgres client
def get_postgres_client():
    return psycopg.connect(
        f"host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DB} user={POSTGRES_USER}",
        autocommit=False,
    )

# Create ClickHouse client
def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=8123,  # Default ClickHouse port
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database='default'
    )
