# modules the api call
import requests
import json

# modules for stats
import numpy as np

# modules for visualizations
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
from plotly.subplots import make_subplots


# Initialize variables with api key, 7-day range, and api url
API_KEY = "S7jg6teRf99TsK7cokbQsGnN97Fp0ylojTFHZnq8"
START_DATE = "2025-01-24"
END_DATE = "2025-01-31"
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={START_DATE}&end_date={END_DATE}&api_key={API_KEY}"

# Retrieve data from the api and store desired values inside of a list
response = requests.get(url)
data = json.loads(response.text)
asteroids = []
for date in data['near_earth_objects']:
    for asteroid in data['near_earth_objects'][date]:
        asteroids.append({
            'name':  asteroid['name'],
            'size':  asteroid['estimated_diameter']['meters']['estimated_diameter_max'],
            'is_hazardous': asteroid['is_potentially_hazardous_asteroid']
        })

# Visualize asteroid data
fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter3d'}]])

# Earth figure represented for scale
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(theta), np.sin(phi)) * 6371  # Earth radius in km
y = np.outer(np.sin(theta), np.sin(phi)) * 6371
z = np.outer(np.ones(np.size(theta)), np.cos(phi)) * 6371

# Define a custom color scale that mimics Earth's colors
earth_colors = [
    [0.0, 'rgb(0, 0, 128)'],     # Deep Ocean
    [0.2, 'rgb(0, 191, 255)'],   # Ocean
    [0.8, 'rgb(255, 255, 255)'], # Clouds
    [1.0, 'rgb(173, 216, 230)']  # Polar Ice
]

# Add Earth to the plot with custom colorscale
fig.add_trace(go.Surface(
    x=x, y=y, z=z, 
    colorscale=earth_colors, 
    showscale=False,
    lighting=dict(ambient=0.4, diffuse=0.8, specular=0.3, roughness=0.3),
    lightposition=dict(x=100000, y=100000, z=100000)
))

# Define colors for asteroids
hazardous_color = '#FF4500'  # Neon red
non_hazardous_color = '#6FFFE9'  # Dark Turqouise

# Add Asteroids to the plot
for asteroid in asteroids:
    size_factor = asteroid['size'] / 100  # Scale down for visualization
    fig.add_trace(go.Scatter3d(
        x=[np.random.uniform(-50000, 50000)],  # Random position for simplicity
        y=[np.random.uniform(-50000, 50000)],
        z=[np.random.uniform(-50000, 50000)],
        mode='markers',
        marker=dict(
            size=size_factor,
            color=hazardous_color if asteroid['is_hazardous'] else non_hazardous_color,
            symbol='circle'
        ),
        name=asteroid['name'],
        hoverinfo='text',
        text=f"Name: {asteroid['name']}<br>Size: {asteroid['size']:.2f}m<br>Hazardous: {'Yes' if asteroid['is_hazardous'] else 'No'}"
    ))

# Update layout to remove gridlines and darken the background
fig.update_layout(scene = dict(
    xaxis_title='',
    yaxis_title='',
    zaxis_title='',
    xaxis=dict(showgrid=False, backgroundcolor='#0B132B'),
    yaxis=dict(showgrid=False, backgroundcolor='#0B132B'),
    zaxis=dict(showgrid=False, backgroundcolor='#0B132B')),
    title='Asteroids Near Earth (NASA NeoWs Data 2025)',
    margin=dict(r=20, b=10, l=10, t=40),
    paper_bgcolor='#0B132B',  # Darken the background
    plot_bgcolor='#0B132B')

fig.show()
