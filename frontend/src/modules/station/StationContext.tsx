import React from 'react';

// Define the shape of the context's data using an interface.
// This interface outlines the structure and expected types of the context's value.
interface StationContextType {
    selectedStationGuid: string | null; // Holds the ID of the currently selected station, or null if no station is selected.
    setSelectedStationGuid: (id: string | null) => void; // Function to update the selected station ID. Accepts a string or null.
}

// Create a context with a default value.
// The default value matches the StationContextType interface, providing initial values
// for the context's data. This context will be used to manage and share the state of
// the selected station ID across components that need access to it.
const StationContext = React.createContext<StationContextType>({
    selectedStationGuid: null, // Initially, no station is selected.
    setSelectedStationGuid: () => {}, // Placeholder function; will be overridden by a state updater function.
});

export default StationContext;

// Usage of this context allows components within the same tree to share and update
// the state of which station is currently selected without prop drilling or lifting state up unnecessarily.
// Components can access the current selectedStationId to display detailed information,
// or call setSelectedStationId to update the selection based on user interactions.
