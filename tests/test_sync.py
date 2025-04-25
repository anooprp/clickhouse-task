import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etl.sync_src_dest import sync_table
from utils.db_connections import get_postgres_client, get_clickhouse_client

def test_sync_table():
    conn = get_postgres_client()
    cur = conn.cursor()
    cur.execute("TRUNCATE table test_table")
    cur.execute("INSERT INTO test_table SELECT 1,current_date")
    conn.commit()
    cur.execute("SELECT * FROM test_table")
    src_data=cur.fetchone()
    print(src_data)
    conn.close()
    sync_table('test_table','True')
    client = get_clickhouse_client()
    result = client.query("SELECT * FROM test_table")
    dest_data=result.result_rows[0]
    print(dest_data)
    client.close()
    assert src_data == dest_data
    print("✅ Postgres-Clickhouse Sync OK")

if __name__ == "__main__":
    test_sync_table()