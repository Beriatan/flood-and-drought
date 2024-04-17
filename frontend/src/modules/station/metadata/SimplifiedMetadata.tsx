import useGetStationMetadata from "../../../hooks/useGetStationMetadata";


export interface SimplifiedMetadataProps {
    stationId: number
}

const SimplifiedMetadata: React.FC<SimplifiedMetadataProps> = (props) => {
    const { stationMetadata, loading, error } = useGetStationMetadata(props.stationId)


    // return (
    //     <>
    //         <ul className={'list-group'}>
    //             <li className={'list-group-item'}>Station ID: props.me</li>
    //         </ul>
    //     </>
    // )
     if (loading) {
        return <p>Loading station metadata...</p>
     }

     if (error) {
        return <p>Error loading station metadata: {error.message}</p>
     }

     if (!stationMetadata) {
        return <p>No station metadata found.</p>
     }

     const [station] = stationMetadata.data

    return (
        <div>
            <h2>Station Metadata</h2>
            <ul className="list-group">
                <li className="list-group-item">Station ID: {station.id}</li>
                <li className="list-group-item">Name: {station.name}</li>
                {/* Add more <li> elements here for other metadata properties you want to display */}
            </ul>
        </div>
    )
}

export default SimplifiedMetadata