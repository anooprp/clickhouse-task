import psycopg
import os
import argparse
import clickhouse_connect
import pandas as pd

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "psql_source")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")

CLICKHOUSE_HOST = os.environ.get("CLICKHOUSE_HOST", "ch_analytics")
CLICKHOUSE_USER = os.environ.get("CLICKHOUSE_USER", "clickhouse")
CLICKHOUSE_PASSWORD = os.environ.get("CLICKHOUSE_PASSWORD", "clickhouse")


# Create ClickHouse client
def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=8123,  # Default ClickHouse port
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database='default'
    )


def get_table_timestamp_column(table_name):
    client = get_clickhouse_client()
    column = None

    result = client.query(f"DESCRIBE TABLE {table_name}")
    col_map = {row[0]: row[1] for row in result.result_rows}

    if "updated_at" in col_map and "DateTime" in col_map["updated_at"]:
        column = "updated_at"
    elif "created_at" in col_map and "DateTime" in col_map["created_at"]:
        column = "created_at"

    client.close()
    return column


def get_last_sync_time(table_name, timestamp_column):
    if not timestamp_column:
        return None

    client = get_clickhouse_client()
    result = client.query(f"SELECT MAX({timestamp_column}) FROM {table_name}")
    client.close()
    return result.result_rows[0][0]


def fetch_from_postgres(table_name, timestamp_column=None, last_sync=None):
    conn = psycopg.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

    with conn.cursor() as cur:
        if timestamp_column and last_sync:
            query = f"SELECT * FROM {table_name} WHERE {timestamp_column} > '{last_sync}'"
            print(query)
            cur.execute(query)
        else:
            print(f"SELECT * FROM {table_name}")
            cur.execute(f"SELECT * FROM {table_name}")

        data = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

    conn.close()
    return data, colnames


def load_into_clickhouse(table_name, data, colnames):
    if not data:
        print(f"[{table_name}] No new rows to insert.")
        return

    client = get_clickhouse_client()

    # Prepare the data as a list of dictionaries
    formatted_data = [
        {colnames[i]: row[i] for i in range(len(colnames))}
        for row in data
    ]
    client.insert(table_name, formatted_data)

    # Optionally, print the row count
    row_count = client.query(f"SELECT count(*) FROM {table_name}")
    print(f"Total rows in ClickHouse: {row_count.result_rows[0][0]}")

    client.close()

def insert_into_clickhouse(table_name, data):
    client = get_clickhouse_client()

    # Prepare the data to insert, dynamically ensuring types are correct
    formatted_data = []
    for row in data:
        formatted_row = []
        for value in row:
            # Ensure correct types based on value (e.g., for numeric values)
            if isinstance(value, str):
                formatted_row.append(value)
            elif isinstance(value, (int, float)):
                formatted_row.append(value)
            else:
                # Handle any other types like None or date fields
                formatted_row.append(value if value is not None else '')
        formatted_data.append(formatted_row)

    # Insert data into ClickHouse
    client.insert(table_name, formatted_data)

    # Optionally, print the row count
    row_count = client.query(f"SELECT count(*) FROM {table_name}")
    print(f"Total rows in ClickHouse: {row_count.result_rows[0][0]}")

    client.close()

def load_parquet_to_clickhouse(table_name, parquet_file_path):
    client = get_clickhouse_client()

    # Read Parquet file into DataFrame
    df = pd.read_parquet(parquet_file_path)
    print(df)

    # Insert DataFrame into ClickHouse
    print('Inserting data using dataframe ')
    client.insert_df(table_name, df)

    # Optionally, print the row count
    row_count = client.query(f"SELECT count(*) FROM {table_name}")
    print(f"Total rows in ClickHouse: {row_count.result_rows[0][0]}")

    client.close()


def convert_postgres_to_parquet(table_name):
    # Fetch all data from the PostgreSQL table
    data, colnames = fetch_from_postgres(table_name)

    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=colnames)

    # Save DataFrame as a Parquet file
    parquet_file_path = f"/tmp/{table_name}.parquet"
    print('Converting to Parquet')
    df.to_parquet(parquet_file_path)

    return parquet_file_path


def sync_table(table_name, reset=False):
    timestamp_column = get_table_timestamp_column(table_name)

    if reset:
        # Full load with reset
        run_clickhouse_sql(f"TRUNCATE TABLE {table_name}")
        print(f"[{table_name}] ClickHouse table reset.")

        # Full load using Parquet
        print(f"[{table_name}] Full load initiated using Parquet.")
        parquet_file_path = convert_postgres_to_parquet(table_name)
        load_parquet_to_clickhouse(table_name, parquet_file_path)
    else:
        # Incremental load using cursors
        last_sync = get_last_sync_time(table_name, timestamp_column)
        data, colnames = fetch_from_postgres(table_name, timestamp_column, last_sync)
        insert_into_clickhouse(table_name, data)


def run_clickhouse_sql(sql):
    client = get_clickhouse_client()
    result = client.query(sql)
    client.close()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync a table from Postgres to ClickHouse.")
    parser.add_argument("table_name", help="Name of the table to sync.")
    parser.add_argument("--reset", action="store_true", help="Reset ClickHouse table before loading (Full load).")
    args = parser.parse_args()

    sync_table(args.table_name, reset=args.reset)
