import os
import requests
import math


# Function to get route directions from OpenRouteService API
def get_route(start_lat, start_lng, finish_lat, finish_lng):
    api_key = os.getenv('OPENROUTESERVICE_API_KEY')
    
    if not api_key:
        raise ValueError("API key is missing. Please set the OPENROUTESERVICE_API_KEY environment variable.")
    
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': api_key,
    }

    json_data = {
        'coordinates': [
            [start_lng, start_lat],
            [finish_lng, finish_lat],
        ],
    }

    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    response = requests.post(url, headers=headers, json=json_data)
    return response.json()


# Helper function to calculate distance between two points (latitude, longitude) using haversine formula
def distance_to(point1, point2):
    lon1, lat1 = point1
    lon2, lat2 = point2
    R = 6371  # Radius of Earth in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers
