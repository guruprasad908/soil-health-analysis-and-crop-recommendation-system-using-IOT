// Format numbers with commas
export const formatNumber = (num) => {
  if (num === null || num === undefined) return 'N/A';
  return num.toLocaleString();
};

// Format currency
export const formatCurrency = (amount, currency = 'USD') => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(amount);
};

// Format percentage
export const formatPercentage = (value) => {
  if (value === null || value === undefined) return 'N/A';
  return `${value.toFixed(1)}%`;
};

// Format soil health score
export const formatSoilHealthScore = (score) => {
  if (score >= 80) return { label: 'Excellent', color: 'green' };
  if (score >= 65) return { label: 'Good', color: 'lightgreen' };
  if (score >= 50) return { label: 'Fair', color: 'orange' };
  return { label: 'Poor', color: 'red' };
};

// Format confidence score
export const formatConfidence = (confidence) => {
  if (confidence >= 80) return { label: 'High', color: 'green' };
  if (confidence >= 60) return { label: 'Medium', color: 'orange' };
  return { label: 'Low', color: 'red' };
};

export default {
  formatNumber,
  formatCurrency,
  formatPercentage,
  formatSoilHealthScore,
  formatConfidence,
};