import React, { useState, useEffect } from 'react';

const ClimatePopup = ({ isOpen, onClose, onFetch, initialLocation, loading, error }) => {
    const [location, setLocation] = useState(initialLocation || '');

    useEffect(() => {
        if (isOpen) {
            setLocation(initialLocation || '');
        }
    }, [isOpen, initialLocation]);

    if (!isOpen) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 9999
        }}>
            <div style={{
                backgroundColor: 'white',
                borderRadius: '8px',
                padding: '20px',
                maxWidth: '500px',
                width: '90%',
                maxHeight: '90vh',
                overflowY: 'auto',
                color: 'black'
            }}>
                <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '20px'
                }}>
                    <h3 style={{ margin: 0, color: 'black' }}>Auto-fetch Climate Data</h3>
                    <button
                        style={{
                            background: 'none',
                            border: 'none',
                            fontSize: '1.5rem',
                            cursor: 'pointer',
                            color: 'gray',
                            padding: 0,
                            width: '30px',
                            height: '30px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}
                        onClick={onClose}
                    >
                        ×
                    </button>
                </div>
                <div>
                    <p style={{ marginTop: 0, color: 'black' }}>Enter your location to automatically fetch climate data for the past year:</p>
                    <div>
                        <label htmlFor="popup-location" style={{ display: 'block', marginBottom: '0.45rem', fontWeight: 600, color: 'black' }}>
                            Location (Village / District):
                        </label>
                        <input
                            id="popup-location"
                            type="text"
                            value={location}
                            onChange={(e) => setLocation(e.target.value)}
                            placeholder="e.g., Babaleshwar, Bidar"
                            disabled={loading}
                            style={{
                                background: 'rgba(230, 244, 230, 0.92)',
                                border: '1px solid rgba(45, 138, 72, 0.2)',
                                borderRadius: '10px',
                                padding: '0.75rem 1rem',
                                fontFamily: 'inherit',
                                fontSize: '1rem',
                                color: 'black',
                                width: '100%'
                            }}
                        />
                    </div>
                    {error && (
                        <div style={{
                            padding: '1rem',
                            borderRadius: '10px',
                            marginBottom: '1rem',
                            fontWeight: 500,
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.65rem',
                            background: 'rgba(220, 53, 69, 0.15)',
                            border: '1px solid rgba(220, 53, 69, 0.4)',
                            color: '#ff7b7b'
                        }}>
                            <span>⚠️</span>
                            <span>{error}</span>
                        </div>
                    )}
                    <div style={{
                        display: 'flex',
                        justifyContent: 'flex-end',
                        gap: '0.8rem',
                        marginTop: '1.5rem'
                    }}>
                        <button
                            style={{
                                background: 'linear-gradient(135deg, #156C3F, #1E8B50)',
                                color: 'white',
                                border: 'none',
                                borderRadius: '10px',
                                padding: '0.75rem 1.6rem',
                                fontSize: '1rem',
                                fontWeight: 600,
                                cursor: 'pointer',
                                transition: 'transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease, opacity 0.15s ease',
                                boxShadow: '0 12px 20px -12px rgba(123, 216, 143, 0.6)'
                            }}
                            onClick={onClose}
                            disabled={loading}
                        >
                            Cancel
                        </button>
                        <button
                            style={{
                                background: 'linear-gradient(135deg, #2d8a48, #1b5e32)',
                                color: 'white',
                                border: 'none',
                                borderRadius: '10px',
                                padding: '0.75rem 1.6rem',
                                fontSize: '1rem',
                                fontWeight: 600,
                                cursor: 'pointer',
                                transition: 'transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease, opacity 0.15s ease',
                                boxShadow: '0 12px 20px -12px rgba(45, 138, 72, 0.4)'
                            }}
                            onClick={() => onFetch(location)}
                            disabled={loading || !location.trim()}
                        >
                            {loading ? 'Fetching...' : 'Fetch Climate Data'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ClimatePopup;
