from datetime import datetime, timedelta
import json
import os
from shapely.geometry import Point


class HistoricalDataService:
    def __init__(self, station_metadata_list, flood_event_data, stations_base_folder):
        self.station_metadata_list = station_metadata_list
        self.flood_event_data = flood_event_data
        self.stations_base_folder = stations_base_folder
        self.flood_event_sindex = self.flood_event_data.sindex

    def get_individual_flood_dates(self, start_date, end_date):
        """Generates individual dates between start and end date."""
        # Check if the dates are already datetime objects (e.g., Timestamp)
        if not isinstance(start_date, datetime):
            start = datetime.strptime(str(start_date), "%Y-%m-%dT%H:%M:%SZ")
        else:
            start = start_date

        if not isinstance(end_date, datetime):
            end = datetime.strptime(str(end_date), "%Y-%m-%dT%H:%M:%SZ")
        else:
            end = end_date

        date_generated = [start + timedelta(days=x) for x in range(0, (end - start).days + 1)]
        return [date.strftime("%Y-%m-%d") for date in date_generated]

    def get_flood_dates_for_station(self, station_point):
        flood_dates = []

        possible_matches_index = list(self.flood_event_sindex.query(station_point))
        possible_matches = self.flood_event_data.iloc[possible_matches_index]

        for index, event in possible_matches.iterrows():
            # Validate and fix geometries if necessary
            valid_geometry = event['geometry'] if event['geometry'].is_valid else event['geometry'].buffer(0)
            valid_station_point = station_point if station_point.is_valid else station_point.buffer(0)

            # Perform the within check using validated/modified geometries
            if valid_station_point.within(valid_geometry):
                start_date_str = event['start_date']
                end_date_str = event['end_date']
                individual_dates = self.get_individual_flood_dates(start_date_str, end_date_str)
                flood_dates.extend(individual_dates)
                print(
                    f"Found {len(individual_dates)} flood dates for station {station_point.wkt} in event {event['id']}")

        return list(set(flood_dates))  # Ensure uniqueness of dates

    def process_flood_events_for_stations(self):
        for station in self.station_metadata_list:
            station_point = Point(station.lat_long.longitude, station.lat_long.latitude)
            flood_dates = self.get_flood_dates_for_station(station_point)

            if flood_dates:
                print(f"Found {len(flood_dates)} flood dates for station {station.id}")
                self.write_flood_dates_to_file(station.id, flood_dates)

    def write_flood_dates_to_file(self, station_id, new_flood_dates):
        station_folder = os.path.join(self.stations_base_folder, str(station_id))  # Ensure station_id is a string
        os.makedirs(station_folder, exist_ok=True)

        flood_file_path = os.path.join('data', station_folder, 'flood_events.json')

        existing_flood_dates = []

        # Check if the file exists and read existing dates into a list
        if os.path.exists(flood_file_path):
            with open(flood_file_path, 'r') as file:
                existing_flood_dates = json.load(file)  # Load existing dates as a list

        # Combine new and existing dates, ensuring uniqueness
        updated_flood_dates = list(set(existing_flood_dates).union(set(new_flood_dates)))

        # Write the combined list of unique dates back to the file
        with open(flood_file_path, 'w') as file:
            json.dump(updated_flood_dates, file, indent=4)  # Use 'w' mode to overwrite and indent for readability
            print(f"Saved flood dates for station {station_id} to {flood_file_path}")
