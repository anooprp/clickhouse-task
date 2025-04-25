import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from utils.sql_loader import load_sql_file

def test_valid_sql_file():
    sql = load_sql_file("sample.sql")  # Assumes this file exists in /sql
    assert isinstance(sql, str)
    assert "SELECT 'Hello World' as col" in sql
    print("✅ test_valid_sql_file OK")

def test_missing_sql_file():
    with pytest.raises(FileNotFoundError):
        load_sql_file("nonexistent_file.sql")

    print("✅ test_missing_sql_file OK")


if __name__ == "__main__":
    test_valid_sql_file()
    test_missing_sql_file()
