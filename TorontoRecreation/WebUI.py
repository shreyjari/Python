from flask import Flask, render_template, request
import requests
import pandas as pd

app = Flask(__name__)

# API Endpoint
url = "https://services3.arcgis.com/b9WvedVPoizGfvfD/arcgis/rest/services/COT_Sports_DropIn_View/FeatureServer/0/query"
params = {
    "f": "json",
    "where": "show_on_sports_map = 'Yes'",
    "returnGeometry": "false",
    "outFields": "*",
    "outSR": "102100",
    "resultOffset": "0",
    "resultRecordCount": "2000"
}

def fetch_data():
    response = requests.get(url, params=params)
    data = response.json()
    features = data.get("features", [])
    extracted_data = []
    for feature in features:
        attributes = feature.get("attributes", {})
        facility_id = attributes.get("facility_master_id", "N/A")
        location_id = attributes.get("locationid", "N/A")
        facility_name = attributes.get("complexname", "N/A")
        address = attributes.get("address", "N/A")
        website = attributes.get("website", "N/A")
        sports_a_d = attributes.get("sports_activities_a_d", "")
        sports_e_p = attributes.get("sports_activities_e_p", "")
        sports_s_z = attributes.get("sports_activities_s_z", "")
        all_sports = f"{sports_a_d}, {sports_e_p}, {sports_s_z}".lower()
        schedule_button = f'<a href="/schedule/{location_id}" class="btn btn-primary">View Schedule</a>' if location_id and location_id != "N/A" else "No Schedule Available"
        extracted_data.append([
            facility_id,
            location_id,
            facility_name,
            address,
            f'<a href="{website}" target="_blank">Visit Website</a>' if website and website != "N/A" else "N/A",
            all_sports,
            schedule_button
        ])
    return pd.DataFrame(extracted_data, columns=["Facility ID", "Location ID", "Facility Name", "Address", "Website", "Sports Activities", "Schedule"])

df = fetch_data()

@app.route('/')
def index():
    return render_template("index.html", tables=[df.to_html(classes='table table-striped text-center', index=False, escape=False)], titles=df.columns.values, auto_refresh=True)

@app.route('/schedule/<location_id>')
def schedule(location_id):
    schedule_url = f"https://www.toronto.ca/data/parks/live/dropin/sports/{location_id}.json"
    try:
        response = requests.get(schedule_url)
        response.raise_for_status()
        schedule_data = response.json()
        if schedule_data:
            schedule_df = pd.DataFrame(schedule_data)
            return render_template("schedule.html", schedule=schedule_df.to_html(classes='table table-striped text-center', index=False, escape=False), location_id=location_id)
        else:
            return render_template("error.html", message=f"No schedule available for Location ID: {location_id}")
    except requests.exceptions.RequestException as e:
        return render_template("error.html", message=f"Error fetching schedule for Location ID: {location_id}. {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)