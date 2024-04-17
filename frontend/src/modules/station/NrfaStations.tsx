import React from "react"
import useGetStationsList from "../../hooks/useGetStationsList"
import extractErrorMessage from "../error/ExtractErrorMessage";


const NrfaStations: React.FC = () => {

    // // const { stationList, error, loading } = useGetStationsList()
    // if (loading) {
    //     return <p>Loading station list...</p>
    // }
    // if (error) {
    //     // Check if the error is an AxiosError to access detailed response data
    //     const errorMessage = extractErrorMessage(error)
    //     return <p>Error loading station list: { errorMessage }</p>;
    // }
    //
    // if (!stationList) {
    //     return <p>No station list found.</p>
    // }
    //
    return (
        <>
            {/*Here will be displayed list of visible stations up to 10*/}
        </>
    )
}

export default NrfaStations