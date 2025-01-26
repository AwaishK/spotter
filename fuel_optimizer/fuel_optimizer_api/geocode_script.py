import os
import requests
import csv
from fuel_optimizer_api.models import FuelStation

# Load OpenRouteService API key from environment variable
api_key = os.getenv('OPENROUTESERVICE_API_KEY')

if not api_key:
    raise ValueError("API key is missing. Please set the OPENROUTESERVICE_API_KEY environment variable.")


# Function to get coordinates (latitude, longitude) from OpenRouteService API
def get_coordinates(address):
    url = f"https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={address}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to get coordinates for address: {address}")
        return
    
    data = response.json()
    
    # Extract latitude and longitude from the geocoding API response
    try:
        lat = data['features'][0]['geometry']['coordinates'][1]
        lon = data['features'][0]['geometry']['coordinates'][0]
    except (IndexError, KeyError):
        print(f"Failed to extract coordinates for address: {address}")
        return
    
    return lat, lon


# Function to pre-geocode and store fuel station data
def geocode_and_store_fuel_stations(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            address = row['Address']
            city = row['City']
            state = row['State']
            full_address = f"{address}, {city}, {state}"

            # Check if the address already exists in the FuelStation table
            if FuelStation.objects.filter(address=address, city=city, state=state).exists():
                print(f"Address already exists: {full_address}. Skipping API call.")
                continue  # Skip API request for existing address
            
            # Get coordinates using OpenRouteService geocoding API
            coordinates = get_coordinates(full_address)
            if coordinates is None:
                continue

            latitude, longitude = coordinates
            fuel_price = float(row['Retail Price'])
            
            # Store the data in the FuelStation model
            FuelStation.objects.create(
                truckstop_id=row['OPIS Truckstop ID'],
                name=row['Truckstop Name'],
                address=address,
                city=city,
                state=state,
                retail_price=fuel_price,
                latitude=latitude,
                longitude=longitude
            )
            print(f"Stored: {full_address}, Coordinates: {latitude}, {longitude}")


fuel_file = os.getenv('FUEL_PRICES_FILEPATH')

# Check if the fuel file path is present
if not fuel_file:
    raise ValueError("Fuel file path is missing. Please set the FUEL_PRICES_FILEPATH environment variable.")

# Call the function to pre-geocode and store the data (use the appropriate CSV file path)
geocode_and_store_fuel_stations(fuel_file)
