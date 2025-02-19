from flask import Flask, render_template, jsonify, request
import requests
import pandas as pd

app = Flask(__name__)

BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
PACKAGE_ID = "traffic-volumes-at-intersections-for-all-modes"

def fetch_traffic_data():
    """Fetch full traffic volume data from Toronto Open Data API."""
    url = f"{BASE_URL}/api/3/action/package_show"
    params = {"id": PACKAGE_ID}
    response = requests.get(url, params=params).json()

    if not response["success"]:
        return [], []

    resources = response["result"]["resources"]
    resource_id = next((r["id"] for r in resources if r["datastore_active"]), None)

    if not resource_id:
        return [], []

    # Fetch full dataset
    url = f"{BASE_URL}/api/3/action/datastore_search"
    params = {"id": resource_id, "limit": 0}  # No limit, return all records
    data_response = requests.get(url, params=params).json()

    records = data_response.get("result", {}).get("records", [])
    columns = list(records[0].keys()) if records else []

    return columns, records

@app.route('/traffic_page')
def traffic_page():
    columns, data = fetch_traffic_data()
    return render_template('traffic.html', columns=columns, data=data)

@app.route('/api/traffic', methods=['GET'])
def get_traffic():
    """API Endpoint with Pagination & Filtering"""
    columns, data = fetch_traffic_data()

    # Get query parameters
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 100))  # Default 100 records per page
    intersection = request.args.get("intersection", "").lower()
    mode = request.args.get("mode", "").lower()

    # Filter data
    if intersection:
        data = [row for row in data if intersection in row.get("INTERSECTION_NAME", "").lower()]
    if mode:
        data = [row for row in data if mode in row.get("MODE", "").lower()]

    # Paginate
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    data_paginated = data[start:end]

    return jsonify({
        "total_records": total,
        "page": page,
        "per_page": per_page,
        "data": data_paginated
    })

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """API Endpoint to return unique intersection & mode values for search suggestions"""
    _, data = fetch_traffic_data()
    
    type = request.args.get("type", "").lower()
    
    if type == "intersection":
        values = list(set(row.get("INTERSECTION_NAME", "").strip() for row in data if row.get("INTERSECTION_NAME")))
    elif type == "mode":
        values = list(set(row.get("MODE", "").strip() for row in data if row.get("MODE")))
    else:
        return jsonify({"error": "Invalid type"}), 400

    return jsonify(sorted(values))


if __name__ == '__main__':
    app.run(debug=True)
