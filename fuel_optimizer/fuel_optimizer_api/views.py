from django.http import JsonResponse
from .models import FuelStation
from .utils import get_route, distance_to
import geopandas as gpd
from shapely.geometry import Point, LineString


def filter_stations(fuel_stations, route_coords):
    route_line = LineString(route_coords)
    gas_stations_gdf = gpd.GeoDataFrame(
        fuel_stations,
        geometry=[Point(s.longitude, s.latitude) for s in fuel_stations]
    )

    # 10 is buffer miles 
    buffer_zone = route_line.buffer(10 * 1609.34)  # Convert miles to meters for buffer

    # Filter gas stations within the buffer zone
    stations_in_buffer = gas_stations_gdf[gas_stations_gdf.geometry.within(buffer_zone)]
    return stations_in_buffer[0].values.tolist()


def optimize_route(request):
    start_lat = float(request.GET.get('start_lat'))
    start_lng = float(request.GET.get('start_lng'))
    finish_lat = float(request.GET.get('finish_lat'))
    finish_lng = float(request.GET.get('finish_lng'))

    # Query the database for all fuel stations
    fuel_stations = FuelStation.objects.all()

    total_cost = 0
    optimal_stops = []
    fuel_efficiency = 10  # miles per gallon
    stops = []
    start = (start_lng, start_lat)

    # Iterate over the route and calculate optimal stops
    route = get_route(start_lat, start_lng, finish_lat, finish_lng)
    route_coords = [[start_lng, start_lat]] + route['features'][0]['geometry']['coordinates'] + [[finish_lng, finish_lat]]
    filtered_stations = filter_stations(fuel_stations, route_coords)
    for step in route['features'][0]['geometry']['coordinates']:
        closest_station = min(filtered_stations, key=lambda station: distance_to((station.longitude, station.latitude), step))
        distance_travelled = distance_to(start, step)
        stops.append((distance_travelled, step, closest_station))

        if distance_travelled >= 500:  # 500 miles max range
            stops_ = [s for s in stops if s[0]>=100]
            dt, op_step, optimal_station = min(stops_, key=lambda station: station[2].retail_price)
            # Find the closest fuel station to the current step using database query
            optimal_stops.append({
                'name': optimal_station.name,
                'address': optimal_station.address,
                'city': optimal_station.city,
                'state': optimal_station.state,
                'price': optimal_station.retail_price
            })
            stops = stops[stops.index((dt, op_step, optimal_station)) + 1:]
            d_t = distance_to(start, op_step)
            total_cost += optimal_station.retail_price * (d_t / fuel_efficiency)
            start = op_step
        

    return JsonResponse({
        'route': route,
        'optimal_stops': optimal_stops,
        'total_cost': total_cost
    })
