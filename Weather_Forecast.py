import requests

def get_weather_by_coordinates(api_key):
    # Prompt the user for coordinates
    latitude = input("Enter latitude: ")
    longitude = input("Enter longitude: ")

    try:
        # Construct the API endpoint URL
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

        # Make the API call
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the JSON response
        weather_data = response.json()

        # Display all available weather information
        print("\nWeather Information:")
        print(f"Location: {weather_data.get('name', 'N/A')}, {weather_data['sys'].get('country', 'N/A')}")
        print(f"Coordinates: Lat {weather_data['coord'].get('lat', 'N/A')}, Lon {weather_data['coord'].get('lon', 'N/A')}")
        print(f"Temperature: {weather_data['main'].get('temp', 'N/A')}°C")
        print(f"Feels Like: {weather_data['main'].get('feels_like', 'N/A')}°C")
        print(f"Min Temperature: {weather_data['main'].get('temp_min', 'N/A')}°C")
        print(f"Max Temperature: {weather_data['main'].get('temp_max', 'N/A')}°C")
        print(f"Pressure: {weather_data['main'].get('pressure', 'N/A')} hPa")
        print(f"Humidity: {weather_data['main'].get('humidity', 'N/A')}%")
        print(f"Weather: {weather_data['weather'][0].get('description', 'N/A')}")
        print(f"Cloudiness: {weather_data['clouds'].get('all', 'N/A')}%")
        print(f"Wind Speed: {weather_data['wind'].get('speed', 'N/A')} m/s")
        print(f"Wind Direction: {weather_data['wind'].get('deg', 'N/A')}°")
        print(f"Visibility: {weather_data.get('visibility', 'N/A')} meters")
        print(f"Rain (1h): {weather_data.get('rain', {}).get('1h', 'No rain')} mm")
        print(f"Snow (1h): {weather_data.get('snow', {}).get('1h', 'No snow')} mm")
        print(f"Sunrise: {weather_data['sys'].get('sunrise', 'N/A')} (Unix timestamp)")
        print(f"Sunset: {weather_data['sys'].get('sunset', 'N/A')} (Unix timestamp)")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError as e:
        print(f"Unexpected data format: {e}")

# API key
API_KEY = "db6d7cb04dfc004776d35d70a30a7ff2"

# Run the function
get_weather_by_coordinates(API_KEY)
