import requests


class HydrologyDataService:
    def __init__(self):
        self.base_url = "http://environment.data.gov.uk/hydrology/id/"
        # self.s3_service = s3_service

    def get_active_stations(self, observed_property):
        """Retrieve active monitoring stations for a specific observed property (e.g., waterFlow or waterLevel)."""
        endpoint = f"{self.base_url}stations"
        params = {
            'status.label': 'Active',
            'observedProperty': observed_property,
        }
        response = requests.get(endpoint, params=params)
        return response.json()

    def get_station_measures(self, station_id):
        """Retrieve available measures for a specific station."""
        endpoint = f"{self.base_url}stations/{station_id}/measures"
        response = requests.get(endpoint)
        return response.json()

    def get_measure_readings(self, measure_id, date_range):
        """Retrieve readings for a specific measure within a given date range."""
        endpoint = f"{self.base_url}measures/{measure_id}/readings"
        params = date_range  # Assumes date_range is a dict with keys 'min-date' and 'max-date'
        response = requests.get(endpoint, params=params)
        return response.json()
