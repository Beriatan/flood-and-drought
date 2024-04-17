from dataclasses import dataclass, field
from typing import List, Dict, Union, Tuple


@dataclass
class FloodEventTimeSeries:
    station_id: int
    event_date: str
    pre_flood_data: Dict[str, Tuple[Union[float, None], str]] = field(default_factory=dict)
    flood_data: Dict[str, Tuple[Union[float, None], str]] = field(default_factory=dict)

    def add_pre_flood_data(self, date: str, data: Union[float, None]):
        self.pre_flood_data[date] = (data, 'pre-flood')

    def add_flood_data(self, date: str, data: Union[float, None]):
        self.flood_data[date] = (data, 'flood')

    def get_data(self) -> Dict[str, Tuple[Union[float, None], str]]:
        return {**self.pre_flood_data, **self.flood_data}

    def get_data_type(self, data_type: str) -> Dict[str, Tuple[Union[float, None], str]]:
        if data_type == 'pre-flood':
            return self.pre_flood_data
        elif data_type == 'flood':
            return self.flood_data
        else:
            raise ValueError(f'Invalid data type: {data_type}')

    def get_data_types(self) -> List[str]:
        return ['pre-flood', 'flood']

    def get_station_id(self) -> int:
        return self.station_id

    def get_event_date(self) -> str:
        return self.event_date

    def get_pre_flood_data(self) -> Dict[str, Tuple[Union[float, None], str]]:
        return self.pre_flood_data

    def get_flood_data(self) -> Dict[str, Tuple[Union[float, None], str]]:
        return self.flood_data


@dataclass
class FloodEventCollection:
    def __init__(self):
        self.events_by_station = {}

    def add_event(self, event: FloodEventTimeSeries):
        station_id = event.get_station_id()
        if station_id not in self.events_by_station:
            self.events_by_station[station_id] = []
        self.events_by_station[station_id].append(event)

    def get_events_by_station(self, station_id: int) -> List[FloodEventTimeSeries]:
        return self.events_by_station.get(station_id, [])
