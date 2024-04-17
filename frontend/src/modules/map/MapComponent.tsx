import useGetStationsList from "../../hooks/useGetStationsList";
import extractErrorMessage from "../error/ExtractErrorMessage";
import Map from "./Map";



const MapComponent: React.FC = () => {
    const { stationList, loading, error } = useGetStationsList()

    if (loading) return <p>Loading...</p>
    if (error) {
        const errorMessage = extractErrorMessage(error)
        return <p>Error: { errorMessage }</p>
    }
    return stationList ? <Map  stationsList={ stationList }/> : <p>No Stations found.</p>

}

export default MapComponent