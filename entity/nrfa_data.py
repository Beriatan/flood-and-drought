from dataclasses import dataclass
from typing import List, Dict, Union


@dataclass(frozen=True)
class NRFAStation:
    id: int
    name: str
    easting: float
    northing: float
    latitude: float
    longitude: float


@dataclass(frozen=True)
class NRFATimeSeriesDataType:
    id: str
    name: str
    parameter: str
    units: str
    measurement_type: str
    period: str


@dataclass(frozen=True)
class NRFAStationTimeSeriesData:
    timestamp: str
    interval: str
    station: NRFAStation
    data_type: NRFATimeSeriesDataType
    data_stream: List[Union[float, None]]


class NRFAData:
    def __init__(self):
        # Key: station ID, Value: Dict of lists of TimeSeriesData
        self.data = {}

    def add_data(self, station_id: int, data_type: str, time_series_data: NRFAStationTimeSeriesData):

        if station_id not in self.data:
            self.data[station_id] = {}

        if data_type not in self.data[station_id]:
            self.data[station_id] = []

        self.data[station_id][data_type] = time_series_data

    def get_data(self, station_id: int, data_type: str) -> NRFAStationTimeSeriesData:
        return self.data[station_id][data_type]

    def get_data_types(self, station_id: int) -> List[str]:
        return list(self.data[station_id].keys())

    def get_station_ids(self) -> List[int]:
        return list(self.data.keys())

    def get_station_data(self, station_id: int) -> Dict[str, NRFAStationTimeSeriesData]:
        return self.data[station_id]

    def get_station_data_type(self, station_id: int, data_type: str) -> NRFAStationTimeSeriesData:
        return self.data[station_id][data_type]

    def get_station_data_types(self, station_id: int) -> List[NRFATimeSeriesDataType]:
        return list(self.data[station_id].values())


