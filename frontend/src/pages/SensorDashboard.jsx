import React, { useState, useEffect } from 'react';
import { useTranslation } from '../hooks/useTranslation';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';
import './SensorDashboard.css';

// Register ChartJS components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const SensorDashboard = () => {
    const { t } = useTranslation();
    const [esp8266Readings, setEsp8266Readings] = useState([]);
    const [arduinoReadings, setArduinoReadings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [lastUpdated, setLastUpdated] = useState(null);

    const fetchSensorData = async () => {
        try {
            setLoading(true);

            // Fetch ESP8266 Data
            const espResponse = await fetch('http://localhost:8000/api/sensor/dashboard?limit=20');
            if (espResponse.ok) {
                const espData = await espResponse.json();
                setEsp8266Readings(espData.readings.filter(r => r.device_id === 'ESP8266'));
            }

            // Fetch Arduino UNO Data
            const unoResponse = await fetch('http://localhost:8000/api/sensor/uno-dashboard?limit=20');
            if (unoResponse.ok) {
                const unoData = await unoResponse.json();
                setArduinoReadings(unoData.readings);
            }

            setLastUpdated(new Date());
            setError(null);
        } catch (err) {
            console.error('Error fetching sensor data:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleTriggerNext = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/sensor/trigger-next', {
                method: 'POST'
            });
            if (!response.ok) {
                throw new Error('Failed to trigger next reading');
            }
            alert('✅ Trigger command sent to ESP8266!');
        } catch (err) {
            alert('❌ Failed to trigger next reading');
        }
    };

    useEffect(() => {
        fetchSensorData();
        const intervalId = setInterval(fetchSensorData, 5000);
        return () => clearInterval(intervalId);
    }, []);

    // Helper to process chart data
    const getChartData = (readings, type) => {
        const reversedReadings = [...readings].reverse(); // Oldest to newest for chart
        const labels = reversedReadings.map(r => new Date(r.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));

        if (type === 'npk') {
            return {
                labels,
                datasets: [
                    {
                        label: t('sensor.nitrogen'),
                        data: reversedReadings.map(r => r.N),
                        borderColor: '#2ecc71',
                        backgroundColor: 'rgba(46, 204, 113, 0.2)',
                        tension: 0.4
                    },
                    {
                        label: t('sensor.phosphorus'),
                        data: reversedReadings.map(r => r.P),
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.2)',
                        tension: 0.4
                    },
                    {
                        label: t('sensor.potassium'),
                        data: reversedReadings.map(r => r.K),
                        borderColor: '#f1c40f',
                        backgroundColor: 'rgba(241, 196, 15, 0.2)',
                        tension: 0.4
                    }
                ]
            };
        } else {
            return {
                labels,
                datasets: [
                    {
                        label: t('prediction.temperature'),
                        data: reversedReadings.map(r => r.temperature),
                        borderColor: '#e67e22',
                        backgroundColor: 'rgba(230, 126, 34, 0.2)',
                        tension: 0.4
                    },
                    {
                        label: t('prediction.humidity'),
                        data: reversedReadings.map(r => r.humidity),
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.2)',
                        tension: 0.4
                    }
                ]
            };
        }
    };

    const chartOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: false,
            },
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    const DeviceSection = ({ title, readings, type, showTrigger }) => {
        const isNPK = type === 'npk';
        const latest = readings.length > 0 ? readings[0] : null;

        return (
            <div className="analytics-card">
                <div className="card-header">
                    <h2>{title}</h2>
                    {showTrigger && (
                        <button className="trigger-btn" onClick={handleTriggerNext}>
                            {t('sensor.triggerManual')}
                        </button>
                    )}
                </div>

                {latest && (
                    <div className="metrics-row">
                        {isNPK ? (
                            <>
                                <div className="metric-box n-metric">
                                    <span className="label">{t('sensor.nitrogen').split(' ')[0]}</span>
                                    <span className="value">{latest.N}</span>
                                    <span className="unit">{t('sensor.unit.mgkg')}</span>
                                </div>
                                <div className="metric-box p-metric">
                                    <span className="label">{t('sensor.phosphorus').split(' ')[0]}</span>
                                    <span className="value">{latest.P}</span>
                                    <span className="unit">{t('sensor.unit.mgkg')}</span>
                                </div>
                                <div className="metric-box k-metric">
                                    <span className="label">{t('sensor.potassium').split(' ')[0]}</span>
                                    <span className="value">{latest.K}</span>
                                    <span className="unit">{t('sensor.unit.mgkg')}</span>
                                </div>
                            </>
                        ) : (
                            <>
                                <div className="metric-box temp-metric">
                                    <span className="label">{t('prediction.temperature').split(' ')[0]}</span>
                                    <span className="value">{latest.temperature?.toFixed(1)}</span>
                                    <span className="unit">{t('sensor.unit.celsius')}</span>
                                </div>
                                <div className="metric-box hum-metric">
                                    <span className="label">{t('prediction.humidity').split(' ')[0]}</span>
                                    <span className="value">{latest.humidity?.toFixed(1)}</span>
                                    <span className="unit">{t('sensor.unit.percent')}</span>
                                </div>
                                <div className="metric-box moist-metric">
                                    <span className="label">{t('sensor.soilMoisture')}</span>
                                    <span className="value">{latest.moisture}</span>
                                    <span className="unit">{t('sensor.unit.percent')}</span>
                                </div>
                            </>
                        )}
                    </div>
                )}

                <div className="chart-container">
                    {readings.length > 0 ? (
                        <Line options={chartOptions} data={getChartData(readings, type)} />
                    ) : (
                        <div className="no-data">{t('sensor.waitingData')}</div>
                    )}
                </div>
            </div>
        );
    };

    return (
        <div className="sensor-dashboard-v2">
            <div className="dashboard-header">
                <h1>📊 {t('sensor.dashboard')} {t('sensor.analysis')}</h1>
                <div className="status-bar">
                    <span className={`status-indicator ${loading ? 'loading' : 'live'}`}>
                        {loading ? t('sensor.refreshing') : t('sensor.liveSystemActive')}
                    </span>
                    {lastUpdated && <span className="last-seen">{t('sensor.lastUpdated')}: {lastUpdated.toLocaleTimeString()}</span>}
                </div>
            </div>

            <div className="analytics-grid">
                <DeviceSection
                    title={t('sensor.espTitle')}
                    readings={esp8266Readings}
                    type="npk"
                    showTrigger={true}
                />

                <DeviceSection
                    title={t('sensor.unoTitle')}
                    readings={arduinoReadings}
                    type="env"
                    showTrigger={false}
                />
            </div>
        </div>
    );
};

export default SensorDashboard;
