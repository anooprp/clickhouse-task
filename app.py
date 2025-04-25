from flask import Flask, render_template, request, jsonify
import subprocess
from etl.sync_table import run_clickhouse_sql
from utils.sql_loader import load_sql_file

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_batch')
def run_batch():
    subprocess.Popen(["uv", "run", "python", "main.py", "batch", "--advertisers", "5", "--campaigns", "3", "--impressions", "1000", "--ctr", "0.07"])
    return jsonify({"message": "Batch Load initiated."})

@app.route('/sync/<table>', methods=["GET"])
def sync_table(table):
    reset = request.args.get("reset", "false").lower() == "true"
    if table in ["clicks", "impressions", "campaign", "advertiser"]:
        cmd = ["uv", "run", "python", "etl/sync_table.py", table]
        if reset:
            cmd.append("--reset")
        subprocess.Popen(cmd)
        return jsonify({"message": f"{table.capitalize()} Sync initiated."})
    else:
        return jsonify({"error": "Invalid table name."}), 400

@app.route('/run_reset', methods=['GET'])
def run_reset():
    confirm = request.args.get('confirm', 'no')
    if confirm == 'yes':
        subprocess.Popen(["uv", "run", "python", "main.py", "reset", "--yes"])
        return jsonify({"message": "Data reset initiated."})
    else:
        return jsonify({"message": "Reset confirmation required."}), 400

@app.route("/custom_query", methods=["GET", "POST"])
def custom_query():
    error = None
    success = None
    results = None
    columns = None
    query = ""

    if request.method == "POST":
        # Get either raw query input or predefined filename
        raw_query = request.form.get("query", "").strip()  # Get raw query
        predefined_file = request.form.get("predefined_query", "").strip()  # Get predefined file name

        # If there's a predefined query, load it
        if predefined_file:
            try:
                # Load the predefined SQL query from a file
                query = load_sql_file(predefined_file)
            except Exception as e:
                error = f"Failed to load predefined query: {str(e)}"
        elif raw_query:
            # Otherwise use the raw query provided in the textarea
            query = raw_query

        # Now, execute the query if there's a valid query
        if query:
            try:
                # Execute the query using the `run_clickhouse_sql` function
                result = run_clickhouse_sql(query)
                if result.result_set:
                    columns = result.column_names
                    results = result.result_rows
                    success = "Query executed successfully."
                else:
                    success = "Query executed successfully. No results to show."
            except Exception as e:
                error = f"Query execution failed: {str(e)}"
        else:
            error = "No query provided."

    return render_template(
        "custom_query.html",
        error=error,
        success=success,
        results=results,
        columns=columns,
        query=query
    )




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000,debug=True)
