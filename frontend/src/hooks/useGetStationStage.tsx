import axiosInstance from "./AxiosInstance";
import {useQuery} from "react-query";


export interface StationStage {
    typicalRangeHigh: number,
    typicalRangeLow: number
}

const fetchStationStageLevels = async (guid: string): Promise<StationStage> => {
    const { data  } = await axiosInstance.get( `/api/v1/stations/${guid}/stage`)
    return data
}

const useGetStationStage = (guid:string) => {
    const { data: stationStage, isLoading, error } = useQuery<StationStage, Error>(
        ['stationStage', guid],
        () => fetchStationStageLevels(guid!),
        {
            enabled: !!guid
        }
    )

    return { stationStage, loading:isLoading, error}
}

export default useGetStationStage