import requests
import pandas as pd
import os

# Define Save Directory
save_dir = r"C:\Users\shrey\OneDrive\Desktop\1. Learning\1. Projects\2. Python\TorontoRecreation"

# Ensure the directory exists
os.makedirs(save_dir, exist_ok=True)

# API Endpoint
url = "https://services3.arcgis.com/b9WvedVPoizGfvfD/arcgis/rest/services/COT_Sports_DropIn_View/FeatureServer/0/query"

# Query Parameters
params = {
    "f": "json",
    "where": "show_on_sports_map = 'Yes'",
    "returnGeometry": "false",
    "outFields": "*",
    "outSR": "102100",
    "resultOffset": "0",
    "resultRecordCount": "2000"
}

try:
    # Fetch the data from API
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise error for bad responses (e.g., 404, 500)
    data = response.json()

    # Extract features (list of facilities)
    features = data.get("features", [])

    # Process the data
    filtered_data = []
    for feature in features:
        attributes = feature.get("attributes", {})

        facility_id = attributes.get("facility_master_id", "N/A")
        facility_name = attributes.get("complexname", "N/A")
        address = attributes.get("address", "N/A")
        website = attributes.get("website", "N/A")

        sports_a_d = attributes.get("sports_activities_a_d", "")
        sports_e_p = attributes.get("sports_activities_e_p", "")
        sports_s_z = attributes.get("sports_activities_s_z", "")

        # Combine all sports activity fields
        all_sports = ", ".join(filter(None, [sports_a_d, sports_e_p, sports_s_z]))

        # Append full record (ensure consistent columns)
        filtered_data.append([
            facility_id, facility_name, address, website,
            sports_a_d, sports_e_p, sports_s_z, all_sports  # Ensure matching columns
        ])

    # Convert to DataFrame
    df = pd.DataFrame(filtered_data, columns=[
        "Facility ID", "Facility Name", "Address", "Website",
        "Sports A-D", "Sports E-P", "Sports S-Z", "All Sports"
    ])

    # Remove duplicate entries (if any)
    df.drop_duplicates(inplace=True)

    # Define file paths
    csv_path = os.path.join(save_dir, "Toronto_Volleyball_Schedules.csv")

    # Save to Excel & CSV
    df.to_csv(csv_path, index=False)

    # Display output
    print(f"Data successfully saved!")
    print(f"CSV: {csv_path}")
    print(f"Total Records: {len(df)}\n")
    print(df.head(10))  # Display first 10 records

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")

except Exception as e:
    print(f"Unexpected Error: {e}")
