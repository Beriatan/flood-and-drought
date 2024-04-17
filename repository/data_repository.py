import json
from entity.nrfa_metadata import StationMetadataSimplified, StationMetadataList, LatLong
import geopandas as gpd


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data


def save_station_metadata(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        print(f"Saved station metadata to {file_path}")


def save_station_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        print(f"Saved station data to {file_path}")


def load_flood_events(file_path):
    return gpd.read_file(file_path)


def load_station_metadata(file_path) -> StationMetadataList:
    stations_data = load_json_file(file_path)
    station_metadata_list = StationMetadataList()
    for station_group in stations_data:
        for station_data in station_group:
            station_id = station_data['id']
            station_name = station_data['name']
            lat_long_data = station_data['lat-long']
            lat_long = LatLong(
                lat_long_data['string'],
                latitude=lat_long_data['latitude'],
                longitude=lat_long_data['longitude']
            )

            station_metadata = StationMetadataSimplified(station_id, station_name, lat_long)
            station_metadata_list.add_station(station_metadata)

    return station_metadata_list
