import requests
import json

# Example with NASA NeoWs API - Near Earth Object Web Service for Asteroid information
# Transform the data response from json to a python dictionary

API_KEY = 'API_KEY' # stored inside .env file

response = requests.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2025-09-07&end_date=2025-09-08&api_key={API_KEY}")
data = response.json()
formatted_data = json.dumps(data, indent=2)
# print(formatted_data)

# id, name, estimated diameter > feet > estimated_diameter_max, 
# is_potentially_hazardous_asteroid (BOOL), close_approach_data > close_approach_date_full
# miss_distance > miles, 

# Get tomorrow's asteroid data
# Represent each asteroid on a graph by size using the average diameter
# Show their distance in miles away from the earth

example_asteroid = {
    "links": {
        "self": "http://api.nasa.gov/neo/rest/v1/neo/3545713?api_key=S7jg6teRf99TsK7cokbQsGnN97Fp0ylojTFHZnq8"
    },
    "id": "3545713",
    "neo_reference_id": "3545713",
    "name": "(2010 RJ43)",
    "nasa_jpl_url": "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=3545713",
    "absolute_magnitude_h": 23.7,
    "estimated_diameter": {
        "kilometers": {
            "estimated_diameter_min": 0.0483676488,
            "estimated_diameter_max": 0.1081533507
        },
        "meters": {
            "estimated_diameter_min": 48.3676488219,
            "estimated_diameter_max": 108.1533506775
        },
        "miles": {
            "estimated_diameter_min": 0.0300542543,
            "estimated_diameter_max": 0.0672033557
        },
        "feet": {
            "estimated_diameter_min": 158.6865169607,
            "estimated_diameter_max": 354.8338390368
        }
    },
    "is_potentially_hazardous_asteroid": False,
    "close_approach_data": [
        {
            "close_approach_date": "2025-09-07",
            "close_approach_date_full": "2025-Sep-07 13:04",
            "epoch_date_close_approach": 1757250240000,
            "relative_velocity": {
                "kilometers_per_second": "10.7198701969",
                "kilometers_per_hour": "38591.532708975",
                "miles_per_hour": "23979.2776435295"
            },
            "miss_distance": {
                "astronomical": "0.25377004",
                "lunar": "98.71654556",
                "kilometers": "37963457.4538148",
                "miles": "23589398.60685224"
            },
            "orbiting_body": "Earth"
        }
    ],
    "is_sentry_object": False
}

# Access the value like this:
is_hazardous = example_asteroid["is_potentially_hazardous_asteroid"]
print(is_hazardous)  # Will print: False

# For asteroids from the API response:
near_earth_objects = data["near_earth_objects"]
# This will be organized by date, so you'll need to specify the date first
specific_date = "2025-09-07"  # Use whatever date you're interested in
asteroids_for_date = near_earth_objects[specific_date]

# Then for each asteroid in that date:
for asteroid in asteroids_for_date:
    is_hazardous = asteroid["is_potentially_hazardous_asteroid"]
    print(f"Asteroid {asteroid['name']} hazardous?: {is_hazardous}")

