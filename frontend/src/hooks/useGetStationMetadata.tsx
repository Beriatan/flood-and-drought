import { StationMetadata } from "../modules/station/StationMetadataTypes"
import axiosInstance from "./AxiosInstance"
import {useQuery} from "react-query";

const fetchStationMetadata = async (guid: string): Promise<StationMetadata> => {
    const { data } = await axiosInstance.get(`/api/v1/stations/${guid}/metadata`)
    return data
}

const useGetStationMetadata = (guid: string ) => {
    const { data: stationMetadata, isLoading, error } = useQuery<StationMetadata, Error>(
        ['stationMetadata', guid],
        () => fetchStationMetadata(guid!),
    {
        enabled: !!guid
        }
    )

    return { stationMetadata, loading:isLoading, error }
}

export default useGetStationMetadata