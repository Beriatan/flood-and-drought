
export interface StationMetadata {
    data: Station[];
}

export interface Station {
    id: number;
    name: string;
    "catchment-area"?: number;
    "grid-reference"?: GridReference;
    river?: string;
    location?: string;
    "station-level"?: number;
    easting?: number;
    northing?: number;
    latitude?: number;
    longitude?: number;
    "measuring-authority-id"?: string;
    "measuring-authority-station-id"?: string;
    "hydrometric-area"?: number;
    opened?: string;
    closed?: string | null;
    "station-type"?: string;
    "bankfull-flow"?: number;
    "structurefull-flow"?: number | null;
    sensitivity?: number;
    "nrfa-mean-flow"?: boolean;
    "nrfa-peak-flow"?: boolean;
    "feh-pooling"?: boolean;
    "feh-qmed"?: boolean;
    "feh-neither"?: boolean;
    nhmp?: boolean;
    benchmark?: boolean;
    "live-data"?: boolean;
    eflag?: boolean;
    "historic-droughts"?: boolean;
    marius?: boolean;
    "outlook-analogues"?: boolean;
    "outlook-esp"?: boolean;
    "factors-affecting-runoff"?: string;
    "data-summary"?: DataSummary;
    "licence-url"?: string;
    "description-summary"?: string;
    // Make other description fields nullable as needed
}

export interface GridReference {
    ngr?: string;
    easting?: number;
    northing?: number;
}

export interface LatLong {
    string?: string;
    latitude: number;
    longitude: number;
}

export interface DataSummary {
    "data-types"?: DataType[];
}

export interface DataType {
    "data-type"?: string;
    parameter?: string;
    units?: string;
    period?: string;
    first?: string;
    last?: string;
}
