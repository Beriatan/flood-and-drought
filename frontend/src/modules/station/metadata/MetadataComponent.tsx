import useGetStationMetadata from "../../../hooks/useGetStationMetadata";
import React from "react";


export interface SimplifiedMetadataProps {
    guid: string
}

const MetadataComponent: React.FC<SimplifiedMetadataProps> = (props) => {
    const { stationMetadata, loading, error } = useGetStationMetadata(props.guid)

     if (loading) {
        return <p>Loading station metadata...</p>
     }

     if (error) {
        return <p>Error loading station metadata: {error.message}</p>
     }

     if (!stationMetadata) {
        return <p>No station metadata found.</p>
     }

     const station = stationMetadata

    return (
        <div className="station-details">
            <h2>{station.label}</h2>
            <ul>
                <li>River: {station.riverName}</li>
                <li>Date Opened: {station.dateOpened}</li>
                <li>Environmental Agency Link: <a href={station.eaLink} target="_blank" rel="noopener noreferrer">View Details</a></li>
                <li>Latitude: {station.lat}</li>
                <li>Longitude: {station.long}</li>
                {station.town && <li>Town: {station.town}</li>}
                {station.catchmentName && <li>Catchment Name: {station.catchmentName}</li>}
            </ul>
        </div>
    )
}

export default MetadataComponent