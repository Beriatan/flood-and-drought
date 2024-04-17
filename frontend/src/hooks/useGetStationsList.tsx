import axiosInstance from "./AxiosInstance";
import { StationPoint, StationsRecord} from "../modules/station/StationListTypes";
import {useQuery} from "react-query";

function transformStationsList(data: any): StationPoint {
    return {
        id: data.id,
        name: data.name,
        latLong: {
            string: data['lat-long']?.string,
            latitude: data['lat-long']?.latitude,
            longitude: data['lat-long']?.longitude
        }
    }
}

const fetchStationsList = async (): Promise<StationsRecord> => {
    const { data } = await axiosInstance.get('/api/v1/stations');
    const stationsRecord: StationsRecord = {};

    // Ensure data is an array of arrays. If data is already a flat array, remove .flat()
    const flatData = Array.isArray(data[0]) ? data.flat() : data;

    flatData.forEach((stationData: any) => {
        const transformedStation = transformStationsList(stationData);
        stationsRecord[transformedStation.id] = transformedStation;
    });

    return stationsRecord;
};



const useGetStationsList = () => {
    const { data: stationList, isLoading, error } = useQuery<StationsRecord>(
        'stations',
        () => fetchStationsList()
    )

    return { stationList, loading: isLoading, error}
}

export default useGetStationsList