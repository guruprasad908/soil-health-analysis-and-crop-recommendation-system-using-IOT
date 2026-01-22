// useMixedLayout.js
// Custom hook for fetching mixed cropping layout data

import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook to fetch mixed cropping layout data
 * @param {string} crop - Main crop name
 * @param {number} landSize - Land size in acres
 * @returns {object} - Layout data, loading state, error state, and retry function
 */
export const useMixedLayout = (crop, landSize) => {
  const [layoutData, setLayoutData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchLayout = useCallback(async () => {
    if (!crop || landSize <= 0) {
      setError('Invalid parameters: crop and land size are required');
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Using v2 endpoint to avoid caching issues with previous implementation
      const response = await fetch(
        `http://localhost:8000/mixed-cropping-layout-v2?crop=${encodeURIComponent(crop)}&land_size=${landSize}`
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch layout: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      setLayoutData(data);
    } catch (err) {
      setError(err.message || 'An error occurred while fetching the layout');
    } finally {
      setLoading(false);
    }
  }, [crop, landSize]);

  useEffect(() => {
    fetchLayout();
  }, [fetchLayout]);

  const retry = () => {
    fetchLayout();
  };

  return { layoutData, loading, error, retry };
};