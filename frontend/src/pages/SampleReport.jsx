import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from '../hooks/useTranslation';
import './SampleReport.css';

const SampleReport = () => {
  const { t } = useTranslation();
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Sample data for the report
    const sampleData = {
      farmer_name: "Sample Farmer",
      phone: "9876543210",
      location: "Sample Village, Sample District",
      land_size: 5.5,
      N: 85,
      P: 42,
      K: 68,
      temperature: 28.5,
      humidity: 65,
      ph: 6.8,
      rainfall: 1100,
      soil_type: "alluvial soil",
      predicted_crop: "Rice",
      confidence: 95.2,
      model_used: "Stacking Classifier",
      top_crops: [
        { crop: "Rice", confidence: 95.2 },
        { crop: "Wheat", confidence: 87.6 },
        { crop: "Maize", confidence: 82.3 }
      ],
      soil_treatment: [
        "✅ Current nitrogen levels are adequate for rice cultivation",
        "⚠️ Phosphorus levels are slightly below optimal range",
        "✅ Potassium levels are good for crop growth",
        "✅ Soil pH is within the ideal range for rice (5.5-7.0)"
      ],
      fertilizer_estimate: "For 5.5 acres of land:\n- Nitrogen (Urea): 45 kg/acre (247.5 kg total)\n- Phosphorus (DAP): 30 kg/acre (165 kg total)\n- Potassium (MOP): 25 kg/acre (137.5 kg total)\n\nApplication schedule:\n1. Basal application: 50% Nitrogen + Full Phosphorus + 50% Potassium\n2. Tillering stage: 25% Nitrogen + 25% Potassium\n3. Panicle initiation: 25% Nitrogen + 25% Potassium",
      soil_health: {
        overall_score: 82.5,
        category: "Good",
        color: "#2ecc71",
        recommendations: [
          "Maintain current nitrogen management practices",
          "Consider adding phosphorus-rich organic matter",
          "Monitor soil pH regularly",
          "Implement proper water management for rice cultivation"
        ],
        breakdown: {
          nitrogen_level: 14,
          phosphorus_level: 10,
          potassium_level: 12,
          ph_balance: 18,
          nutrient_balance: 13,
          temperature_suitability: 5,
          humidity_suitability: 5,
          rainfall_adequacy: 5,
          soil_type_compatibility: 10
        }
      },
      warnings: [
        "⚠️ Heavy rainfall expected in next 3 days. Consider drainage planning.",
        "⚠️ Phosphorus levels are slightly below optimal range. Apply DAP as recommended."
      ]
    };

    setReportData(sampleData);
    setLoading(false);
  }, []);

  const formatPercentage = (value) => {
    return `${value.toFixed(1)}%`;
  };

  const formatSoilHealthScore = (score) => {
    if (score >= 80) return { label: 'Excellent', color: 'success' };
    if (score >= 65) return { label: 'Good', color: 'warning' };
    if (score >= 50) return { label: 'Fair', color: 'caution' };
    return { label: 'Poor', color: 'danger' };
  };

  if (loading) {
    return (
      <div className="sample-report-page">
        <div className="container">
          <div className="loading">
            <div className="spinner"></div>
            <p>{t('sample.generatingReport')}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="sample-report-page">
      <div className="container">
        <div className="report-header">
          <Link to="/" className="back-link">← {t('sample.backToHome')}</Link>
          <div className="header-actions">
            <button className="btn-primary" onClick={() => window.print()}>
              🖨️ Print Report
            </button>
          </div>
        </div>

        <div className="report-card">
          <div className="report-header-section">
            <h1>{t('sample.soilHealthReport')}</h1>
            <div className="report-meta">
              <div className="meta-item">
                <span className="label">{t('sample.generated')}:</span>
                <span>{new Date().toLocaleDateString()}</span>
              </div>
              <div className="meta-item">
                <span className="label">{t('sample.farmer')}:</span>
                <span>{reportData.farmer_name}</span>
              </div>
              <div className="meta-item">
                <span className="label">{t('sample.location')}:</span>
                <span>{reportData.location}</span>
              </div>
            </div>
          </div>

          {reportData.warnings && reportData.warnings.length > 0 && (
            <div className="warnings-section">
              <h3>⚠️ {t('sample.importantWarnings')}</h3>
              <ul>
                {reportData.warnings.map((warning, index) => (
                  <li key={index}>{warning.replace("⚠️", "").trim()}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="prediction-section">
            <h2>🌾 {t('sample.predictedCrop')}</h2>
            <div className="prediction-result">
              <div className="crop-info">
                <h3>{reportData.predicted_crop}</h3>
                <p>{t('sample.model')}: {reportData.model_used}</p>
              </div>
              <div className="confidence-chip">
                <span>Confidence</span>
                <strong>{formatPercentage(reportData.confidence)}</strong>
              </div>
            </div>

            {reportData.top_crops && reportData.top_crops.length > 1 && (
              <div className="alternatives-section">
                <h3>{t('sample.alternativeCrops')}</h3>
                <div className="alternatives-grid">
                  {reportData.top_crops.slice(1).map((crop, index) => (
                    <div className="alternative-card" key={index}>
                      <span className="crop-name">{crop.crop}</span>
                      <span className="crop-confidence">{formatPercentage(crop.confidence)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="soil-health-section">
            <h2>🧪 {t('sample.soilHealthAnalysis')}</h2>
            <div className="health-overview">
              <div className="health-score">
                <span className="label">{t('sample.overallScore')}</span>
                <div className="score-value">
                  <strong>{reportData.soil_health.overall_score.toFixed(1)}</strong>
                  <span>/100</span>
                </div>
                <span className={`status status-${formatSoilHealthScore(reportData.soil_health.overall_score).color}`}>
                  {formatSoilHealthScore(reportData.soil_health.overall_score).label}
                </span>
              </div>
              
              <div className="health-breakdown">
                <h3>{t('sample.componentScores')}</h3>
                <div className="breakdown-grid">
                  {Object.entries(reportData.soil_health.breakdown).map(([key, value]) => (
                    <div className="breakdown-item" key={key}>
                      <span className="label">{key.replace(/_/g, ' ')}</span>
                      <span className="value">{value.toFixed(1)}/20</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {reportData.soil_health.recommendations && (
              <div className="recommendations-section">
                <h3>{t('sample.recommendations')}</h3>
                <ul>
                  {reportData.soil_health.recommendations.map((rec, index) => (
                    <li key={index}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <div className="input-parameters">
            <h2>📊 Input Parameters</h2>
            <div className="parameters-grid">
              <div className="parameter-card">
                <span className="label">Nitrogen (N)</span>
                <span className="value">{reportData.N} mg/kg</span>
              </div>
              <div className="parameter-card">
                <span className="label">Phosphorus (P)</span>
                <span className="value">{reportData.P} mg/kg</span>
              </div>
              <div className="parameter-card">
                <span className="label">Potassium (K)</span>
                <span className="value">{reportData.K} mg/kg</span>
              </div>
              <div className="parameter-card">
                <span className="label">pH Level</span>
                <span className="value">{reportData.ph}</span>
              </div>
              <div className="parameter-card">
                <span className="label">Temperature</span>
                <span className="value">{reportData.temperature}°C</span>
              </div>
              <div className="parameter-card">
                <span className="label">Humidity</span>
                <span className="value">{reportData.humidity}%</span>
              </div>
              <div className="parameter-card">
                <span className="label">Rainfall</span>
                <span className="value">{reportData.rainfall} mm</span>
              </div>
              <div className="parameter-card">
                <span className="label">Soil Type</span>
                <span className="value">{reportData.soil_type}</span>
              </div>
            </div>
          </div>

          <div className="treatment-section">
            <h2>💊 Soil Treatment Recommendations</h2>
            <ul>
              {reportData.soil_treatment.map((treatment, index) => (
                <li key={index} className={treatment.startsWith('✅') ? 'success' : 'warning'}>
                  {treatment.replace(/✅|⚠️/g, '').trim()}
                </li>
              ))}
            </ul>
          </div>

          <div className="fertilizer-section">
            <h2>📦 Fertilizer Application Guide</h2>
            <pre>{reportData.fertilizer_estimate}</pre>
          </div>

          <div className="footer-section">
            <p>Report generated by SoilSense Intelligent Agriculture System</p>
            <p>This analysis is based on machine learning models and should be used as a guide alongside expert consultation.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SampleReport;