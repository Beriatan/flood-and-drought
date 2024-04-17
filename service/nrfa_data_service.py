import os
import json
import urllib.request, urllib.error
from urllib.error import URLError, HTTPError
import concurrent.futures


class NRFADataService:
    def __init__(self, s3_service):
        self.base_url = os.getenv("NRFA_API_BASE_URL")
        self.s3_service = s3_service

    def fetch_station_ids(self):
        url = f"{self.base_url}/station-ids?format=json-object"
        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            return data.get("station-ids", [])
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} {e.reason}")
            return []

    def download_station_metadata(self, station_ids, data_folder, additional_fields=None):
        """
        Downloads metadata for a list of station IDs and saves it to a specified folder.
        The metadata fields to be downloaded are configurable, with some defaults always included.
        """
        # Define default fields to always fetch
        default_fields = 'id,name,lat-long,catchment-area,river,location,opened,closed,qmed,gdf-statistics'

        # If additional fields are provided, append them to the default fields
        if additional_fields:
            fields = f"{default_fields},{additional_fields}"
        else:
            fields = default_fields

        all_station_info = []
        for station_id in station_ids:
            metadata_url = f"{self.base_url}/station-info?station={station_id}&format=json-object&fields={fields}"
            try:
                response = urllib.request.urlopen(metadata_url)
                data = json.loads(response.read())
                all_station_info.append(data.get('data', []))
            except urllib.error.HTTPError as e:
                print(f"HTTP Error: {e.code} {e.reason}")

        # Construct the S3 key based on the given data folder
        json_file_path = f'{data_folder}/all_stations_metadata.json'
        # Save the fetched metadata to S3
        self.s3_service.save_json_to_s3(json_file_path, all_station_info)

        print(f"Metadata for {len(station_ids)} stations saved to {json_file_path}.")

    def download_station_data(self, station_id, base_folder="nrfa_stations", data_type='gdf'):

        time_series_url = f"{self.base_url}/time-series?station={station_id}&data-type={data_type}&format=json-object"

        try:
            response = urllib.request.urlopen(time_series_url)
            data = json.loads(response.read())

            station_folder = f"{base_folder}/{station_id}"

            data_file_path = f"{station_folder}/{data_type}.json"
            self.s3_service.save_json_to_s3(data_file_path, data)
        except urllib.error.HTTPError as e:
            print(f"HTTP Error for station {station_id}: {e.code}")

    def download_all_stations_data(self, data_folder=None, data_types=None, station_ids=None):
        """
        Downloads data for all stations from the NRFA API using multi-threading.
        Each station's data is saved as a separate file.
        """
        if data_types is None:
            data_types = ['gdf', 'ndf', 'pot-stage', 'pot-flow', 'amax-stage', 'amax-flow']

        if station_ids is None:
            station_ids = self.fetch_station_ids()

        if data_folder is None:
            data_folder = "nrfa_stations"

        print(f"Downloading data for {len(station_ids)} stations and {len(data_types)} data types."
              f" This may take a while...")

        # Helper function for downloading station data
        def download_for_station_and_type(station_id, data_type):
            try:
                print(f"Fetching {data_type} data for station {station_id}...")
                self.download_station_data(station_id, data_folder, data_type=data_type)
                print(f"Completed fetching {data_type} data for station {station_id}.")
            except Exception as e:
                print(f"Error fetching {data_type} data for station {station_id}: {e}")

        # Use ThreadPoolExecutor to download data in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a list of futures
            futures = []
            for station_id in station_ids:
                for data_type in data_types:
                    futures.append(executor.submit(download_for_station_and_type, station_id, data_type))

            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                future.result()  # This will re-raise any exception raised in the task

        print(f"All data downloads completed.")

    def download_all_stations_metadata(self, data_folder, fields=None):
        """
        Downloads metadata for all stations from the NRFA API.
        """

        if fields is None:
            fields = 'id,name,lat-long'
        station_ids = self.fetch_station_ids()
        print(f"Downloading metadata for {len(station_ids)} stations. This may take a while...")
        self.download_station_metadata(station_ids, data_folder, fields)
        print(f"Metadata download completed.")

    def fetch_and_save_detailed_station_metadata(self, station_id, base_folder="nrfa_stations"):
        """
        Fetches detailed station metadata for a given station ID and saves it to the station's folder.
        """
        # station_folder = os.path.join(base_folder, str(station_id))
        # os.makedirs(station_folder, exist_ok=True)

        station_folder = f"{base_folder}/{station_id}"

        # Define the fields parameter to fetch comprehensive metadata
        fields = "id,name,catchment-area,grid-reference,lat-long,river,location,station-level,easting,northing," \
                 "station-information,category,catchment-information,gdf-statistics,peak-flow-statistics,elevation," \
                 "catchment-rainfall,lcm2000,lcm2007,geology,feh-descriptors,urban-extent,spatial-location," \
                 "peak-flow-metadata,data-summary,description,all"

        metadata_url = f"{self.base_url}/station-info?station={station_id}&format=json-object&fields={fields}"

        try:
            print("Fetching detailed metadata...")
            response = urllib.request.urlopen(metadata_url)
            data = json.loads(response.read())
            print(f"Fetched detailed metadata for station {station_id}.")

            # Save the fetched metadata to a JSON file
            # metadata_file_path = os.path.join("data", station_folder, "detailed_metadata.json")
            metadata_file_path = f"{station_folder}/detailed_metadata.json"
            # with open(metadata_file_path, 'w') as file:
            #     json.dump(data, file, indent=4)
            self.s3_service.save_json_to_s3(metadata_file_path, data)
            print(f"Detailed metadata for station {station_id} saved to {metadata_file_path}")

        except HTTPError as e:
            print(f"HTTP Error: {e.code} {e.reason}")
        except URLError as e:
            print(f"URL Error: {e.reason}")
        except Exception as e:
            print(f"Error: {e}")

    def fetch_and_save_station_ids(self):
        """
        Fetches all station IDs from the NRFA API and saves them to a JSON file.
        """
        station_ids = self.fetch_station_ids()
        self.s3_service.save_json_to_s3("nrfa_stations_metadata/station_ids.json", station_ids)
