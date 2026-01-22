import React, { useState, useContext, useMemo } from 'react';
import { getFertilizerRecommendation } from '../services/api';
import { useTheme } from '../contexts/ThemeContext';
import { useTranslation } from '../hooks/useTranslation';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';
import './FertilizerRecommendation.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

const defaultForm = {
  temperature: 25,
  humidity: 60,
  moisture: 40,
  soil_type: 'Loamy',
  crop_type: 'Wheat',
  nitrogen: 50,
  potassium: 30,
  phosphorous: 40
};

const soilTypes = ['Red', 'Black', 'Sandy', 'Loamy', 'Clayey'];
const cropTypes = ['Ground Nuts', 'Cotton', 'Sugarcane', 'Wheat', 'Tobacco', 'Barley', 
                  'Millets', 'Pulses', 'Oil seeds', 'Maize', 'Paddy'];

const FertilizerRecommendation = () => {
  const { theme } = useTheme();
  const { t } = useTranslation();
  const [form, setForm] = useState(defaultForm);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Chart colors for both light and dark themes
  const chartColors = useMemo(() => {
    if (theme === 'dark') {
      return {
        background: '#2d2d2d',
        grid: 'rgba(255, 255, 255, 0.1)',
        text: '#f4fff9',
        border: 'rgba(255, 255, 255, 0.2)',
        barColors: [
          'rgba(123, 216, 143, 0.7)',
          'rgba(255, 179, 71, 0.7)',
          'rgba(63, 169, 107, 0.7)',
          'rgba(214, 143, 48, 0.7)',
          'rgba(45, 138, 72, 0.7)',
          'rgba(180, 120, 30, 0.7)',
          'rgba(90, 180, 120, 0.7)'
        ],
        barBorders: [
          'rgba(123, 216, 143, 1)',
          'rgba(255, 179, 71, 1)',
          'rgba(63, 169, 107, 1)',
          'rgba(214, 143, 48, 1)',
          'rgba(45, 138, 72, 1)',
          'rgba(180, 120, 30, 1)',
          'rgba(90, 180, 120, 1)'
        ]
      };
    } else {
      return {
        background: 'rgba(255, 255, 255, 0.9)',
        grid: 'rgba(0, 0, 0, 0.1)',
        text: '#164025',
        border: 'rgba(0, 0, 0, 0.1)',
        barColors: [
          'rgba(45, 138, 72, 0.7)',
          'rgba(214, 143, 48, 0.7)',
          'rgba(63, 169, 107, 0.7)',
          'rgba(255, 179, 71, 0.7)',
          'rgba(123, 216, 143, 0.7)',
          'rgba(180, 120, 30, 0.7)',
          'rgba(90, 180, 120, 0.7)'
        ],
        barBorders: [
          'rgba(45, 138, 72, 1)',
          'rgba(214, 143, 48, 1)',
          'rgba(63, 169, 107, 1)',
          'rgba(255, 179, 71, 1)',
          'rgba(123, 216, 143, 1)',
          'rgba(180, 120, 30, 1)',
          'rgba(90, 180, 120, 1)'
        ]
      };
    }
  }, [theme]);

  // Data distribution chart options
  const dataDistributionOptions = useMemo(() => ({
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: chartColors.text
        }
      },
      title: {
        display: true,
        text: t('fertilizer.distributionInDataset'),
        color: chartColors.text,
        font: {
          size: 16
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: chartColors.grid
        },
        ticks: {
          color: chartColors.text
        }
      },
      x: {
        grid: {
          color: chartColors.grid
        },
        ticks: {
          color: chartColors.text
        }
      }
    }
  }), [chartColors]);

  // Data distribution chart data
  const dataDistributionData = useMemo(() => ({
    labels: ['14-35-14', '10-26-26', 'Urea', '28-28', 'DAP', '20-20', '17-17-17'],
    datasets: [
      {
        label: 'Number of Samples',
        data: [14492, 14378, 14325, 14232, 14220, 14181, 14172],
        backgroundColor: chartColors.barColors,
        borderColor: chartColors.barBorders,
        borderWidth: 1,
      },
    ],
  }), [chartColors]);

  // Soil type distribution chart data
  const soilTypeData = useMemo(() => ({
    labels: ['Black', 'Sandy', 'Loamy', 'Clayey', 'Red'],
    datasets: [
      {
        data: [20100, 20064, 19999, 19920, 19917],
        backgroundColor: [
          'rgba(45, 138, 72, 0.7)',
          'rgba(214, 143, 48, 0.7)',
          'rgba(63, 169, 107, 0.7)',
          'rgba(123, 216, 143, 0.7)',
          'rgba(255, 179, 71, 0.7)'
        ],
        borderColor: [
          'rgba(45, 138, 72, 1)',
          'rgba(214, 143, 48, 1)',
          'rgba(63, 169, 107, 1)',
          'rgba(123, 216, 143, 1)',
          'rgba(255, 179, 71, 1)'
        ],
        borderWidth: 1,
      },
    ],
  }), []);

  // Crop type distribution chart data
  const cropTypeData = useMemo(() => ({
    labels: ['Sugarcane', 'Cotton', 'Tobacco', 'Millets', 'Paddy', 'Oil seeds', 'Pulses', 'Barley', 'Maize', 'Wheat', 'Ground Nuts'],
    datasets: [
      {
        label: 'Number of Samples',
        data: [9267, 9237, 9224, 9154, 9103, 9096, 9072, 9041, 9013, 8912, 8881],
        backgroundColor: chartColors.barColors,
        borderColor: chartColors.barBorders,
        borderWidth: 1,
      },
    ],
  }), [chartColors]);

  // Feature comparison chart data (average values across fertilizers)
  const featureComparisonData = useMemo(() => ({
    labels: ['14-35-14', '10-26-26', 'Urea', '28-28', 'DAP', '20-20', '17-17-17'],
    datasets: [
      {
        label: 'Temperature (°C)',
        data: [31.53, 31.49, 31.51, 31.51, 31.50, 31.51, 31.47],
        borderColor: chartColors.barColors[0],
        backgroundColor: chartColors.barColors[0],
        tension: 0.1
      },
      {
        label: 'Humidity (%)',
        data: [60.94, 60.95, 60.99, 60.92, 61.06, 61.06, 60.99],
        borderColor: chartColors.barColors[1],
        backgroundColor: chartColors.barColors[1],
        tension: 0.1
      },
      {
        label: 'Moisture (%)',
        data: [45.04, 45.02, 44.99, 45.16, 44.99, 45.01, 44.82],
        borderColor: chartColors.barColors[2],
        backgroundColor: chartColors.barColors[2],
        tension: 0.1
      }
    ],
  }), [chartColors]);

  // Feature comparison chart options
  const featureComparisonOptions = useMemo(() => ({
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: chartColors.text
        }
      },
      title: {
        display: true,
        text: 'Average Feature Values Across Fertilizer Types',
        color: chartColors.text,
        font: {
          size: 16
        }
      }
    },
    scales: {
      y: {
        grid: {
          color: chartColors.grid
        },
        ticks: {
          color: chartColors.text
        }
      },
      x: {
        grid: {
          color: chartColors.grid
        },
        ticks: {
          color: chartColors.text
        }
      }
    }
  }), [chartColors]);

  // Detailed warning about the experimental nature of this feature
  const renderDetailedWarning = () => (
    <div className="detailed-warning">
      <div className="warning-header">
        <span className="warning-icon">⚠️</span>
        <h2>EXPERIMENTAL FEATURE - READ BEFORE USING</h2>
      </div>
      <div className="warning-content">
        <p>
          <strong>This fertilizer recommendation system is highly experimental and should NOT be used for actual farming decisions.</strong>
        </p>
        
        <div className="warning-section">
          <h3>Data Analysis Insights:</h3>
          <p>The charts below show our analysis of the dataset used to train this model:</p>
          <div className="chart-grid">
            <div className="chart-container">
              <Bar data={dataDistributionData} options={dataDistributionOptions} />
            </div>
            <div className="chart-container">
              <Pie data={soilTypeData} options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'top',
                    labels: {
                      color: chartColors.text
                    }
                  },
                  title: {
                    display: true,
                    text: t('fertilizer.soilTypeDistribution'),
                    color: chartColors.text,
                    font: {
                      size: 16
                    }
                  }
                }
              }} />
            </div>
          </div>
          <div className="chart-container full-width">
            <Bar data={featureComparisonData} options={featureComparisonOptions} />
          </div>
          <p><strong>Key Findings:</strong></p>
          <ul>
            <li><strong>Balanced Dataset:</strong> All fertilizer types have nearly equal representation (≈14,000 samples each), eliminating bias from class imbalance.</li>
            <li><strong>Similar Feature Values:</strong> The average temperature, humidity, and moisture values are nearly identical across all fertilizer types (31.5°C, 61% humidity, 45% moisture).</li>
            <li><strong>Weak Correlations:</strong> Features show very weak correlations with each other (most values between -0.05 and +0.05), indicating no strong relationships that a model could exploit.</li>
            <li><strong>No Clear Patterns:</strong> There are no distinguishing characteristics in the input features that would help predict the correct fertilizer type.</li>
            <li><strong>Low Model Accuracy:</strong> With such similar input values across all outputs, the model can only achieve ≈15% accuracy, barely better than random guessing (14.3%).</li>
          </ul>
        </div>
        
        <div className="warning-section">
          <h3>{t('fertilizer.whyNotReliable')}</h3>
          <ul>
            <li><strong>Low Model Accuracy:</strong> The machine learning model has an accuracy of only ≈15%, which is barely better than random guessing (14.3% for 7 fertilizer types).</li>
            <li><strong>Poor Data Quality:</strong> Analysis of the dataset shows that soil conditions and crop types have very similar values across all fertilizer types, making it difficult for any model to learn meaningful patterns.</li>
            <li><strong>No Clear Patterns:</strong> Statistical analysis reveals no strong correlations between input features (NPK values, soil type, crop type, etc.) and the recommended fertilizer type.</li>
            <li><strong>Artificial Dataset:</strong> The dataset may have been synthetically generated, which means it doesn't reflect real-world agricultural conditions.</li>
          </ul>
        </div>
        
        <div className="warning-section">
          <h3>{t('fertilizer.whyThisMatters')}</h3>
          <ul>
            <li><strong>Financial Risk:</strong> Using incorrect fertilizer recommendations can lead to crop failure, reduced yields, and significant financial losses.</li>
            <li><strong>Environmental Impact:</strong> Wrong fertilizer application can cause soil degradation, water pollution, and harm to beneficial microorganisms.</li>
            <li><strong>Legal Liability:</strong> Relying on inaccurate recommendations for commercial farming decisions could have legal implications.</li>
          </ul>
        </div>
        
        <div className="warning-section">
          <h3>{t('fertilizer.howToImprove')}</h3>
          <ol>
            <li><strong>Collect Real Data:</strong> Gather authentic data from agricultural research institutions, farms, and soil testing labs.</li>
            <li><strong>Feature Engineering:</strong> Add more relevant features like soil pH, organic matter content, climate zone, and seasonal factors.</li>
            <li><strong>Expert Validation:</strong> Work with agricultural scientists to validate the dataset and recommendations.</li>
            <li><strong>Advanced Models:</strong> Try different algorithms like neural networks or ensemble methods specifically designed for agricultural data.</li>
            <li><strong>Continuous Learning:</strong> Implement feedback mechanisms to improve recommendations based on actual field results.</li>
          </ol>
        </div>
        
        <div className="warning-section">
          <h3>{t('fertilizer.recommendedAlternatives')}</h3>
          <ul>
            <li>Consult with local agricultural extension services</li>
            <li>Use professional soil testing services</li>
            <li>Follow university-based fertilizer recommendation guides</li>
            <li>Seek advice from certified agronomists</li>
          </ul>
        </div>
        
        <p className="final-warning">
          <strong>{t('fertilizer.experimentalDisclaimer')}</strong>
        </p>
      </div>
    </div>
  );

  const updateField = (evt) => {
    const { name, value, type } = evt.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'number' || type === 'range' ? parseFloat(value) || 0 : value
    }));
  };

  const submitRecommendation = async (evt) => {
    evt.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await getFertilizerRecommendation(form);
      if (data.error || data.detail) {
        throw new Error(data.error || data.detail);
      }
      setResult(data);
    } catch (err) {
      setError(err.message || 'Recommendation failed. Please verify the inputs.');
    } finally {
      setLoading(false);
    }
  };

  const renderDisclaimer = () => {
    return (
      <div className="disclaimer-banner">
        <span className="disclaimer-icon">⚠️</span>
        <span className="disclaimer-text">
          <strong>{t('fertilizer.experimentalFeature')}:</strong> {t('fertilizer.lowAccuracyDisclaimer')} 
          {t('fertilizer.doNotRelyDisclaimer')} {t('fertilizer.consultExpertsDisclaimer')}
        </span>
      </div>
    );
  };

  const renderFertilizerInfo = () => {
    if (!result?.fertilizer_info) return null;
    
    const info = result.fertilizer_info;
    return (
      <div className="fertilizer-info-card">
        <h3>{t('fertilizer.recommendedFertilizer')}: {info.name}</h3>
        <p className="fertilizer-description">{info.description}</p>
        <div className="fertilizer-details">
          <div className="detail-item">
            <span className="detail-label">NPK Ratio:</span>
            <span className="detail-value">{info.NPK_ratio}</span>
          </div>
          {info.best_for && info.best_for.length > 0 && (
            <div className="detail-item">
              <span className="detail-label">Best For:</span>
              <span className="detail-value">{info.best_for.join(', ')}</span>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderProbabilities = () => {
    if (!result?.all_probabilities || result.all_probabilities.length === 0) return null;
    
    return (
      <div className="probabilities-section">
        <h3>{t('fertilizer.allProbabilities')}</h3>
        <div className="probabilities-grid">
          {result.all_probabilities.map((item, index) => (
            <div 
              key={item.fertilizer} 
              className={`probability-card ${index === 0 ? 'top-recommendation' : ''}`}
            >
              <div className="fertilizer-name">{item.fertilizer}</div>
              <div className="probability-bar">
                <div 
                  className="probability-fill" 
                  style={{ width: `${item.probability}%` }}
                />
                <span className="probability-value">{item.probability.toFixed(1)}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderInputConditions = () => {
    if (!result?.input_conditions) return null;
    
    const conditions = result.input_conditions;
    return (
      <div className="conditions-section">
        <h3>{t('fertilizer.inputConditions')}</h3>
        <div className="conditions-grid">
          <div className="condition-item">
            <span className="condition-label">Temperature:</span>
            <span className="condition-value">{conditions.temperature}°C</span>
          </div>
          <div className="condition-item">
            <span className="condition-label">Humidity:</span>
            <span className="condition-value">{conditions.humidity}%</span>
          </div>
          <div className="condition-item">
            <span className="condition-label">Moisture:</span>
            <span className="condition-value">{conditions.moisture}%</span>
          </div>
          <div className="condition-item">
            <span className="condition-label">Soil Type:</span>
            <span className="condition-value">{conditions.soil_type}</span>
          </div>
          <div className="condition-item">
            <span className="condition-label">Crop Type:</span>
            <span className="condition-value">{conditions.crop_type}</span>
          </div>
          <div className="condition-item">
            <span className="condition-label">Nitrogen:</span>
            <span className="condition-value">{conditions.nitrogen} mg/kg</span>
          </div>
          <div className="condition-item">
            <span className="condition-label">Potassium:</span>
            <span className="condition-value">{conditions.potassium} mg/kg</span>
          </div>
          <div className="condition-item">
            <span className="condition-label">Phosphorous:</span>
            <span className="condition-value">{conditions.phosphorous} mg/kg</span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className={`fertilizer-recommendation-page ${theme}`}>
      <div className="container">
        <header className="page-header">
          <h1>Fertilizer Recommendation</h1>
          <p className="page-subtitle">
            Get AI-powered fertilizer recommendations based on soil conditions and crop type
          </p>
        </header>
        
        {renderDetailedWarning()}

        <div className="content-grid">
          {/* Input Form Section */}
          <section className="input-section">
            <div className="card">
              <h2>Soil & Crop Information</h2>
              <form onSubmit={submitRecommendation} className="recommendation-form">
                <div className="form-grid">
                  {/* Temperature */}
                  <div className="form-group">
                    <label htmlFor="temperature">Temperature (°C)</label>
                    <input
                      type="number"
                      id="temperature"
                      name="temperature"
                      min="-10"
                      max="50"
                      value={form.temperature}
                      onChange={updateField}
                      className="form-input"
                    />
                    <input
                      type="range"
                      name="temperature"
                      min="-10"
                      max="50"
                      value={form.temperature}
                      onChange={updateField}
                      className="form-slider"
                    />
                  </div>

                  {/* Humidity */}
                  <div className="form-group">
                    <label htmlFor="humidity">Humidity (%)</label>
                    <input
                      type="number"
                      id="humidity"
                      name="humidity"
                      min="0"
                      max="100"
                      value={form.humidity}
                      onChange={updateField}
                      className="form-input"
                    />
                    <input
                      type="range"
                      name="humidity"
                      min="0"
                      max="100"
                      value={form.humidity}
                      onChange={updateField}
                      className="form-slider"
                    />
                  </div>

                  {/* Moisture */}
                  <div className="form-group">
                    <label htmlFor="moisture">Moisture (%)</label>
                    <input
                      type="number"
                      id="moisture"
                      name="moisture"
                      min="0"
                      max="100"
                      value={form.moisture}
                      onChange={updateField}
                      className="form-input"
                    />
                    <input
                      type="range"
                      name="moisture"
                      min="0"
                      max="100"
                      value={form.moisture}
                      onChange={updateField}
                      className="form-slider"
                    />
                  </div>

                  {/* Soil Type */}
                  <div className="form-group">
                    <label htmlFor="soil_type">Soil Type</label>
                    <select
                      id="soil_type"
                      name="soil_type"
                      value={form.soil_type}
                      onChange={updateField}
                      className="form-select"
                    >
                      {soilTypes.map((type) => (
                        <option key={type} value={type}>
                          {type}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Crop Type */}
                  <div className="form-group">
                    <label htmlFor="crop_type">Crop Type</label>
                    <select
                      id="crop_type"
                      name="crop_type"
                      value={form.crop_type}
                      onChange={updateField}
                      className="form-select"
                    >
                      {cropTypes.map((crop) => (
                        <option key={crop} value={crop}>
                          {crop}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Nitrogen */}
                  <div className="form-group">
                    <label htmlFor="nitrogen">Nitrogen (mg/kg)</label>
                    <input
                      type="number"
                      id="nitrogen"
                      name="nitrogen"
                      min="0"
                      max="200"
                      value={form.nitrogen}
                      onChange={updateField}
                      className="form-input"
                    />
                    <input
                      type="range"
                      name="nitrogen"
                      min="0"
                      max="200"
                      value={form.nitrogen}
                      onChange={updateField}
                      className="form-slider"
                    />
                  </div>

                  {/* Potassium */}
                  <div className="form-group">
                    <label htmlFor="potassium">Potassium (mg/kg)</label>
                    <input
                      type="number"
                      id="potassium"
                      name="potassium"
                      min="0"
                      max="200"
                      value={form.potassium}
                      onChange={updateField}
                      className="form-input"
                    />
                    <input
                      type="range"
                      name="potassium"
                      min="0"
                      max="200"
                      value={form.potassium}
                      onChange={updateField}
                      className="form-slider"
                    />
                  </div>

                  {/* Phosphorous */}
                  <div className="form-group">
                    <label htmlFor="phosphorous">Phosphorous (mg/kg)</label>
                    <input
                      type="number"
                      id="phosphorous"
                      name="phosphorous"
                      min="0"
                      max="200"
                      value={form.phosphorous}
                      onChange={updateField}
                      className="form-input"
                    />
                    <input
                      type="range"
                      name="phosphorous"
                      min="0"
                      max="200"
                      value={form.phosphorous}
                      onChange={updateField}
                      className="form-slider"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="submit-button"
                  disabled={loading}
                >
                  {loading ? 'Analyzing...' : 'Get Recommendation'}
                </button>
              </form>
            </div>
          </section>

          {/* Results Section */}
          <section className="results-section">
            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                <span>{error}</span>
              </div>
            )}

            {renderDisclaimer()}

            {result && (
              <>
                <div className="result-card">
                  <h2>Recommendation Results</h2>
                  <div className="confidence-badge">
                    Confidence: {result.confidence?.toFixed(1) || 'N/A'}%
                  </div>
                  {renderFertilizerInfo()}
                  {renderProbabilities()}
                  {renderInputConditions()}
                </div>
              </>
            )}

            {!result && !error && (
              <div className="placeholder-card">
                <div className="placeholder-icon">🌿</div>
                <h3>Enter Soil & Crop Information</h3>
                <p>Fill in the form to get your personalized fertilizer recommendation</p>
              </div>
            )}
          </section>
        </div>
      </div>
    </div>
  );
};

export default FertilizerRecommendation;