import React, {useState} from "react";
import PredictionComponent from "../../prediction/PredictionComponent";
import MetadataComponent from "../../station/metadata/MetadataComponent";
import MapComponent from "../../map/MapComponent";
import StationContext from "../../station/StationContext";
import StationsListComponent from "../../station/StationsListComponent";
import MemoizedPredictionComponent from "../../prediction/MemoizedPredictionComponent";


const MapTab: React.FC = () => {
    const [ selectedStationGuid, setSelectedStationGuid ] = useState<string | null>(null)
    const [ showWarnings, setShowWarnings ] = useState(false)

    const toggleWarnings = () => {
        setShowWarnings(!showWarnings)
    }


    return(
        <StationContext.Provider value={{ selectedStationGuid , setSelectedStationGuid }}>
            <div className={'container-fluid h-75'}>
                <div className={'row full-height-row'}>
                    <div className={'col-6'}>
                        <MapComponent />
                    </div>
                    <div className={'row, col-6'}>
                        {selectedStationGuid && <MetadataComponent guid={selectedStationGuid}/>}
                        {selectedStationGuid ?
                            <MemoizedPredictionComponent guid={selectedStationGuid}/>
                            : <h5>Select a measurement station to display details</h5>
                        }
                        <button className={'btn btn-warning mt-3'} onClick={toggleWarnings} >
                            { showWarnings ? 'Hide Warnings' : 'Show Warnings'}
                        </button>
                        { showWarnings && (
                            <div className={'pt-4'}>
                                <h5 className={'pt-4'}>Potential flood and drought warnings</h5>
                                    <ul className={'list-group'}>
                                        <li className={'list-inline-item'}>
                                            <div className="alert alert-warning" role="alert">
                                                Predicted River Levels within upper bounds - flood warning
                                            </div>
                                        </li>
                                        <li className={'list-inline-item'}>
                                            <div className="alert alert-danger" role="alert">
                                                Predicted River Levels above upper bounds - severe flood warning
                                            </div>
                                        </li>
                                        <li className={'list-inline-item'}>
                                            <div className="alert alert-warning" role="alert">
                                                Predicted River Levels within lower bounds - drought warning
                                            </div>
                                        </li>
                                        <li className={'list-inline-item'}>
                                            <div className="alert alert-danger" role="alert">
                                                Predicted River Levels above upper bounds - severe drought warning
                                            </div>
                                        </li>
                                    </ul>
                            </div>
                            )}

                    </div>

                </div>
                <div className={'row'}>
                    <div className={'col-12'}>

                        <StationsListComponent />
                    </div>

                </div>
            </div>
        </StationContext.Provider>
    )
}


export default MapTab