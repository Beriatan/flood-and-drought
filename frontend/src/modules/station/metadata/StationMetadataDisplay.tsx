import React from "react";

export interface StationMetadataDisplayProps {
    metadataType: 'simplified' | 'complete' | 'description'
    stationId: number
}

const StationMetadataDisplay: React.FC<StationMetadataDisplayProps> = (props) => {


    return(
        <><div>
            Selected station basic metadata
        </div></>
    )
}

export default StationMetadataDisplay