from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Polygon:
    coordinates: List[List[Tuple[float, float]]] # List of coordinates in the polygon

@dataclass
class Geometry:
    type: str
    coordinates: Polygon

@dataclass
class FeatureProperties:
    rec_out_id: str
    rec_grp_id: str
    name: str
    start_date: str
    end_date: str
    flood_src: str
    flood_caus: str
    fm_status: str
    hfm_status: str
    data_src: str
    fluvial_f: str
    coastal_f: str
    tidal_f: str
    data_prov: str
    data_qual: str
    dgb_gemattr_data: str

@dataclass
class Feature:
    type: str
    id: str
    geometry: Geometry
    geometry_name: str
    properties: FeatureProperties
    bbox: List[float]

@dataclass
class FeatureCollection:
    type:str
    features: List[Feature]