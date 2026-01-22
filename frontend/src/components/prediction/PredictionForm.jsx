import React, { useState } from 'react';
import { autoDetectLocation, getHistoricalWeatherFree } from '../../services/api';
import { searchLocation, selectBestResult, geocodeWithFallback } from '../../utils/location';
import { villages, districts, villagesByDistrict } from '../../data/villages';
import ClimatePopup from './ClimatePopup';
import { useTranslation } from '../../hooks/useTranslation';

const PredictionForm = ({
    form,
    updateField,
    setForm,
    models,
    modelDetails,
    selectedModel,
    setSelectedModel,
    loading,
    onSubmit
}) => {
    const { t } = useTranslation();
    const [showClimatePopup, setShowClimatePopup] = useState(false);
    const [climateLoading, setClimateLoading] = useState(false);
    const [climateError, setClimateError] = useState('');
    const [error, setError] = useState('');

    // State for village selector
    const [selectedDistrict, setSelectedDistrict] = useState('');
    const [selectedVillage, setSelectedVillage] = useState('');
    const [pincode, setPincode] = useState('');
    const [pincodeLoading, setPincodeLoading] = useState(false);

    const renderModelInfo = () => {
        if (!selectedModel || !modelDetails[selectedModel]) return null;
        const info = modelDetails[selectedModel];
        return (
            <div className="model-info">
                <span className="model-type">{info.type}</span>
                <p>{info.description}</p>
            </div>
        );
    };

    const handlePincodeSearch = async () => {
        if (!pincode || pincode.length < 6) {
            setError('Please enter a valid 6-digit pincode');
            return;
        }

        setPincodeLoading(true);
        setError('');

        try {
            const result = await geocodeWithFallback(pincode);
            if (result) {
                console.log('Pincode result:', result);
                // Update location field with the result name
                setForm(prev => ({
                    ...prev,
                    location: result.name
                }));

                // Try to extract district from the result name if possible
                // Format is usually "Village (Pincode)" or "District State"
                // This is a best-effort to set the dropdowns, but primarily we set the location text
                const parts = result.name.split(' ');
                const potentialName = parts[0];

                // Check if it matches any district
                const matchedDistrict = districts.find(d =>
                    d.toLowerCase() === potentialName.toLowerCase() ||
                    result.name.toLowerCase().includes(d.toLowerCase())
                );

                if (matchedDistrict) {
                    setSelectedDistrict(matchedDistrict);
                }
            }
        } catch (err) {
            setError(err.message || 'Failed to find location details for this pincode');
        } finally {
            setPincodeLoading(false);
        }
    };

    const fetchClimateData = async (locationToUse) => {
        if (!locationToUse) {
            setClimateError('Please enter a location first');
            return;
        }

        setClimateLoading(true);
        setClimateError('');

        try {
            // Enhance location query with district if available and not already present
            let query = locationToUse;
            if (selectedDistrict && !query.toLowerCase().includes(selectedDistrict.toLowerCase())) {
                query = `${query}, ${selectedDistrict}`;
            }

            console.log('Fetching climate data for location:', query);

            // Use geocodeWithFallback to handle pin codes and complex strings
            let locationData = null;
            try {
                locationData = await geocodeWithFallback(query);
            } catch (e) {
                console.warn("Geocoding failed:", e);
            }

            if (!locationData) {
                throw new Error('Location not found. Please try a different location.');
            }

            // Fetch 2 years of historical weather data for better accuracy
            const endDate = new Date();
            endDate.setDate(endDate.getDate() - 1); // Yesterday
            const startDate = new Date();
            startDate.setFullYear(startDate.getFullYear() - 2); // 2 years ago

            const startStr = startDate.toISOString().split('T')[0];
            const endStr = endDate.toISOString().split('T')[0];

            const weatherData = await getHistoricalWeatherFree(
                locationData.lat,
                locationData.lon,
                null,
                startStr,
                endStr
            );

            if (weatherData.error) {
                throw new Error(weatherData.error);
            }

            // Calculate average temperature, humidity, and rainfall
            let totalTemp = 0;
            let totalHumidity = 0;
            let totalRainfall = 0;
            let count = 0;

            console.log('Weather data received:', weatherData);

            const dataArray = weatherData.data || weatherData.daily || (Array.isArray(weatherData) ? weatherData : []);

            if (dataArray && dataArray.length > 0) {
                dataArray.forEach((day) => {
                    const temp = day.temperature ?? day.temperature_2m_mean ?? day.temperature_2m ?? day.temp ?? day.temperature_max ?? day.temperature_min;
                    const humidity = day.humidity ?? day.relative_humidity_2m_mean ?? day.relative_humidity_2m ?? day.rh ?? 60;
                    const rainfall = day.rain ?? day.rain_sum ?? day.precipitation ?? day.precipitation_sum ?? day.rainfall ?? 0;

                    if (temp !== undefined && temp !== null && !isNaN(temp) && temp > -50 && temp < 60) {
                        totalTemp += temp;
                        count++;
                    }
                    if (humidity !== undefined && humidity !== null && !isNaN(humidity) && humidity >= 0 && humidity <= 100) {
                        totalHumidity += humidity;
                    }
                    if (rainfall !== undefined && rainfall !== null && !isNaN(rainfall) && rainfall >= 0) {
                        totalRainfall += rainfall;
                    }
                });

                const avgTemp = count > 0 ? totalTemp / count : 25;
                const avgHumidity = count > 0 ? totalHumidity / count : 60;
                const avgDailyRainfall = count > 0 ? totalRainfall / count : 0;
                let annualRainfall = avgDailyRainfall * 365;

                if (annualRainfall > 300) {
                    annualRainfall = annualRainfall / 2;
                }

                const updatedForm = {
                    temperature: Math.round(avgTemp * 10) / 10,
                    humidity: Math.round(avgHumidity * 10) / 10,
                    rainfall: Math.round(annualRainfall)
                };

                setForm(prev => ({
                    ...prev,
                    rainfall: Number(updatedForm.rainfall) || 0
                }));

                setTimeout(() => {
                    setShowClimatePopup(false);
                    setClimateError('');
                }, 500);
            } else {
                throw new Error('No weather data available for this location.');
            }
        } catch (err) {
            setClimateError(err.message || 'Failed to fetch climate data. Please try again.');
        } finally {
            setClimateLoading(false);
        }
    };

    return (
        <section className="card input-card">
            <form onSubmit={onSubmit} className="form-stack">
                <div className="form-group inline">
                    <label htmlFor="model">{t('prediction.modelEngine')}</label>
                    <input
                        id="model"
                        type="text"
                        value={t('about.stackingClassifier')}
                        disabled
                        style={{
                            background: '#f8f9fa',
                            color: '#2c3e50',
                            fontWeight: '600',
                            border: '1px solid #ced4da',
                            cursor: 'not-allowed'
                        }}
                    />
                </div>
                <div className="model-info">
                    <span className="model-type">{t('prediction.ensembleLearning')}</span>
                    <p>{t('prediction.modelDescription')}</p>
                </div>

                <div className="grid two-cols">
                    <div className="form-group">
                        <label htmlFor="farmer_name">{t('prediction.farmerName')}</label>
                        <input id="farmer_name" name="farmer_name" value={form.farmer_name} onChange={updateField} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="phone">{t('prediction.phone')}</label>
                        <input id="phone" name="phone" value={form.phone} onChange={updateField} required />
                    </div>
                </div>

                <div className="grid two-cols">
                    <div className="form-group">
                        <label htmlFor="location">
                            {t('prediction.villageDistrict')}
                            <div style={{ display: 'inline-flex', gap: '4px', marginLeft: '8px', flexWrap: 'wrap' }}>
                                <button
                                    type="button"
                                    onClick={async () => {
                                        if (!navigator.geolocation) {
                                            setError('Geolocation is not supported by your browser');
                                            return;
                                        }
                                        setError('');
                                        try {
                                            const position = await new Promise((resolve, reject) => {
                                                navigator.geolocation.getCurrentPosition(resolve, reject);
                                            });
                                            const { latitude, longitude } = position.coords;
                                            const locationData = await autoDetectLocation(latitude, longitude);
                                            if (locationData.success) {
                                                setForm(prev => ({ ...prev, location: locationData.location }));
                                            } else {
                                                setError('Could not detect location. Please enter manually.');
                                            }
                                        } catch (err) {
                                            setError('Location access denied or failed. Please enter location manually.');
                                        }
                                    }}
                                    style={{
                                        padding: '4px 12px',
                                        fontSize: '0.85rem',
                                        background: '#4CAF50',
                                        color: 'white',
                                        border: 'none',
                                        borderRadius: '4px',
                                        cursor: 'pointer'
                                    }}
                                    title="Use GPS to auto-detect your location"
                                >
                                    {t('prediction.useMyLocation')}
                                </button>
                            </div>
                        </label>

                        {error && <div style={{ color: 'red', fontSize: '0.8rem', marginBottom: '5px' }}>{error}</div>}

                        {/* Pin Code Input */}
                        <div style={{ display: 'flex', gap: '8px', marginBottom: '10px' }}>
                            <input
                                type="text"
                                placeholder={t('prediction.enterPinCode')}
                                value={pincode}
                                onChange={(e) => setPincode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                                style={{ flex: 1 }}
                            />
                            <button
                                type="button"
                                onClick={handlePincodeSearch}
                                disabled={pincodeLoading || pincode.length !== 6}
                                className="btn-secondary"
                                style={{ padding: '8px 12px', whiteSpace: 'nowrap' }}
                            >
                                {pincodeLoading ? t('prediction.searching') : t('prediction.find')}
                            </button>
                        </div>

                        {/* Village/City Selector Dropdown */}
                        <div style={{ marginBottom: '10px' }}>
                            <select
                                id="district-select"
                                value={selectedDistrict}
                                onChange={(e) => {
                                    setSelectedDistrict(e.target.value);
                                    setSelectedVillage(''); // Reset village when district changes
                                }}
                                style={{
                                    width: '100%',
                                    padding: '8px',
                                    marginBottom: '8px',
                                    borderRadius: '4px',
                                    border: '1px solid #ddd',
                                    fontSize: '0.9rem'
                                }}
                            >
                                <option value="">{t('prediction.selectDistrict')}</option>
                                {districts.map(district => (
                                    <option key={district} value={district}>{district}</option>
                                ))}
                            </select>

                            {selectedDistrict && (
                                <select
                                    id="village-select"
                                    value={selectedVillage}
                                    onChange={(e) => {
                                        const villageName = e.target.value;
                                        setSelectedVillage(villageName);
                                        if (villageName) {
                                            const village = villagesByDistrict[selectedDistrict]?.find(v => v.name === villageName);
                                            if (village) {
                                                setForm(prev => ({ ...prev, location: `${village.name}, ${village.district}` }));
                                            }
                                        }
                                    }}
                                    style={{
                                        width: '100%',
                                        padding: '8px',
                                        borderRadius: '4px',
                                        border: '1px solid #ddd',
                                        fontSize: '0.9rem'
                                    }}
                                >
                                    <option value="">{t('prediction.selectVillage')}</option>
                                    {villagesByDistrict[selectedDistrict]?.map(village => (
                                        <option key={village.name} value={village.name}>
                                            {village.name}
                                        </option>
                                    ))}
                                </select>
                            )}
                        </div>

                        <input
                            id="location"
                            name="location"
                            value={form.location}
                            onChange={updateField}
                            placeholder={t('prediction.manualLocation')}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="land_size">{t('prediction.landSize')}</label>
                        <input
                            id="land_size"
                            name="land_size"
                            type="number"
                            min="0.1"
                            step="0.1"
                            value={form.land_size}
                            onChange={updateField}
                            required
                        />
                    </div>
                </div>

                <div className="grid two-cols">
                    <div className="form-group">
                        <label htmlFor="N">{t('prediction.nitrogen')}</label>
                        <input
                            id="N"
                            name="N"
                            type="number"
                            min="0"
                            max="200"
                            step="1"
                            value={form.N}
                            onChange={updateField}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="P">{t('prediction.phosphorus')}</label>
                        <input
                            id="P"
                            name="P"
                            type="number"
                            min="0"
                            max="200"
                            step="1"
                            value={form.P}
                            onChange={updateField}
                            required
                        />
                    </div>
                </div>

                <div className="grid two-cols">
                    <div className="form-group">
                        <label htmlFor="K">{t('prediction.potassium')}</label>
                        <input
                            id="K"
                            name="K"
                            type="number"
                            min="0"
                            max="200"
                            step="1"
                            value={form.K}
                            onChange={updateField}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="ph">{t('prediction.soilPh')}</label>
                        <input
                            id="ph"
                            name="ph"
                            type="number"
                            min="3.5"
                            max="9.0"
                            step="0.1"
                            value={form.ph}
                            onChange={updateField}
                            required
                        />
                    </div>
                </div>

                <div className="grid two-cols">
                    <div className="form-group">
                        <label htmlFor="temperature">
                            {t('prediction.temperature')}
                        </label>
                        <input
                            id="temperature"
                            name="temperature"
                            type="number"
                            min="-10"
                            max="50"
                            step="0.1"
                            value={form.temperature}
                            onChange={updateField}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="humidity">{t('prediction.humidity')}</label>
                        <input
                            id="humidity"
                            name="humidity"
                            type="number"
                            min="0"
                            max="100"
                            step="0.1"
                            value={form.humidity}
                            onChange={updateField}
                            required
                        />
                    </div>
                </div>

                <div className="grid two-cols">
                    <div className="form-group">
                        <label htmlFor="rainfall">
                            {t('prediction.rainfall')}
                            <button
                                type="button"
                                className="btn-secondary btn-small"
                                onClick={() => setShowClimatePopup(true)}
                                style={{
                                    marginLeft: '8px',
                                    padding: '4px 12px',
                                    fontSize: '0.85rem'
                                }}
                                title="Fetch rainfall data automatically based on location"
                            >
                                {t('prediction.autoFetch')}
                            </button>
                        </label>
                        <input
                            type="number"
                            id="rainfall"
                            name="rainfall"
                            min="0"
                            step="1"
                            value={form.rainfall !== undefined && form.rainfall !== null ? form.rainfall : 120}
                            onChange={updateField}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="soil_type">{t('prediction.soilType')}</label>
                        <select id="soil_type" name="soil_type" value={form.soil_type} onChange={updateField} required>
                            <option value="alluvial soil">{t('prediction.soilType.alluvial')}</option>
                            <option value="black soil">{t('prediction.soilType.black')}</option>
                            <option value="red soil">{t('prediction.soilType.red')}</option>
                            <option value="laterite soil">{t('prediction.soilType.laterite')}</option>
                            <option value="sandy soil">{t('prediction.soilType.sandy')}</option>
                            <option value="peaty soil">{t('prediction.soilType.peaty')}</option>
                        </select>
                    </div>
                </div>

                <button type="submit" className="btn-primary" disabled={loading}>
                    {loading ? t('prediction.predicting') : t('prediction.generateAdvisory')}
                </button>

                <ClimatePopup
                    isOpen={showClimatePopup}
                    onClose={() => setShowClimatePopup(false)}
                    onFetch={fetchClimateData}
                    initialLocation={form.location}
                    loading={climateLoading}
                    error={climateError}
                />
            </form>
        </section>
    );
};

export default PredictionForm;
