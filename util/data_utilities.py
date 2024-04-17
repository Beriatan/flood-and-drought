import os
import json


def sort_flood_event_dates(base_folder='data//nrfa_stations'):
    for station_id in os.listdir(base_folder):
        station_folder = os.path.join(base_folder, station_id)
        flood_events_file = os.path.join(station_folder, 'flood_events.json')
        if os.path.exists(flood_events_file):
            with open(flood_events_file, 'r') as file:
                flood_dates = json.load(file)
            flood_dates_sorted = sorted(flood_dates)
            with open(flood_events_file, 'w') as file:
                json.dump(flood_dates_sorted, file, indent=4)
            print(f"Sorted flood event dates for station {station_id}")


def compile_stations_with_flood_events(base_folder='data/nrfa_stations',
                                       output_file='data/stations_with_flood_events.json'):
    stations_with_flood_events = []
    for station_id in os.listdir(base_folder):
        station_folder = os.path.join(base_folder, station_id)
        flood_events_file = os.path.join(station_folder, 'flood_events.json')
        if os.path.exists(flood_events_file):
            stations_with_flood_events.append(station_id)

    with open(output_file, 'w') as file:
        json.dump(stations_with_flood_events, file, indent=4)
    print(f"Compiled list of stations with flood events to {output_file}")


def transform_to_camel_case(data):
    """Transform dictionary keys from snake_case to camelCase."""

    def camel_case(s):
        parts = s.split('_')
        return parts[0] + ''.join(p.capitalize() or '_' for p in parts[1:])

    if isinstance(data, dict):
        return {camel_case(k): transform_to_camel_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [transform_to_camel_case(v) for v in data]
    else:
        return data