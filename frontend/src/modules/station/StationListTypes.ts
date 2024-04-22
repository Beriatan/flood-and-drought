export type StationsRecord = Record<string, StationPoint>


export interface StationPoint {
    guid: string,
    label: string,
    lat: number,
    long: number,
    referenceId: string,
    riverName?: string,
    town?: string,
    catchmentName?: string
}

