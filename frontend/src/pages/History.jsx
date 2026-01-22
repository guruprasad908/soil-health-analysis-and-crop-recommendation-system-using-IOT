import React, { useEffect, useState } from 'react';
import { getPredictionHistory, exportData } from '../services/api';
import { useTranslation } from '../hooks/useTranslation';
import './History.css';

const History = () => {
  const { t } = useTranslation();
  const [records, setRecords] = useState([]);
  const [filters, setFilters] = useState({ farmer_name: '', phone: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const loadHistory = async (params = {}) => {
    setLoading(true);
    setError('');
    try {
      const response = await getPredictionHistory(params);
      if (response.error) {
        throw new Error(response.error);
      }
      setRecords(response.predictions || []);
    } catch (err) {
      setError(err.message || 'Unable to fetch history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleChange = (evt) => {
    const { name, value } = evt.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const submitFilters = (evt) => {
    evt.preventDefault();
    loadHistory(filters);
  };

  const handleExport = async (format) => {
    try {
      const response = await exportData(format, filters);
      if (!response.ok) {
        throw new Error('Export failed');
      }
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `prediction-history.${format === 'excel' ? 'xlsx' : 'csv'}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="history-view">
      <div className="container">
        <div className="section-heading">
          <h1>📊 {t('history.title')}</h1>
          <p className="section-subtitle">{t('history.subtitle')}</p>
        </div>

        <div className="history-layout">
          <section className="card filter-panel">
            <form className="form-stack" onSubmit={submitFilters}>
              <div className="grid two-cols">
                <div className="form-group">
                  <label htmlFor="farmer_name">{t('history.farmerName')}</label>
                  <input id="farmer_name" name="farmer_name" value={filters.farmer_name} onChange={handleChange} placeholder="e.g. Ramesh" />
                </div>
                <div className="form-group">
                  <label htmlFor="phone">{t('history.phone')}</label>
                  <input id="phone" name="phone" value={filters.phone} onChange={handleChange} placeholder="10-digit phone" />
                </div>
              </div>
              <div className="filter-actions">
                <button type="submit" className="btn-primary" disabled={loading}>
                  {loading ? 'Filtering…' : 'Apply filters'}
                </button>
                <button type="button" className="btn-ghost" onClick={() => handleExport('csv')}>
                  Export CSV
                </button>
                <button type="button" className="btn-ghost" onClick={() => handleExport('excel')}>
                  Export Excel
                </button>
              </div>
            </form>
          </section>

          <div className="history-results">
            {error && (
              <div className="alert alert-error">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
            )}

            {loading && (
              <div className="loading">
                <div className="spinner" />
                <p>{t('history.fetching')}</p>
              </div>
            )}

            {!loading && records.length === 0 && !error && (
              <div className="card empty-state">
                <p>{t('history.noHistory')}</p>
              </div>
            )}

            {!loading && records.length > 0 && (
              <section className="card history-panel">
                <header className="history-head">
                  <div>
                    <span className="badge">{t('history.recentAdvisories')}</span>
                    <h2>{records.length} {t('history.records')}</h2>
                  </div>
                </header>
                <div className="table-scroll">
                  <table>
                    <thead>
                      <tr>
                        <th>Farmer</th>
                        <th>Location</th>
                        <th>Soil type</th>
                        <th>Crop</th>
                        <th>Model</th>
                        <th>Confidence</th>
                        <th>Soil health</th>
                        <th>Created</th>
                      </tr>
                    </thead>
                    <tbody>
                      {records.map((row) => (
                        <tr key={row.id}>
                          <td>{row.farmer_name}</td>
                          <td>{row.location}</td>
                          <td>{row.soil_type}</td>
                          <td>{row.predicted_crop}</td>
                          <td>{row.model_used}</td>
                          <td>{row.confidence ? `${row.confidence.toFixed(1)}%` : '—'}</td>
                          <td>{row.soil_health_score ? `${row.soil_health_score.toFixed(1)}` : '—'}</td>
                          <td>{new Date(row.timestamp).toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default History;