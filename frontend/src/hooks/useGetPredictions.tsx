import axiosInstance from "./AxiosInstance";
import {useQuery} from "react-query";
import {StationPredictions} from "../modules/prediction/PredictionComponent";



const fetchPredictions = async (guid: string): Promise<StationPredictions> => {
    const { data } = await axiosInstance.post(`/api/v1/stations/${guid}/predictions`);
    return data;
};

const useGetPredictions = (guid: string) => {
    const { data: stationPredictions, isLoading, error } = useQuery<StationPredictions, Error>(
        ['stationPredictions', guid],
        () => fetchPredictions(guid),
        {
            enabled: !!guid, // Only run the query if guid is not null or undefined
            staleTime: Infinity, // Data will never be considered stale; automatic refetches won't be triggered
            cacheTime: 5 * 60 * 1000, // Cache the data for 5 minutes before garbage collection
            keepPreviousData: true // Keep showing the previous data while new data is being fetched
        }
    );

    return { stationPredictions, loading: isLoading, error };
};

export default useGetPredictions;