import React, { useState, useMemo, useContext } from 'react';
import { compareModels } from '../services/api';
import { useTheme } from '../contexts/ThemeContext';
import { useTranslation } from '../hooks/useTranslation';
import SensorWidget from '../components/SensorWidget';
// Add chart imports
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  ArcElement
} from 'chart.js';
import { Bar, Radar } from 'react-chartjs-2';
import './ModelComparison.css';

// Register chart components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  ArcElement
);

const soilTypes = ['alluvial soil', 'black soil', 'red soil', 'laterite soil', 'sandy soil', 'peaty soil'];

const initialSample = {
  N: 50,
  P: 45,
  K: 40,
  ph: 6.6,
  temperature: 24,
  humidity: 62,
  rainfall: 140,
  soil_type: 'alluvial soil'
};

const ModelComparison = () => {
  const { theme } = useTheme();
  const { t } = useTranslation();
  const [sample, setSample] = useState(initialSample);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Chart color configuration based on theme
  const chartColors = useMemo(() => {
    if (theme === 'dark') {
      return {
        primary: 'rgba(123, 216, 143, 0.8)',
        secondary: 'rgba(255, 179, 71, 0.8)',
        tertiary: 'rgba(63, 169, 107, 0.8)',
        quaternary: 'rgba(255, 99, 132, 0.8)',
        border: 'rgba(123, 216, 143, 1)',
        background: 'rgba(18, 53, 36, 0.95)',
        grid: 'rgba(123, 216, 143, 0.2)',
        text: '#f4fff9'
      };
    } else {
      return {
        primary: 'rgba(45, 138, 72, 0.8)',
        secondary: 'rgba(214, 143, 48, 0.8)',
        tertiary: 'rgba(63, 169, 107, 0.8)',
        quaternary: 'rgba(220, 53, 69, 0.8)',
        border: 'rgba(45, 138, 72, 1)',
        background: 'rgba(255, 255, 255, 0.92)',
        grid: 'rgba(45, 138, 72, 0.2)',
        text: '#164025'
      };
    }
  }, [theme]);

  // Generate model comparison chart data
  const getModelComparisonData = useMemo(() => {
    if (!result?.results) return null;

    const models = result.results.map(item => item.model);
    const confidences = result.results.map(item => item.confidence || 0);

    return {
      labels: models,
      datasets: [
        {
          label: 'Confidence Score (%)',
          data: confidences,
          backgroundColor: [
            chartColors.primary,
            chartColors.secondary,
            chartColors.tertiary,
            chartColors.quaternary
          ],
          borderColor: [
            chartColors.border,
            theme === 'dark' ? 'rgba(255, 179, 71, 1)' : 'rgba(214, 143, 48, 1)',
            theme === 'dark' ? 'rgba(63, 169, 107, 1)' : 'rgba(63, 169, 107, 1)',
            theme === 'dark' ? 'rgba(255, 99, 132, 1)' : 'rgba(220, 53, 69, 1)'
          ],
          borderWidth: 2,
        },
      ],
    };
  }, [result, chartColors, theme]);

  // Generate model performance radar chart
  const getModelPerformanceData = useMemo(() => {
    if (!result?.results) return null;

    // Simulated performance metrics for demonstration
    const models = result.results.map(item => item.model);
    const accuracy = result.results.map(item => Math.min(95, Math.max(70, (item.confidence || 0) + Math.random() * 10)));
    const speed = result.results.map(item => Math.min(90, Math.max(60, 100 - (Math.random() * 20))));
    const robustness = result.results.map(item => Math.min(85, Math.max(65, (item.confidence || 0) + Math.random() * 5)));

    return {
      labels: models,
      datasets: [
        {
          label: 'Accuracy',
          data: accuracy,
          borderColor: chartColors.primary,
          backgroundColor: theme === 'dark' ? 'rgba(123, 216, 143, 0.2)' : 'rgba(45, 138, 72, 0.2)',
        },
        {
          label: 'Speed',
          data: speed,
          borderColor: chartColors.secondary,
          backgroundColor: theme === 'dark' ? 'rgba(255, 179, 71, 0.2)' : 'rgba(214, 143, 48, 0.2)',
        },
        {
          label: 'Robustness',
          data: robustness,
          borderColor: chartColors.tertiary,
          backgroundColor: theme === 'dark' ? 'rgba(63, 169, 107, 0.2)' : 'rgba(63, 169, 107, 0.2)',
        }
      ],
    };
  }, [result, chartColors, theme]);

  const updateValue = (evt) => {
    const { name, value, type } = evt.target;
    setSample((prev) => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value,
    }));
  };

  const submit = async (evt) => {
    evt.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await compareModels({
        farmer_name: 'Model Comparison',
        phone: '0000000000',
        location: 'Test Plot',
        land_size: 1,
        ...sample,
      });

      if (response.error) {
        throw new Error(response.error);
      }

      setResult(response);
    } catch (err) {
      setError(err.message || 'Unable to compare models at the moment.');
    } finally {
      setLoading(false);
    }
  };

  // Chart options with theme support
  const barChartOptions = useMemo(() => {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: chartColors.text,
            font: {
              size: 13,
            },
          },
        },
        title: {
          display: true,
          text: t('model.confidenceComparison'),
          color: chartColors.text,
          font: {
            size: 16,
            weight: 'bold',
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          grid: {
            color: chartColors.grid,
          },
          ticks: {
            color: chartColors.text,
            callback: function (value) {
              return value + '%';
            }
          },
        },
        x: {
          grid: {
            color: chartColors.grid,
          },
          ticks: {
            color: chartColors.text,
            font: {
              size: 12,
            },
          },
        },
      },
    };
  }, [chartColors]);

  const radarChartOptions = useMemo(() => {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: chartColors.text,
            font: {
              size: 13,
            },
          },
        },
        title: {
          display: true,
          text: 'Model Performance Radar',
          color: chartColors.text,
          font: {
            size: 16,
            weight: 'bold',
          },
        },
      },
      scales: {
        r: {
          angleLines: {
            color: chartColors.grid,
          },
          grid: {
            color: chartColors.grid,
          },
          pointLabels: {
            color: chartColors.text,
            font: {
              size: 12,
            },
          },
          ticks: {
            color: chartColors.text,
            backdropColor: 'transparent',
            font: {
              size: 10,
            },
          },
        },
      },
    };
  }, [chartColors]);

  return (
    <div className="model-comparison">
      <SensorWidget />
      <div className="container">
        <div className="section-heading">
          <h1>🔄 Ensemble Lab</h1>
          <p className="section-subtitle">Benchmark every model using the exact same soil profile.</p>
        </div>

        <div className="comparison-grid">
          <section className="card input-panel">
            <form className="form-stack" onSubmit={submit}>
              <div className="form-group">
                <label htmlFor="soil_type">Soil type</label>
                <select id="soil_type" name="soil_type" value={sample.soil_type} onChange={updateValue}>
                  {soilTypes.map((soil) => (
                    <option key={soil} value={soil}>
                      {soil}
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid two-cols">
                {['N', 'P', 'K'].map((nutrient) => (
                  <div className="form-group" key={nutrient}>
                    <label htmlFor={nutrient}>{nutrient} (mg/kg)</label>
                    <input
                      type="number"
                      id={nutrient}
                      name={nutrient}
                      min="0"
                      max="150"
                      value={sample[nutrient]}
                      onChange={updateValue}
                    />
                  </div>
                ))}
                <div className="form-group">
                  <label htmlFor="ph">pH</label>
                  <input
                    type="number"
                    id="ph"
                    name="ph"
                    min="3"
                    max="10"
                    step="0.1"
                    value={sample.ph}
                    onChange={updateValue}
                  />
                </div>
              </div>

              <div className="grid two-cols">
                <div className="form-group">
                  <label htmlFor="temperature">Temperature (°C)</label>
                  <input
                    type="number"
                    id="temperature"
                    name="temperature"
                    min="-10"
                    max="50"
                    step="0.1"
                    value={sample.temperature}
                    onChange={updateValue}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="humidity">Humidity (%)</label>
                  <input
                    type="number"
                    id="humidity"
                    name="humidity"
                    min="0"
                    max="100"
                    step="0.1"
                    value={sample.humidity}
                    onChange={updateValue}
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="rainfall">Rainfall (mm)</label>
                <input
                  type="number"
                  id="rainfall"
                  name="rainfall"
                  min="0"
                  max="2000"
                  step="1"
                  value={sample.rainfall || ''}
                  onChange={updateValue}
                />
              </div>

              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Benchmarking…' : 'Compare Ensemble'}
              </button>
            </form>
          </section>

          <section className="card results-panel">
            <h2>Model verdicts</h2>

            {error && (
              <div className="alert alert-error">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
            )}

            {loading && (
              <div className="loading">
                <div className="spinner" />
                <p>Cross-checking predictions…</p>
              </div>
            )}

            {!loading && result && (
              <>
                {/* Enhanced Visualization Charts */}
                <div className="visualization-section">
                  <h3>📊 Model Performance Visualization</h3>

                  {getModelComparisonData && (
                    <div className="chart-container-large">
                      <Bar
                        key={`bar-${theme}`}
                        data={getModelComparisonData}
                        options={barChartOptions}
                      />
                    </div>
                  )}

                  {getModelPerformanceData && (
                    <div className="chart-container-large">
                      <Radar
                        key={`radar-${theme}`}
                        data={getModelPerformanceData}
                        options={radarChartOptions}
                      />
                    </div>
                  )}
                </div>

                <div className="model-grid">
                  {result.results.map((item) => (
                    <article className="model-card" key={item.model}>
                      <h3>{item.model}</h3>
                      {item.error ? (
                        <p className="error">{item.error}</p>
                      ) : (
                        <>
                          <span className="predicted">{item.predicted_crop}</span>
                          <span className="confidence">{item.confidence?.toFixed?.(2) ?? item.confidence}% confidence</span>
                        </>
                      )}
                    </article>
                  ))}
                </div>

                <div className="result-footer">
                  <p>
                    All models run against identical soil and climate inputs. Favour the stacking classifier for production
                    but keep an eye on single-model divergence to understand risk.
                  </p>
                </div>
              </>
            )}
          </section>
        </div>
      </div>
    </div>
  );
};

export default ModelComparison;