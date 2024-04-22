import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js';
import useGetStationStage from "../../hooks/useGetStationStage";
import useGetPredictions from "../../hooks/useGetPredictions";

// Register necessary components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

// Define props for the StationPrediction component
interface StationPredictionProps {
    guid: string;
}

export interface PredictionData {
    date: string;
    value: number;
}
export interface StationPredictions {
    max_predictions: PredictionData[]
    min_predictions: PredictionData[]
    mean_predictions: PredictionData[]
}

const PredictionComponent: React.FC<StationPredictionProps> = ({ guid }) => {
    const { stationStage } = useGetStationStage(guid);
    const { stationPredictions, loading, error } = useGetPredictions(guid);

    if (loading ) {
        return <div className="d-flex justify-content-center">
            <div className="spinner-border text-success" role="status">
            </div><span className="sr-only">Generating predictions and loading the chart...</span>
        </div>;
    }

    if (error) {
        return <div>Error loading predictions: {error.message}</div>; // Error handling
    }

    const chartData = {
        labels: stationPredictions?.max_predictions.map(item => item.date),
        datasets: [
            {
                label: 'Maximum Predicted Level (lmax)',
                data: stationPredictions?.max_predictions.map(item => item.value),
                borderColor: 'rgba(255, 99, 132, 0.4)',
                borderWidth: 1,
                fill: '+1', // Fill to next dataset (index +1)
                tension: 0.4 // Smooth curves
            },
            {
                label: 'Minimum Predicted Level (lmin)',
                data: stationPredictions?.min_predictions.map(item => item.value),
                borderColor: 'rgba(75, 192, 192, 0.4)',
                borderWidth: 1,
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Semi-transparent fill color
                fill: false, // No filling below this dataset
                tension: 0.4 // Smooth curves
            },
            {
                label: 'Mean Predicted Level (lmin)',
                data: stationPredictions?.mean_predictions.map(item => item.value),
                borderColor: 'rgb(0, 0, 0)',
                borderWidth: 2,
                tension: 0.4 // Smooth curves
            },
            {
                label: 'Flood Risk Level',
                data: new Array(stationPredictions?.max_predictions.length).fill(stationStage?.typicalRangeHigh),
                borderColor: 'rgba(0, 0, 255, 0.8)',  // Blue color for visibility
                borderWidth: 1,
                borderDash: [10, 5],
                fill: false
            },
            {
                label: 'Drought Risk Level',
                data: new Array(stationPredictions?.max_predictions.length).fill(stationStage?.typicalRangeLow),
                borderColor: 'rgba(255, 165, 0, 0.8)',  // Orange color for visibility
                borderWidth: 1,
                borderDash: [10, 5],
                fill: false
            }
        ]
    };

    const options = {
        scales: {
            y: {
                beginAtZero: false,
            }
        },
        plugins: {
            legend: {
                display: true
            }
        },
        elements: {
            line: {
                tension: 0.4 // Smooth the line
            }
        }
    };

    return <Line data={chartData} options={options} />;
};

export default PredictionComponent;
