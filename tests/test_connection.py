import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_connections import get_postgres_client, get_clickhouse_client

def test_postgres_connection():
    try:
        conn = get_postgres_client()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        assert cur.fetchone()[0] == 1
        conn.close()
        print("✅ Postgres connection OK")
    except Exception as e:
        assert False, f"❌ Postgres connection failed: {e}"

def test_clickhouse_connection():
    try:
        client = get_clickhouse_client()
        result = client.query("SELECT 1")
        assert result.result_rows[0][0] == 1
        client.close()
        print("✅ ClickHouse connection OK")
    except Exception as e:
        assert False, f"❌ ClickHouse connection failed: {e}"

if __name__ == "__main__":
    test_postgres_connection()
    test_clickhouse_connection()
