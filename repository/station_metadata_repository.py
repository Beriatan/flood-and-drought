import json
from typing import Optional
from flask import current_app

from util.data_utilities import transform_to_camel_case


class StationMetadataRepository:
    
    def __init__(self):
        self.s3_service = current_app.config['s3_service']

    def _load_data(self, file_path) -> Optional[dict]:
        """Load the station data from the JSON file"""
        return self.s3_service.load_json_from_s3(file_path)


    def get_station_metadata(self, station_id: int) -> Optional[dict]:
        file_path = f'nrfa_stations/{station_id}/detailed_metadata.json'
        try:
            data = self._load_data(file_path)
            return transform_to_camel_case(data)
        except FileNotFoundError:
            print(f"Station metadata not found for station ID {station_id}")
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {file_path}")
        except Exception as e:
            print(f"An error occurred while loading station metadata: {e}")

        return None

    def get_all_stations_list(self) -> Optional[dict]:
        file_path = 'nrfa_stations_metadata/all_stations_metadata.json'

        try:
            data = self._load_data(file_path)
            return transform_to_camel_case(data)
        except FileNotFoundError:
            print(f"Stations metadata not found in file: {file_path}")
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {file_path}")
        except Exception as e:
            print(f"An error occurred while loading station metadata: {e}")

        return None
