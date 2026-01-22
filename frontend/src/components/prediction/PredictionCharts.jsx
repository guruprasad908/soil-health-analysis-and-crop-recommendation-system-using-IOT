import React, { useMemo } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { formatSoilHealthScore } from '../../utils/format';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const useChartColors = (theme) => {
    return useMemo(() => {
        if (theme === 'dark') {
            return {
                background: 'rgba(18, 53, 36, 0.95)',
                grid: 'rgba(123, 216, 143, 0.2)',
                text: '#f4fff9',
                border: 'rgba(123, 216, 143, 0.3)',
                barColors: [
                    'rgba(123, 216, 143, 0.7)',
                    'rgba(255, 179, 71, 0.7)',
                    'rgba(63, 169, 107, 0.7)',
                ],
                barBorders: [
                    'rgba(123, 216, 143, 1)',
                    'rgba(255, 179, 71, 1)',
                    'rgba(63, 169, 107, 1)',
                ]
            };
        } else {
            return {
                background: 'rgba(255, 255, 255, 0.92)',
                grid: 'rgba(45, 138, 72, 0.2)',
                text: '#164025',
                border: 'rgba(45, 138, 72, 0.3)',
                barColors: [
                    'rgba(45, 138, 72, 0.7)',
                    'rgba(214, 143, 48, 0.7)',
                    'rgba(63, 169, 107, 0.7)',
                ],
                barBorders: [
                    'rgba(45, 138, 72, 1)',
                    'rgba(214, 143, 48, 1)',
                    'rgba(63, 169, 107, 1)',
                ]
            };
        }
    }, [theme]);
};

export const NpkChart = ({ form, theme, onClick, height = '250px' }) => {
    const colors = useChartColors(theme);

    const data = useMemo(() => ({
        labels: ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)'],
        datasets: [
            {
                label: 'Current Value (mg/kg)',
                data: [form.N, form.P, form.K],
                backgroundColor: colors.barColors,
                borderColor: colors.barBorders,
                borderWidth: 2,
            },
        ],
    }), [form.N, form.P, form.K, colors]);

    const options = useMemo(() => ({
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: { color: colors.text, font: { size: 14 } },
            },
            title: {
                display: true,
                text: 'Soil NPK Levels',
                color: colors.text,
                font: { size: 16, weight: 'bold' },
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 140,
                grid: { color: colors.grid },
                ticks: { color: colors.text, font: { size: 12 } },
            },
            x: {
                grid: { color: colors.grid },
                ticks: { color: colors.text, font: { size: 12 } },
            },
        },
        onClick: onClick ? (e) => onClick(e) : null,
    }), [colors, onClick]);

    return (
        <div
            className="chart-section"
            style={{ marginBottom: '1.5rem', cursor: onClick ? 'pointer' : 'default' }}
            onClick={onClick}
            title={onClick ? "Click to expand" : ""}
        >
            <h3 style={{ fontSize: '1.1rem' }}>📊 Soil NPK Levels</h3>
            <div className="chart-container" style={{ height }}>
                <Bar data={data} options={options} />
            </div>
        </div>
    );
};

export const SoilHealthChart = ({ result, theme, onClick, height = '250px' }) => {
    const colors = useChartColors(theme);
    const soilHealth = result?.soil_health;

    const data = useMemo(() => {
        if (!soilHealth?.breakdown) return null;
        const components = Object.keys(soilHealth.breakdown).map(k => k.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()));
        const scores = Object.values(soilHealth.breakdown);
        return {
            labels: components,
            datasets: [
                {
                    label: 'Score',
                    data: scores,
                    backgroundColor: colors.barColors,
                    borderColor: colors.barBorders,
                    borderWidth: 2,
                },
            ],
        };
    }, [soilHealth, colors]);

    const options = useMemo(() => ({
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: {
            legend: { display: false },
            title: {
                display: true,
                text: 'Soil Health Component Scores',
                color: colors.text,
                font: { size: 16, weight: 'bold' },
            },
        },
        scales: {
            x: {
                beginAtZero: true,
                max: 100,
                grid: { color: colors.grid },
                ticks: {
                    color: colors.text,
                    font: { size: 12 },
                    callback: (value) => value + ' pts'
                },
            },
            y: {
                grid: { color: colors.grid },
                ticks: { color: colors.text, font: { size: 12 } },
            },
        },
        onClick: onClick ? (e) => onClick(e) : null,
    }), [colors, onClick]);

    if (!data) return null;

    return (
        <div
            className="chart-section"
            style={{ marginBottom: '1.5rem', cursor: onClick ? 'pointer' : 'default' }}
            onClick={onClick}
            title={onClick ? "Click to expand" : ""}
        >
            <div className="chart-container" style={{ height }}>
                <Bar data={data} options={options} />
            </div>
        </div>
    );
};


