from dataclasses import dataclass, field
from typing import List, Optional

from entity.nrfa_metadata import LatLong


@dataclass
class GridReference:
    ngr: Optional[str] = None
    easting: Optional[float] = None
    northing: Optional[float] = None


@dataclass
class DataType:
    data_type: Optional[str] = None
    parameter: Optional[str] = None
    units: Optional[str] = None
    period: Optional[str] = None
    first: Optional[str] = None
    last: Optional[str] = None


@dataclass
class DataSummary:
    data_types: List[DataType] = field(default_factory=list)


@dataclass
class StationMetadata:
    id: int
    name: str
    catchment_area: Optional[float] = None
    grid_reference: Optional[GridReference] = None
    lat_long: Optional[LatLong] = None
    river: Optional[str] = None
    location: Optional[str] = None
    station_level: Optional[float] = None
    easting: Optional[float] = None
    northing: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    measuring_authority_id: Optional[str] = None
    measuring_authority_station_id: Optional[str] = None
    hydrometric_area: Optional[int] = None
    opened: Optional[str] = None
    closed: Optional[str] = None
    station_type: Optional[str] = None
    bankfull_flow: Optional[float] = None
    structurefull_flow: Optional[float] = None
    sensitivity: Optional[float] = None
    nrfa_mean_flow: Optional[bool] = None
    nrfa_peak_flow: Optional[bool] = None
    feh_pooling: Optional[bool] = None
    feh_qmed: Optional[bool] = None
    feh_neither: Optional[bool] = None
    nhmp: Optional[bool] = None
    benchmark: Optional[bool] = None
    live_data: Optional[bool] = None
    eflag: Optional[bool] = None
    historic_droughts: Optional[bool] = None
    marius: Optional[bool] = None
    outlook_analogues: Optional[bool] = None
    outlook_esp: Optional[bool] = None
    factors_affecting_runoff: Optional[str] = None
    data_summary: Optional[DataSummary] = None
    licence_url: Optional[str] = None
    description_summary: Optional[str] = None
    description_general: Optional[str] = None
    description_station_hydrometry: Optional[str] = None
    description_flow_record: Optional[str] = None
    description_catchment: Optional[str] = None
    description_flow_regime: Optional[str] = None
    mean_flood_plain_depth: Optional[float] = None
    mean_flood_plain_location: Optional[float] = None
    mean_flood_plain_extent: Optional[float] = None


@dataclass
class StationsData:
    data: List[StationMetadata] = field(default_factory=list)
