import json
import string
from typing import Optional
from flask import current_app

from util.data_utilities import transform_to_camel_case


class StationMetadataRepository:

    def __init__(self):
        pass

    @property
    def s3_service(self):
        return current_app.config['s3_service']

    def _load_data(self, file_path) -> Optional[dict]:
        """Load the station data from the JSON file"""
        return self.s3_service.load_json_from_s3(file_path)

    def get_station_metadata(self, guid: string) -> Optional[dict]:
        file_path = f'flood_stations/{guid}/detailed_metadata.json'

        return self.retrieve_file(file_path)

    def get_station_stage(self, guid: string) -> Optional[dict]:
        file_path = f'flood_stations/{guid}/stage_scale.json'

        return self.retrieve_file(file_path)

    def get_all_stations_locations(self) -> Optional[dict]:
        file_path = 'flood_stations_metadata/stations_locations.json'

        return self.retrieve_file(file_path)

    def retrieve_file(self, file_path: string) -> Optional[dict]:
        try:
            data = self._load_data(file_path)
            return transform_to_camel_case(data)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {file_path}")
        except Exception as e:
            print(f"An error occurred while loading file: {e}")

        return None