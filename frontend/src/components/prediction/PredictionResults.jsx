import React, { useState } from 'react';
import { formatPercentage, formatSoilHealthScore } from '../../utils/format';
import { NpkChart, SoilHealthChart } from './PredictionCharts';

const PredictionResults = ({
    result,
    loading,
    error,
    form,
    theme,
    downloadPdf,
    setShowFeedbackModal
}) => {
    const [expandedChart, setExpandedChart] = useState(null);
    const [marketData, setMarketData] = useState(null);
    const [marketLoading, setMarketLoading] = useState(false);

    // Fetch market prices when result changes
    React.useEffect(() => {
        if (result?.predicted_crop) {
            const fetchPrices = async () => {
                setMarketLoading(true);
                try {
                    // Use the district from the form or default to Karnataka
                    const district = form.location ? form.location.split(',')[0] : 'Karnataka';
                    const response = await fetch(`http://localhost:8000/market-prices?crop=${result.predicted_crop}&district=${district}`);
                    const data = await response.json();
                    if (data.status === 'success') {
                        setMarketData(data);
                    }
                } catch (err) {
                    console.error("Failed to fetch market prices:", err);
                } finally {
                    setMarketLoading(false);
                }
            };
            fetchPrices();
        }
    }, [result, form.location]);

    const downloadButtonStyle = {
        padding: '12px 24px',
        fontSize: '1rem',
        fontWeight: '600',
        background: 'linear-gradient(135deg, #2d8a48, #1b5e32)',
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer',
        boxShadow: '0 4px 12px rgba(45, 138, 72, 0.3)',
        transition: 'all 0.2s ease'
    };

    const renderWarnings = () => {
        if (!result?.warnings || result.warnings.length === 0) return null;
        return (
            <div className="warning-stack">
                {result.warnings.map((warning) => (
                    <div key={warning} className="alert alert-warning">
                        {warning}
                    </div>
                ))}
            </div>
        );
    };

    const renderExpandedChart = () => {
        if (!expandedChart) return null;

        return (
            <div className="modal-overlay" onClick={() => setExpandedChart(null)} style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundColor: 'rgba(0, 0, 0, 0.7)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                zIndex: 1000
            }}>
                <div className="modal-content" style={{
                    width: '90%',
                    maxWidth: '900px',
                    padding: '2rem',
                    backgroundColor: theme === 'dark' ? '#1a1a1a' : '#fff',
                    borderRadius: '12px',
                    position: 'relative'
                }} onClick={e => e.stopPropagation()}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h2 style={{ margin: 0, color: theme === 'dark' ? '#fff' : '#333' }}>Detailed Chart View</h2>
                        <button
                            onClick={() => setExpandedChart(null)}
                            style={{
                                background: 'none',
                                border: 'none',
                                fontSize: '2rem',
                                cursor: 'pointer',
                                color: theme === 'dark' ? '#fff' : '#333'
                            }}
                        >
                            ×
                        </button>
                    </div>
                    <div style={{ height: '500px' }}>
                        {expandedChart === 'npk' && <NpkChart form={form} theme={theme} height="100%" />}
                        {expandedChart === 'soil' && <SoilHealthChart result={result} theme={theme} height="100%" />}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <section className="results-panel">
            {renderExpandedChart()}

            {error && (
                <div className="alert alert-error" role="alert">
                    <span>⚠️</span>
                    <span>{error}</span>
                </div>
            )}

            {loading && (
                <div className="loading">
                    <div className="spinner" />
                    <p>Analysing soil patterns…</p>
                </div>
            )}

            {result && !loading && (
                <div className="card result-card">
                    {/* Download Button at Top */}
                    <div className="report-actions" style={{ marginBottom: '1.5rem', textAlign: 'right', display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                        <button type="button" onClick={downloadPdf} style={downloadButtonStyle}>
                            📄 Download Advisory PDF
                        </button>
                        {result.model_used === "Reinforcement Learning" && (
                            <button
                                type="button"
                                onClick={() => setShowFeedbackModal(true)}
                                style={{
                                    ...downloadButtonStyle,
                                    background: 'linear-gradient(135deg, #ff9800, #f57c00)',
                                    boxShadow: '0 4px 12px rgba(255, 152, 0, 0.3)'
                                }}
                            >
                                🔄 Provide Feedback
                            </button>
                        )}
                        <button
                            type="button"
                            onClick={() => window.location.href = `/farm-visualizer?crop=${encodeURIComponent(result.predicted_crop)}&land_size=${form.land_size}`}
                            style={downloadButtonStyle}
                        >
                            🌾 View Mixed Cropping Farm Layout
                        </button>
                    </div>

                    {/* Horizontal Layout Container */}
                    <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
                        {/* Left Column: Main Prediction & Soil Health */}
                        <div style={{ flex: '1 1 45%', minWidth: '300px' }}>
                            <header className="result-head">
                                <div>
                                    <span className="badge">Recommended crop</span>
                                    <h2>{result.predicted_crop}</h2>
                                    <p>Model: {form.model_name || result.model_used}</p>
                                </div>
                            </header>

                            {renderWarnings()}

                            {/* Regional Analysis */}
                            {result.regional_analysis && (
                                <div className="regional-analysis" style={{
                                    marginTop: '1.5rem',
                                    padding: '1rem',
                                    borderRadius: '8px',
                                    background: result.regional_analysis.is_regionally_suitable
                                        ? 'rgba(76, 175, 80, 0.1)'
                                        : 'rgba(255, 152, 0, 0.1)',
                                    border: `1px solid ${result.regional_analysis.is_regionally_suitable ? '#4CAF50' : '#FF9800'}`
                                }}>
                                    <h3 style={{ marginTop: 0, fontSize: '1.1rem', color: result.regional_analysis.is_regionally_suitable ? '#2E7D32' : '#E65100' }}>
                                        {result.regional_analysis.is_regionally_suitable ? '✅' : '⚠️'} Regional Suitability
                                    </h3>
                                    <div style={{ marginTop: '0.75rem', fontSize: '0.9rem' }}>
                                        <p style={{ margin: '0.3rem 0' }}><strong>Region:</strong> {result.regional_analysis.region}</p>
                                        <p style={{ margin: '0.3rem 0' }}><strong>Climate:</strong> {result.regional_analysis.climate}</p>
                                        <p style={{ margin: '0.3rem 0' }}><strong>Rainfall:</strong> {result.regional_analysis.rainfall_range[0]}-{result.regional_analysis.rainfall_range[1]} mm/year</p>
                                        {result.regional_analysis.recommendations && result.regional_analysis.recommendations.length > 0 && (
                                            <div style={{ marginTop: '0.75rem' }}>
                                                {result.regional_analysis.recommendations.slice(0, 2).map((rec, idx) => (
                                                    <div key={idx} style={{
                                                        padding: '0.5rem',
                                                        marginTop: '0.5rem',
                                                        borderRadius: '4px',
                                                        fontSize: '0.85rem',
                                                        background: rec.type === 'warning' ? 'rgba(244, 67, 54, 0.1)' :
                                                            rec.type === 'success' ? 'rgba(76, 175, 80, 0.1)' :
                                                                'rgba(33, 150, 243, 0.1)'
                                                    }}>
                                                        <p style={{ margin: 0 }}>{rec.message}</p>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}

                            {/* Soil Health */}
                            {result.soil_health && (
                                <div className="soil-health" style={{ marginTop: '1.5rem' }}>
                                    <h3>Soil health snapshot</h3>
                                    <div className="health-grid">
                                        <div className="health-card">
                                            <span className="label">Overall score</span>
                                            <strong>{result.soil_health.overall_score.toFixed(1)} / 100</strong>
                                            <span className={`status status-${formatSoilHealthScore(result.soil_health.overall_score).label.toLowerCase()}`}>
                                                {formatSoilHealthScore(result.soil_health.overall_score).label}
                                            </span>
                                        </div>
                                        <div className="health-card">
                                            <span className="label">Category</span>
                                            <strong>{result.soil_health.category}</strong>
                                            <span className="status">{result.soil_health.color}</span>
                                        </div>
                                    </div>
                                    {result.soil_health.recommendations?.length ? (
                                        <ul className="health-tips" style={{ fontSize: '0.9rem' }}>
                                            {result.soil_health.recommendations.slice(0, 3).map((tip) => (
                                                <li key={tip}>{tip}</li>
                                            ))}
                                        </ul>
                                    ) : null}
                                </div>
                            )}
                        </div>

                        {/* Right Column: Charts & Analysis */}
                        <div style={{ flex: '1 1 45%', minWidth: '300px' }}>
                            <NpkChart form={form} theme={theme} onClick={() => setExpandedChart('npk')} />
                            <SoilHealthChart result={result} theme={theme} onClick={() => setExpandedChart('soil')} />
                        </div>
                    </div>

                    {/* Full Width Sections Below */}
                    <div style={{ marginTop: '1.5rem' }}>
                        {/* Market Price Information - NEW SECTION */}
                        <div className="market-info" style={{ marginBottom: '1.5rem' }}>
                            <h3>📈 Market Price Trends (Agmarknet)</h3>
                            {marketLoading ? (
                                <p>Fetching latest market rates...</p>
                            ) : marketData && marketData.data ? (
                                <div className="market-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '1rem' }}>
                                    {marketData.data.slice(0, 3).map((mandi, idx) => (
                                        <div key={idx} className="market-card" style={{
                                            padding: '1rem',
                                            borderRadius: '8px',
                                            background: theme === 'dark' ? 'rgba(255, 255, 255, 0.05)' : '#f5f5f5',
                                            border: '1px solid #ddd'
                                        }}>
                                            <span className="label" style={{ display: 'block', fontSize: '0.85rem', color: '#666', marginBottom: '0.5rem' }}>{mandi.mandi}</span>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                                                <strong style={{ fontSize: '1.2rem', color: '#2d8a48' }}>₹{mandi.modal}</strong>
                                                <span style={{ fontSize: '0.8rem' }}>/ Quintal</span>
                                            </div>
                                            <div style={{ fontSize: '0.8rem', marginTop: '0.5rem', color: '#888' }}>
                                                Range: ₹{mandi.min} - ₹{mandi.max}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p>No market data available for this crop currently.</p>
                            )}
                            {marketData && (
                                <p style={{ fontSize: '0.8rem', color: '#888', marginTop: '0.5rem', textAlign: 'right' }}>
                                    Source: {marketData.source}
                                </p>
                            )}
                        </div>

                        {/* NPK Comparison Metrics */}
                        <div className="npk-comparison" style={{ marginBottom: '1.5rem' }}>
                            <h3>Current vs Ideal NPK</h3>
                            <div className="metrics-grid">
                                <div className="metric-card">
                                    <div className="metric-label">Nitrogen (N)</div>
                                    <div className="metric-value">{form.N} mg/kg</div>
                                    <div className="metric-note">Ideal Range: 50-100</div>
                                </div>
                                <div className="metric-card">
                                    <div className="metric-label">Phosphorus (P)</div>
                                    <div className="metric-value">{form.P} mg/kg</div>
                                    <div className="metric-note">Ideal Range: 30-60</div>
                                </div>
                                <div className="metric-card">
                                    <div className="metric-label">Potassium (K)</div>
                                    <div className="metric-value">{form.K} mg/kg</div>
                                    <div className="metric-note">Ideal Range: 30-80</div>
                                </div>
                            </div>
                        </div>

                        {/* Soil Treatment Recommendations */}
                        {result.soil_treatment && result.soil_treatment.length > 0 && (
                            <div className="soil-treatment" style={{ marginBottom: '1.5rem' }}>
                                <h3>🧪 Soil Treatment Recommendations</h3>
                                <ul className="treatment-list">
                                    {result.soil_treatment.map((treatment, index) => (
                                        <li key={index} className="treatment-item">
                                            {treatment.startsWith('✅') ? (
                                                <span className="success">{treatment}</span>
                                            ) : treatment.startsWith('⚠️') ? (
                                                <span className="warning">{treatment}</span>
                                            ) : (
                                                <span>{treatment}</span>
                                            )}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Fertilizer Recommendations */}
                        {result.fertilizer_estimate && (
                            <div className="fertilizer-card">
                                <h3>📦 Fertilizer Recommendations</h3>
                                <pre>{result.fertilizer_estimate}</pre>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </section>
    );
};

export default PredictionResults;
