import React, { useState, useEffect, useRef } from 'react';
import './SensorWidget.css';

const SensorWidget = () => {
    const [esp8266Readings, setEsp8266Readings] = useState(null);
    const [arduinoReadings, setArduinoReadings] = useState(null);
    const [isOpen, setIsOpen] = useState(false);
    const [position, setPosition] = useState({ x: 20, y: 100 });
    const [isDragging, setIsDragging] = useState(false);
    const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
    const widgetRef = useRef(null);

    const fetchSensorData = async () => {
        try {
            // Fetch ESP8266 Data
            const espResponse = await fetch('http://localhost:8000/api/sensor/dashboard');
            if (espResponse.ok) {
                const espData = await espResponse.json();
                const espReadings = espData.readings.filter(r => r.device_id === 'ESP8266');
                if (espReadings.length > 0) {
                    setEsp8266Readings(espReadings[0]);
                }
            }

            // Fetch Arduino UNO Data
            const unoResponse = await fetch('http://localhost:8000/api/sensor/uno-dashboard');
            if (unoResponse.ok) {
                const unoData = await unoResponse.json();
                if (unoData.readings.length > 0) {
                    setArduinoReadings(unoData.readings[0]);
                }
            }
        } catch (err) {
            console.error('Error fetching sensor data for widget:', err);
        }
    };

    const handleTriggerNext = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/sensor/trigger-next', {
                method: 'POST'
            });
            if (!response.ok) throw new Error('Failed');
            alert('✅ Trigger sent!');
        } catch (err) {
            alert('❌ Failed to trigger');
        }
    };

    useEffect(() => {
        if (isOpen) {
            fetchSensorData();
            const interval = setInterval(fetchSensorData, 5000);
            return () => clearInterval(interval);
        }
    }, [isOpen]);

    const handleMouseDown = (e) => {
        if (e.target.closest('.widget-header')) {
            setIsDragging(true);
            setDragOffset({
                x: e.clientX - position.x,
                y: e.clientY - position.y
            });
        }
    };

    const handleMouseMove = (e) => {
        if (isDragging) {
            setPosition({
                x: e.clientX - dragOffset.x,
                y: e.clientY - dragOffset.y
            });
        }
    };

    const handleMouseUp = () => {
        setIsDragging(false);
    };

    useEffect(() => {
        if (isDragging) {
            window.addEventListener('mousemove', handleMouseMove);
            window.addEventListener('mouseup', handleMouseUp);
        } else {
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('mouseup', handleMouseUp);
        }
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('mouseup', handleMouseUp);
        };
    }, [isDragging]);

    if (!isOpen) {
        return (
            <button
                className="sensor-widget-toggle"
                onClick={() => setIsOpen(true)}
                style={{
                    position: 'fixed',
                    bottom: '20px',
                    right: '20px',
                    zIndex: 9999,
                    padding: '12px',
                    borderRadius: '50%',
                    backgroundColor: '#2ecc71',
                    color: 'white',
                    border: 'none',
                    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                    cursor: 'pointer',
                    fontSize: '24px'
                }}
            >
                📊 Acses Sensor data
            </button>
        );
    }

    return (
        <div
            ref={widgetRef}
            className="sensor-widget"
            style={{
                position: 'fixed',
                left: `${position.x}px`,
                top: `${position.y}px`,
                zIndex: 9999,
                backgroundColor: 'white',
                borderRadius: '10px',
                boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
                width: '300px',
                overflow: 'hidden'
            }}
            onMouseDown={handleMouseDown}
        >
            <div className="widget-header" style={{
                padding: '10px',
                backgroundColor: '#2c3e50',
                color: 'white',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                cursor: 'move'
            }}>
                <span style={{ fontWeight: 'bold' }}>Live Sensor Data</span>
                <button
                    onClick={() => setIsOpen(false)}
                    style={{
                        background: 'none',
                        border: 'none',
                        color: 'white',
                        cursor: 'pointer',
                        fontSize: '16px'
                    }}
                >
                    ✕
                </button>
            </div>

            <div className="widget-content" style={{ padding: '15px', maxHeight: '400px', overflowY: 'auto' }}>
                <div className="widget-section">
                    <h4 style={{ margin: '0 0 10px 0', color: '#27ae60' }}>ESP8266 (NodeMCU)</h4>
                    <div className="widget-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '5px', marginBottom: '15px' }}>
                        <div className="widget-metric">
                            <div className="label">N</div>
                            <div className="value">{esp8266Readings?.N || 0}</div>
                        </div>
                        <div className="widget-metric">
                            <div className="label">P</div>
                            <div className="value">{esp8266Readings?.P || 0}</div>
                        </div>
                        <div className="widget-metric">
                            <div className="label">K</div>
                            <div className="value">{esp8266Readings?.K || 0}</div>
                        </div>
                    </div>
                </div>

                <div className="widget-section">
                    <h4 style={{ margin: '0 0 10px 0', color: '#e67e22' }}>Arduino UNO R4</h4>
                    <div className="widget-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '5px', marginBottom: '15px' }}>
                        <div className="widget-metric">
                            <div className="label">Temp</div>
                            <div className="value">{arduinoReadings?.temperature?.toFixed(1) || 0}°C</div>
                        </div>
                        <div className="widget-metric">
                            <div className="label">Hum</div>
                            <div className="value">{arduinoReadings?.humidity?.toFixed(1) || 0}%</div>
                        </div>
                        <div className="widget-metric">
                            <div className="label">Moist</div>
                            <div className="value">{arduinoReadings?.moisture || 0}%</div>
                        </div>
                    </div>
                </div>

                <button
                    onClick={handleTriggerNext}
                    style={{
                        width: '100%',
                        padding: '8px',
                        backgroundColor: '#e74c3c',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        fontWeight: 'bold'
                    }}
                >
                    🎯 Trigger
                </button>
            </div>
        </div>
    );
};

export default SensorWidget;
