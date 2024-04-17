import { StationMetadata } from "../modules/station/StationTypes"
import axiosInstance from "./AxiosInstance"
import {useQuery} from "react-query";

const fetchStationMetadata = async (stationId: number): Promise<StationMetadata> => {
    const { data } = await axiosInstance.get(`/api/v1/stations/${stationId}/metadata`)
    return data
}

const useGetStationMetadata = (stationId: number ) => {
    const { data: stationMetadata, isLoading, error } = useQuery<StationMetadata, Error>(
        ['stationMetadata', stationId],
        () => fetchStationMetadata(stationId!),
    {
        enabled: !!stationId
        }
    )

    return { stationMetadata, loading:isLoading, error }
}

export default useGetStationMetadata