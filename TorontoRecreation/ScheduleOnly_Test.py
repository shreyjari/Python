# from flask import Flask, render_template, request
# import requests
# import pandas as pd

# app = Flask(__name__)

# @app.route('/')
# def index():
#     # URL of the API endpoint
#     location_id = 749  # Replace with the desired location ID
#     api_url = f"https://www.toronto.ca/data/parks/live/dropin/sports/{location_id}.json"
    
#     try:
#         # Fetch data from the API
#         response = requests.get(api_url)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         schedule_data = response.json()
        
#         if schedule_data:
#             # Convert JSON data to a DataFrame
#             df = pd.DataFrame(schedule_data)
            
#             # Render the data in the template
#             return render_template("schedule.html", tables=[df.to_html(classes='table table-striped', index=False)], titles=df.columns.values)
#         else:
#             return render_template("error.html", message="No schedule data available.")
    
#     except requests.exceptions.RequestException as e:
#         # Handle exceptions (e.g., network errors, invalid responses)
#         return render_template("error.html", message=f"An error occurred: {e}")

# if __name__ == '__main__':
#     app.run(debug=True)
import requests

location_id = 749
api_url = f"https://www.toronto.ca/data/parks/live/dropin/sports/{location_id}.json"

response = requests.get(api_url)
print(f"Status Code: {response.status_code}")  # Print HTTP status
print(f"Response Content: {response.text}")  # Print raw response
