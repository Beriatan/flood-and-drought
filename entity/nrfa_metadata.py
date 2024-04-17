"""
NRFA Data Access Module

This module provides classes and utilities for interacting with the UK National River Flow Archive (NRFA) data.
The NRFA is a comprehensive source for river flow data across the UK, managing hydrometric data from various
gauging stations. This module facilitates access to NRFA's station metadata and time series data, primarily
through a set of data classes that model the structure of the data.

Key Components:
- LatLong: Data class for representing latitude and longitude information.
- StationMetadata: Data class for storing metadata about a specific NRFA station.
- StationMetadataList: Utility class for managing a collection of StationMetadata objects.

The NRFA API provides access to river flow gauging station information, including station metadata and
time series of daily river flows. This module is designed to interface with the API, enabling the extraction,
transformation, and storage of relevant data for analysis and processing purposes.

Usage of this module and data from the NRFA API is subject to the terms and conditions as outlined by the NRFA.

Acknowledgement: This module utilises data from the UK National River Flow Archive.
"""

from dataclasses import dataclass


@dataclass
class LatLong:
    string: str
    latitude: float
    longitude: float


@dataclass
class StationMetadataSimplified:
    id: int
    name: str
    lat_long: LatLong


class StationMetadataList:
    def __init__(self):
        self.stations = []

    def add_station(self, station):
        self.stations.append(station)

    def get_station(self, index):
        return self.stations[index]

    def get_station_count(self):
        return len(self.stations)

    def get_station_names(self):
        return [station.name for station in self.stations]

    def get_station_ids(self):
        return [station.id for station in self.stations]

    def get_station_latlongs(self):
        return [station.lat_long for station in self.stations]

    # Make the class iterable
    def __iter__(self):
        return iter(self.stations)

