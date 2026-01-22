import React, { useEffect, useState } from 'react';
import { predictCrop, getAvailableModels } from '../services/api';
import { useTheme } from '../contexts/ThemeContext';
import { useTranslation } from '../hooks/useTranslation';
import PredictionForm from '../components/prediction/PredictionForm';
import PredictionResults from '../components/prediction/PredictionResults';
import SensorWidget from '../components/SensorWidget';
import './Prediction.css';

const defaultForm = {
    farmer_name: '',
    phone: '',
    location: '',
    land_size: 1,
    N: 50,
    P: 50,
    K: 50,
    temperature: 25,
    humidity: 60,
    ph: 6.5,
    rainfall: 120,
    soil_type: 'alluvial soil'
};

const Prediction = () => {
    const { theme } = useTheme();
    const { t } = useTranslation();
    const [form, setForm] = useState(defaultForm);
    const [models, setModels] = useState([]);
    const [modelDetails, setModelDetails] = useState({});
    const [selectedModel, setSelectedModel] = useState('');
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    // State for RL feedback modal
    const [showFeedbackModal, setShowFeedbackModal] = useState(false);
    const [feedbackForm, setFeedbackForm] = useState({
        actual_crop: '',
        success: true,
        notes: ''
    });
    const [feedbackLoading, setFeedbackLoading] = useState(false);
    const [feedbackSuccess, setFeedbackSuccess] = useState('');
    const [feedbackError, setFeedbackError] = useState('');

    useEffect(() => {
        (async () => {
            try {
                // Load Models
                const data = await getAvailableModels();
                setModels(data.available_models || []);
                setModelDetails(data.model_details || {});
                setSelectedModel(data.default || data.available_models?.[0] || '');

                // Fetch Sensor Data to Auto-fill
                try {
                    const [espRes, unoRes] = await Promise.all([
                        fetch('http://localhost:8000/api/sensor/dashboard'),
                        fetch('http://localhost:8000/api/sensor/uno-dashboard')
                    ]);

                    if (espRes.ok && unoRes.ok) {
                        const espData = await espRes.json();
                        const unoData = await unoRes.json();

                        const espReadings = espData.readings.filter(r => r.device_id === 'ESP8266');
                        const latestEsp = espReadings.length > 0 ? espReadings[0] : null;
                        const latestUno = unoData.readings.length > 0 ? unoData.readings[0] : null;

                        setForm(prev => ({
                            ...prev,
                            // Auto-fill available sensor data
                            N: latestEsp?.N ?? prev.N,
                            P: latestEsp?.P ?? prev.P,
                            K: latestEsp?.K ?? prev.K,
                            ph: 6.5, // Default or mock if sensor unavailable
                            temperature: latestUno?.temperature ? parseFloat(latestUno.temperature.toFixed(1)) : prev.temperature,
                            humidity: latestUno?.humidity ? parseFloat(latestUno.humidity.toFixed(1)) : prev.humidity,
                        }));
                    }
                } catch (sensorErr) {
                    console.error("Failed to auto-fetch sensor data:", sensorErr);
                }

            } catch (err) {
                setError('Unable to load model catalogue.');
            }
        })();
    }, []);

    const updateField = (evt) => {
        const { name, value, type } = evt.target;
        setForm((prev) => {
            if (type === 'number' || name === 'land_size' || ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'].includes(name)) {
                const numValue = value === '' ? '' : parseFloat(value);
                return {
                    ...prev,
                    [name]: isNaN(numValue) ? (value === '' ? '' : prev[name]) : numValue
                };
            }
            return {
                ...prev,
                [name]: value
            };
        });
    };

    const submitPrediction = async (evt) => {
        evt.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const payload = {
                ...form,
                model_name: 'Reinforcement Learning', // Force RL model as per requirement
                N: Number(form.N) || 0,
                P: Number(form.P) || 0,
                K: Number(form.K) || 0,
                temperature: Number(form.temperature) || 25,
                humidity: Number(form.humidity) || 60,
                ph: Number(form.ph) || 6.5,
                rainfall: Number(form.rainfall) || 120,
                land_size: Number(form.land_size) || 1
            };
            const data = await predictCrop(payload);
            if (data.error || data.detail) {
                throw new Error(data.error || data.detail);
            }
            setResult(data);
        } catch (err) {
            setError(err.message || 'Prediction failed. Please verify the inputs.');
        } finally {
            setLoading(false);
        }
    };

    const downloadPdf = async () => {
        if (!result?.pdf_url) return;
        try {
            const response = await fetch(result.pdf_url.startsWith('http') ? result.pdf_url : `http://localhost:8000${result.pdf_url}`);
            if (!response.ok) {
                throw new Error('Unable to download report.');
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `${form.farmer_name.replace(/\s+/g, '_')}_soil_report.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (err) {
            setError(err.message);
        }
    };

    const submitFeedback = async () => {
        if (!result || !feedbackForm.actual_crop) {
            setFeedbackError('Please enter the crop that was actually planted');
            return;
        }

        setFeedbackLoading(true);
        setFeedbackError('');
        setFeedbackSuccess('');

        try {
            const feedbackPayload = {
                N: Number(form.N),
                P: Number(form.P),
                K: Number(form.K),
                temperature: Number(form.temperature),
                humidity: Number(form.humidity),
                ph: Number(form.ph),
                rainfall: Number(form.rainfall),
                soil_type: form.soil_type,
                recommended_crop: result.predicted_crop,
                actual_crop: feedbackForm.actual_crop,
                success: feedbackForm.success
            };

            const response = await fetch('http://localhost:8000/rl-feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(feedbackPayload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to submit feedback');
            }

            const data = await response.json();
            setFeedbackSuccess(`✅ ${data.message}\n\nReward: ${data.reward}\nModel is learning from your feedback!`);

            setTimeout(() => {
                setShowFeedbackModal(false);
                setFeedbackForm({ actual_crop: '', success: true, notes: '' });
                setFeedbackSuccess('');
            }, 3000);

        } catch (err) {
            setFeedbackError(err.message || 'Failed to submit feedback. Please try again.');
        } finally {
            setFeedbackLoading(false);
        }
    };

    return (
        <div className="prediction-page">
            <SensorWidget />
            <div className="container">
                <div className="section-heading">
                    <h1>🌱 {t('prediction.title')}</h1>
                    <p className="section-subtitle">Turn soil diagnostics into ready-to-act crop plans.</p>
                </div>

                <div className="layout-grid">
                    <PredictionForm
                        form={form}
                        updateField={updateField}
                        setForm={setForm}
                        models={models}
                        modelDetails={modelDetails}
                        selectedModel={selectedModel}
                        setSelectedModel={setSelectedModel}
                        loading={loading}
                        onSubmit={submitPrediction}
                    />

                    <PredictionResults
                        result={result}
                        loading={loading}
                        error={error}
                        form={form}
                        theme={theme}
                        downloadPdf={downloadPdf}
                        setShowFeedbackModal={setShowFeedbackModal}
                    />
                </div>
            </div>

            {/* Feedback Modal */}
            {showFeedbackModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h3>Provide Feedback for RL Model</h3>
                        <p>Help improve the model by telling us what you actually planted and if it was successful.</p>

                        <div className="form-group">
                            <label>Actual Crop Planted:</label>
                            <input
                                type="text"
                                value={feedbackForm.actual_crop}
                                onChange={(e) => setFeedbackForm({ ...feedbackForm, actual_crop: e.target.value })}
                                placeholder="e.g. Rice, Wheat, Maize"
                            />
                        </div>

                        <div className="form-group">
                            <label>Was it successful?</label>
                            <div className="radio-group">
                                <label>
                                    <input
                                        type="radio"
                                        checked={feedbackForm.success}
                                        onChange={() => setFeedbackForm({ ...feedbackForm, success: true })}
                                    /> Yes
                                </label>
                                <label>
                                    <input
                                        type="radio"
                                        checked={!feedbackForm.success}
                                        onChange={() => setFeedbackForm({ ...feedbackForm, success: false })}
                                    /> No
                                </label>
                            </div>
                        </div>

                        {feedbackError && <div className="alert alert-error">{feedbackError}</div>}
                        {feedbackSuccess && <div className="alert alert-success" style={{ whiteSpace: 'pre-wrap' }}>{feedbackSuccess}</div>}

                        <div className="modal-actions">
                            <button onClick={() => setShowFeedbackModal(false)} className="btn-secondary">Cancel</button>
                            <button onClick={submitFeedback} className="btn-primary" disabled={feedbackLoading}>
                                {feedbackLoading ? 'Submitting...' : 'Submit Feedback'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Prediction;
