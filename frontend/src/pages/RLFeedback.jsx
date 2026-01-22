import React, { useState } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import './RLFeedback.css';

const RLFeedback = () => {
  const { theme } = useTheme();
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: '',
    soil_type: 'alluvial soil',
    recommended_crop: '',
    actual_crop: '',
    success: true,
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // Validate required fields
      if (!formData.recommended_crop || !formData.actual_crop) {
        throw new Error('Please fill in all required fields');
      }

      const feedbackPayload = {
        N: Number(formData.N),
        P: Number(formData.P),
        K: Number(formData.K),
        temperature: Number(formData.temperature),
        humidity: Number(formData.humidity),
        ph: Number(formData.ph),
        rainfall: Number(formData.rainfall),
        soil_type: formData.soil_type,
        recommended_crop: formData.recommended_crop,
        actual_crop: formData.actual_crop,
        success: formData.success
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
      setSuccess(`✅ ${data.message}\n\nReward: ${data.reward}\nModel is learning from your feedback!`);
      
      // Reset form
      setFormData({
        N: '',
        P: '',
        K: '',
        temperature: '',
        humidity: '',
        ph: '',
        rainfall: '',
        soil_type: 'alluvial soil',
        recommended_crop: '',
        actual_crop: '',
        success: true,
        notes: ''
      });

    } catch (err) {
      setError(err.message || 'Failed to submit feedback. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`page ${theme}`}>
      <div className="container">
        <header className="page-header">
          <h1>🔄 Reinforcement Learning Feedback</h1>
          <p className="subtitle">
            Help improve the RL model by sharing your crop experiences
          </p>
        </header>

        <section className="card">
          <form onSubmit={handleSubmit}>
            <div className="form-section">
              <h2>Soil & Weather Conditions</h2>
              
              <div className="grid two-cols">
                <div className="form-group">
                  <label htmlFor="N">Nitrogen (N) - mg/kg *</label>
                  <input
                    id="N"
                    name="N"
                    type="number"
                    min="0"
                    max="200"
                    step="1"
                    value={formData.N}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="P">Phosphorus (P) - mg/kg *</label>
                  <input
                    id="P"
                    name="P"
                    type="number"
                    min="0"
                    max="200"
                    step="1"
                    value={formData.P}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
              
              <div className="grid two-cols">
                <div className="form-group">
                  <label htmlFor="K">Potassium (K) - mg/kg *</label>
                  <input
                    id="K"
                    name="K"
                    type="number"
                    min="0"
                    max="200"
                    step="1"
                    value={formData.K}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="temperature">Temperature (°C) *</label>
                  <input
                    id="temperature"
                    name="temperature"
                    type="number"
                    min="-10"
                    max="50"
                    step="0.1"
                    value={formData.temperature}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
              
              <div className="grid two-cols">
                <div className="form-group">
                  <label htmlFor="humidity">Humidity (%) *</label>
                  <input
                    id="humidity"
                    name="humidity"
                    type="number"
                    min="0"
                    max="100"
                    step="0.1"
                    value={formData.humidity}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="ph">pH Level *</label>
                  <input
                    id="ph"
                    name="ph"
                    type="number"
                    min="0"
                    max="14"
                    step="0.1"
                    value={formData.ph}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
              
              <div className="grid two-cols">
                <div className="form-group">
                  <label htmlFor="rainfall">Rainfall (mm) *</label>
                  <input
                    id="rainfall"
                    name="rainfall"
                    type="number"
                    min="0"
                    max="5000"
                    step="1"
                    value={formData.rainfall}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="soil_type">Soil Type *</label>
                  <select
                    id="soil_type"
                    name="soil_type"
                    value={formData.soil_type}
                    onChange={handleChange}
                    required
                  >
                    <option value="alluvial soil">Alluvial Soil</option>
                    <option value="black soil">Black Soil</option>
                    <option value="red soil">Red Soil</option>
                    <option value="laterite soil">Laterite Soil</option>
                    <option value="sandy soil">Sandy Soil</option>
                    <option value="peaty soil">Peaty Soil</option>
                  </select>
                </div>
              </div>
            </div>
            
            <div className="form-section">
              <h2>Crop Information</h2>
              
              <div className="grid two-cols">
                <div className="form-group">
                  <label htmlFor="recommended_crop">Recommended Crop *</label>
                  <input
                    id="recommended_crop"
                    name="recommended_crop"
                    type="text"
                    value={formData.recommended_crop}
                    onChange={handleChange}
                    placeholder="e.g., chilli, jowar, cotton"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="actual_crop">Actual Crop Planted *</label>
                  <input
                    id="actual_crop"
                    name="actual_crop"
                    type="text"
                    value={formData.actual_crop}
                    onChange={handleChange}
                    placeholder="e.g., chilli, jowar, cotton"
                    required
                  />
                </div>
              </div>
              
              <div className="form-group">
                <label>
                  <input
                    type="checkbox"
                    name="success"
                    checked={formData.success}
                    onChange={handleChange}
                  />
                  Did the crop grow well?
                </label>
              </div>
            </div>
            
            <div className="form-section">
              <h2>Additional Notes</h2>
              <div className="form-group">
                <label htmlFor="notes">Any additional details about your experience</label>
                <textarea
                  id="notes"
                  name="notes"
                  value={formData.notes}
                  onChange={handleChange}
                  placeholder="Share any observations, challenges, or insights..."
                  rows="4"
                />
              </div>
            </div>
            
            {error && (
              <div className="alert alert-error">
                ⚠️ {error}
              </div>
            )}
            
            {success && (
              <div className="alert alert-success">
                {success.split('\n').map((line, i) => (
                  <div key={i}>{line}</div>
                ))}
              </div>
            )}
            
            <div className="form-actions">
              <button 
                type="submit" 
                className="btn-primary"
                disabled={loading}
              >
                {loading ? 'Submitting Feedback...' : 'Submit Feedback'}
              </button>
            </div>
          </form>
        </section>
        
        <section className="card info-section">
          <h2>How RL Feedback Works</h2>
          <div className="info-grid">
            <div className="info-item">
              <h3>✅ Positive Feedback</h3>
              <p>If you followed the recommendation and it worked well, you get +1.0 reward</p>
            </div>
            <div className="info-item">
              <h3>🟡 Partial Success</h3>
              <p>If you chose a different crop that worked, you get +0.5 reward</p>
            </div>
            <div className="info-item">
              <h3>❌ Negative Feedback</h3>
              <p>If the recommendation didn't work, you get -1.0 reward</p>
            </div>
          </div>
          <p className="info-note">
            The RL model uses this feedback to continuously improve its recommendations for North Karnataka farmers.
          </p>
        </section>
      </div>
    </div>
  );
};

export default RLFeedback;