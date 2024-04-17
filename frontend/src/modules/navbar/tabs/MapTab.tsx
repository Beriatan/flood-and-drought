import React, {useState} from "react";
import StationPrediction from "../../prediction/StationPrediction";
import SimplifiedMetadata from "../../station/metadata/SimplifiedMetadata";
import NrfaStationsList from "../../station/NrfaStations";
import MapComponent from "../../map/MapComponent";
import StationContext from "../../station/StationContext";


const MapTab: React.FC = () => {
    const [ selectedStationId, setSelectedStationId ] = useState<number | null>(null)

    const mockData = [
        { date: '2024-04-15', value: 0.512 },
        { date: '2024-04-16', value: 0.678 },
        { date: '2024-04-17', value: 0.346 },
        { date: '2024-04-18', value: 0.763 },
        { date: '2024-04-19', value: 0.497 },
        { date: '2024-04-20', value: 0.821 },
        { date: '2024-04-21', value: 0.364 }
    ];

    const mockData2 = [
        { date: '2024-04-15T16:00:00', value: 0.346 },
        { date: '2024-04-15T16:15:00', value: 0.382 },
        { date: '2024-04-15T16:30:00', value: 0.456 },
        { date: '2024-04-15T16:45:00', value: 0.528 },
        { date: '2024-04-15T17:00:00', value: 0.582 },
        { date: '2024-04-15T17:15:00', value: 0.562 },
        { date: '2024-04-15T17:30:00', value: 0.497 },
        { date: '2024-04-15T17:45:00', value: 0.423 },
        { date: '2024-04-15T18:00:00', value: 0.386 },
        { date: '2024-04-15T18:15:00', value: 0.346 },
        { date: '2024-04-15T18:30:00', value: 0.411 },
        { date: '2024-04-15T18:45:00', value: 0.482 },
        { date: '2024-04-15T19:00:00', value: 0.552 },
        { date: '2024-04-15T19:15:00', value: 0.581 },
        { date: '2024-04-15T19:30:00', value: 0.475 },
        { date: '2024-04-15T19:45:00', value: 0.397 },
        { date: '2024-04-15T20:00:00', value: 0.358 },
        { date: '2024-04-15T20:15:00', value: 0.425 },
        { date: '2024-04-15T20:30:00', value: 0.505 },
        { date: '2024-04-15T20:45:00', value: 0.582 },
        { date: '2024-04-15T21:00:00', value: 0.546 },
        { date: '2024-04-15T21:15:00', value: 0.478 },
        { date: '2024-04-15T21:30:00', value: 0.346 },
        { date: '2024-04-15T21:45:00', value: 0.421 }
    ];



    return(
        <StationContext.Provider value={{ selectedStationId , setSelectedStationId }}>
            <div className={'container-fluid h-75'}>
                <div className={'row full-height-row'}>
                    <div className={'col-6'}>
                        <MapComponent />
                    </div>
                    <div className={'row, col-6'}>
                        {selectedStationId && <SimplifiedMetadata stationId={selectedStationId}/>}
                        Predictions for the next 7 days
                        <StationPrediction data={mockData} />
                        {/*Prediction for the next 6 hours*/}
                        {/*<StationPrediction data={mockData2}/>*/}
                        <div className="alert alert-warning" role="alert">
                            Flood Alert: Predicted river levels are approaching within 10% of riverbank capacity. Please stay alert for updates and take necessary precautions.
                        </div>


                    </div>

                </div>
                <div className={'row'}>
                    <div className={'col-12'}>

                        <NrfaStationsList />
                    </div>

                </div>
            </div>
        </StationContext.Provider>
    )
}


export default MapTab