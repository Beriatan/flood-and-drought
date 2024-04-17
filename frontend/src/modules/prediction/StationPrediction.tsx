import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// Define an interface for the data items
interface DataItem {
    date: string;
    value: number;
}

// Define props for the StationPrediction component
interface StationPredictionProps {
    data: DataItem[];
}

const StationPrediction: React.FC<StationPredictionProps> = ({ data }) => {
    const chartData = {
        labels: data.map(item => item.date),
        datasets: [
            {
                label: 'Predicted River Level',
                data: data.map(item => item.value),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            },
            {
                label: 'Riverbank Level',
                data: new Array(data.length).fill(0.840),
                borderColor: 'rgb(255, 99, 132)',
                borderDash: [5, 5],
                fill: false
            },
            {
                label: 'Pre-drought Level',
                data: new Array(data.length).fill(0.112),
                borderColor: 'rgb(255, 206, 86)',
                borderDash: [5, 5],
                fill: false
            }
        ]
    };

    const options = {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: true
            }
        }
    };

    return <Line data={chartData} options={options} />;
};

export default StationPrediction;
