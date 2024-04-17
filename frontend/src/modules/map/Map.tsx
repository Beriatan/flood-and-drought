import React, {useContext, useState} from 'react'
import {MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L, {Icon} from 'leaflet'
import { StationsRecord } from "modules/station/StationListTypes"
import locationDot from 'assets/iconmonstr-location-pin-thin.svg'
import MarkerClusterGroup from "react-leaflet-cluster";
import StationContext from "../station/StationContext";
const position: L.LatLngExpression = [51.505, -0.09];


const markerIcon = new Icon({
    iconUrl: locationDot,
    className: 'custom-marker-icon',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30]
});

export interface MapComponentProps {
    stationsList: StationsRecord
}

const Map: React.FC<MapComponentProps> = ({ stationsList }) => {
    const { setSelectedStationId } = useContext(StationContext)
    return (
            <MapContainer center={position} zoom={13} style={{ height: '75vh' }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            <MarkerClusterGroup>
            {Object.entries(stationsList).map(([stationId, station]) => (
                <Marker
                    icon={markerIcon}
                    key={stationId}
                    position={[station.latLong.latitude, station.latLong.longitude]}
                    eventHandlers={{
                        click: () => {
                            setSelectedStationId(parseInt(stationId))
                        }
                    }}
                >
                        <Popup>{station.name}</Popup>
                </Marker>
            ))
            }
            </MarkerClusterGroup>
        </MapContainer>
    )
}

export default Map;