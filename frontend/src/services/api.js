// Use environment variable if available, otherwise default to localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Helper function to handle API requests
const apiRequest = async (url, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

// Weather API
export const getWeather = async (lat, lon) => {
  return apiRequest(`/weather?lat=${lat}&lon=${lon}`);
};

export const getWeatherForecast = async (lat, lon) => {
  return apiRequest(`/weather-forecast?lat=${lat}&lon=${lon}`);
};

export const getHistoricalWeather = async (lat, lon, daysAgo) => {
  return apiRequest(`/weather-history?lat=${lat}&lon=${lon}&days_ago=${daysAgo}`);
};

export const getHistoricalWeatherRange = async (lat, lon, days, startDate, endDate) => {
  // Always use the free Open-Meteo API for range queries
  let url = `/weather-history-free?lat=${lat}&lon=${lon}`;

  if (startDate && endDate) {
    url += `&start_date=${startDate}&end_date=${endDate}`;
  } else if (days) {
    url += `&days_ago=${days}`;
  }

  return apiRequest(url);
};

export const getHistoricalWeatherFree = async (lat, lon, daysAgo, startDate, endDate) => {
  let url = `/weather-history-free?lat=${lat}&lon=${lon}`;

  if (startDate && endDate) {
    url += `&start_date=${startDate}&end_date=${endDate}`;
  } else if (daysAgo) {
    url += `&days_ago=${daysAgo}`;
  }

  return apiRequest(url);
};

export const getAvailableModels = async () => {
  return apiRequest('/models');
};

export const predictCrop = async (data) => {
  return apiRequest('/predict', {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const compareModels = async (data) => {
  return apiRequest('/compare-models', {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const explainPrediction = async (data) => {
  return apiRequest('/explain-prediction', {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

// History API
export const getPredictionHistory = async (params = {}) => {
  const queryString = new URLSearchParams(params).toString();
  return apiRequest(`/history?${queryString}`);
};



// Export API
export const exportData = async (format, params = {}) => {
  const queryString = new URLSearchParams({ format, ...params }).toString();
  return fetch(`${API_BASE_URL}/export?${queryString}`);
};

// Download PDF
export const downloadPDF = async (farmerName) => {
  return fetch(`${API_BASE_URL}/download?farmer_name=${encodeURIComponent(farmerName)}`);
};

export const getMarketPrices = async (crop, state = null, district = null) => {
  let url = `/market-prices?crop=${encodeURIComponent(crop)}`;
  if (state) url += `&state=${encodeURIComponent(state)}`;
  if (district) url += `&district=${encodeURIComponent(district)}`;
  return apiRequest(url);
};

export const getPriceTrend = async (crop, state = null, days = 30) => {
  let url = `/price-trend?crop=${encodeURIComponent(crop)}&days=${days}`;
  if (state) url += `&state=${encodeURIComponent(state)}`;
  return apiRequest(url);
};

export const getMarketRecommendation = async (crop, state = null) => {
  let url = `/market-recommendation?crop=${encodeURIComponent(crop)}`;
  if (state) url += `&state=${encodeURIComponent(state)}`;
  return apiRequest(url);
};

// Fertilizer Recommendation API
export const getFertilizerRecommendation = async (data) => {
  return apiRequest('/fertilizer-recommendation', {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

// Auto-detect location from GPS coordinates
export const autoDetectLocation = async (lat, lon) => {
  return apiRequest(`/auto-location?lat=${lat}&lon=${lon}`);
};

export default {
  getWeather,
  getWeatherForecast,
  getHistoricalWeather,
  getHistoricalWeatherRange,
  getHistoricalWeatherFree,
  getAvailableModels,
  predictCrop,
  compareModels,
  explainPrediction,
  getPredictionHistory,
  exportData,
  downloadPDF,
  getMarketPrices,
  getPriceTrend,
  getMarketRecommendation,
  getFertilizerRecommendation
};
