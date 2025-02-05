import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num
from datetime import datetime

# Example with NASA NeoWs API - Near Earth Object Web Service for Asteroid information
# Transform the data response from json to a python dictionary
API_KEY = '' # stored in .env file
START_DATE = "2025-09-07"
END_DATE = "2025-09-12"

response = requests.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date={START_DATE}&end_date={END_DATE}&api_key={API_KEY}")
data = response.json()
formatted_data = json.dumps(data, indent=2)

### SAVE DATA TO JSON FILE FOR TESTING
# with open('asteroid_example_data_raw.json', 'w') as f:
#     json.dump(data, f, indent=2)

# Extract and format asteroid data
asteroids = []
asteroid_count = 0  # Initialize counter for asteroids
threat_count = 0 # Initialize threat counter for dangerous asteroids
largest_asteroid = 0


for date in data['near_earth_objects']:
    for asteroid in data['near_earth_objects'][date]:
        asteroid_info = {
            'id': asteroid['id'],
            'name': asteroid['name'],
            'max_diameter_feet': asteroid['estimated_diameter']['feet']['estimated_diameter_max'],
            'is_hazardous': asteroid['is_potentially_hazardous_asteroid'],
            'close_approach_date': asteroid['close_approach_data'][0]['close_approach_date_full'],
            'miss_distance_miles': float(asteroid['close_approach_data'][0]['miss_distance']['miles'])
        }
        asteroids.append(asteroid_info)
        asteroid_count += 1  # Increment the counter for each asteroid

        if asteroid_info['is_hazardous']:
            threat_count += 1 # Also increment the counter for each hazardous asteroid

        if asteroid['estimated_diameter']['feet']['estimated_diameter_max'] > largest_asteroid:
            largest_asteroid = asteroid['estimated_diameter']['feet']['estimated_diameter_max']

# Print formatted results
# print("\nNEAR EARTH ASTEROIDS REPORT:")
# print("-" * 80)
# for asteroid in asteroids:
#      print(f"\nAsteroid ID: {asteroid['id']}")
#      print(f"Name: {asteroid['name']}")
#      print(f"Maximum Diameter: {asteroid['max_diameter_feet']:.2f} feet")
#      print(f"Potentially Hazardous: {asteroid['is_hazardous']}")
#      print(f"Close Approach Date: {asteroid['close_approach_date']}")
#      print(f"Miss Distance: {asteroid['miss_distance_miles']:,.2f} miles")
#      print("-" * 80)

# # Print total count of asteroids
# print(f"Total number of predicted asteroids for the given date(s): {asteroid_count}")
# print(f"Total number of potentially hazardous asteroids: {threat_count}")
# print(f"Largest asteroid reported for this period: {largest_asteroid:,.2f} max. feet in diameter")

# Now the fun part!
