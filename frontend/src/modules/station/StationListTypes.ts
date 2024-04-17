import {LatLong} from "./StationTypes";


export type StationsRecord = Record<number, StationPoint>


export interface StationPoint {
    id: number,
    name: string,
    latLong: LatLong
}

