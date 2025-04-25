import os
# Get the absolute directory path where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUERY_DIR = os.path.join(BASE_DIR, "../sql")

def load_sql_file(filename):
    # basic safety check
    if ".." in filename or "/" in filename:
        raise ValueError("Invalid query filename")
    filepath = os.path.join(QUERY_DIR, filename)
    with open(filepath, "r") as f:
        return f.read()
