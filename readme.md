# Project Structure

├── spotter  
│   ├── fuel_optimizer                  
│   │   │── fuel_optimizer  
│   │   │   │── asgi.py  
│   │   │   │── settings.py  
│   │   │   │── urls.py  
│   │   │   │── wsgi.py  
│   │   │   │  
│   │   │── fuel_optimizer_api    
│   │   │   │── migrations  
│   │   │   │── admin.py  
│   │   │   │── apps.py  
│   │   │   │── geocode_script.py  
│   │   │   │── models.py  
│   │   │   │── tests.py  
│   │   │   │── urls.py  
│   │   │   │── utils.py  
│   │   │   │── views.py  
│   │   │   │  
│   │   │── db.sqlite3  
│   │   │── manage.py  
│   │   │── fuel-prices-for-be-assessment.csv  
│   │── README.md  
│   │── Makefile  
│   │── requirements.txt  
│   │── .env  
│   │── env  
│   │── .gitignore  


# Setup & Installations

1. **create virtual env and install requirements**

**Ensure that you are in the `spotter` directory, which contains the requirements.txt file, before proceeding.**

```bash
python -m venv env  
source env/bin/activate  
pip install -r requirements   
```

2. **Run the following command to navigate to the `fuel_optimizer` Django project directory**

```bash
cd fuel_optimizer
```

3. **Run the following command to start django server and then test it.**

```bash
python manage.py runserver 
```
---

Testing url: http://127.0.0.1:8000/fuel_optimizer_api/optimize_route/?start_lat=34.052235&start_lng=-118.243683&finish_lat=40.712776&finish_lng=-74.005974

---

# Explanation

# Fuel Station Geocoder and Data Storage Script (`geocode_script.py`)

This script automates the process of geocoding fuel station addresses and storing the data in a database model (`FuelStation`). It utilizes the OpenRouteService API for geocoding and is designed to handle large datasets efficiently by checking for existing records before making API requests.

---

## How It Works

1. **Environment Setup:**
   - Ensure the OpenRouteService API key is set as an environment variable (`OPENROUTESERVICE_API_KEY`).
   - Provide the file path of the fuel prices CSV file as an environment variable (`FUEL_PRICES_FILEPATH`).

2. **Geocoding Functionality:**
   - The `get_coordinates(address)` function takes a full address as input and sends a request to the OpenRouteService API.
   - The API response is parsed to extract latitude and longitude. If extraction fails, the function returns `None`.

3. **Data Storage:**
   - The script reads the input CSV file containing fuel station data.
   - For each record:
     - A check is performed to see if the address already exists in the `FuelStation` database table.
     - If not, the script retrieves the coordinates via the `get_coordinates` function.
     - The record, including fuel prices and geocoded coordinates, is stored in the database.

4. **Execution:**
   - The script reads the file path from the `FUEL_PRICES_FILEPATH` environment variable and processes the CSV file by calling the `geocode_and_store_fuel_stations(csv_file_path)` function.

## Usage

1. **Set up the required environment variables:**
   
**Add the following variables to a `.env` file in the project directory. The script will automatically load them.**

   ```bash
   OPENROUTESERVICE_API_KEY="your_api_key_here"
   FUEL_PRICES_FILEPATH="path_to_your_csv_file.csv"
   ```


# Utilities Module (`utils.py`)

This module provides utility functions for geospatial tasks.

It will be utilized from views.py. 


# Views (`views.py`)

This provides views for the django app.

## Working for optimize_route view 

    - Extract the start and finish coordinates from the query parameters.
    - Fetch the route using the `get_route` function, which returns the coordinates of the route path.
    - Query the `FuelStation` model to retrieve all available fuel stations from the database.
    - Use the `filter_stations` function to identify fuel stations near the route.
    - For each step in the route:
     - Find the closest fuel station using the `distance_to` function.
     - Track potential stops and calculate the distance traveled from the last stop.
    - If the distance traveled exceeds the maximum range (500 miles):
     - Filter stops for those traveled at least 100 miles from the start.
     - Select the station with the lowest fuel price among the filtered stops.
     - Update `optimal_stops` with the station's details.
     - Calculate the fuel cost for the segment and update the total cost.
     - Reset the starting point to the current step and continue.
    - Return the calculated route, optimal stops, and total cost as a JSON response.



