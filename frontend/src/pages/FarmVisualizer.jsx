// FarmVisualizer.jsx
// Main page component for the mixed cropping planner and aerial farm visualizer

import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { useMixedLayout } from '../hooks/useMixedLayout';
import FarmCanvas from '../components/FarmCanvas';
import '../styles/farmVisualizer.css';

const FarmVisualizer = () => {
  const location = useLocation();
  const canvasContainerRef = useRef(null);
  const [containerSize, setContainerSize] = useState({ width: 800, height: 600 });

  // Parse query parameters
  const queryParams = new URLSearchParams(location.search);
  const crop = queryParams.get('crop');
  const landSize = parseFloat(queryParams.get('land_size')) || 1;

  const { layoutData, loading, error, retry } = useMixedLayout(crop, landSize);

  // Update container size on resize
  useEffect(() => {
    const updateSize = () => {
      if (canvasContainerRef.current) {
        setContainerSize({
          width: canvasContainerRef.current.offsetWidth,
          height: canvasContainerRef.current.offsetHeight
        });
      }
    };

    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  if (loading) {
    return (
      <div className="farm-visualizer">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Generating your farm layout...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="farm-visualizer">
        <div className="error-container">
          <h2>Error Loading Layout</h2>
          <p>{error}</p>
          <button className="retry-button" onClick={retry}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!layoutData || !layoutData.layout) {
    return (
      <div className="farm-visualizer">
        <div className="no-layout-container">
          <h2>No Layout Available</h2>
          <p>Unable to generate a mixed cropping layout for this crop.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="farm-visualizer">
      <header className="visualizer-header">
        <h1>Mixed Cropping Farm Layout</h1>
        <div className="layout-info">
          <p>Main Crop: <strong>{layoutData.main_crop}</strong></p>
          <p>Land Size: <strong>{landSize} acres</strong></p>
        </div>
      </header>

      <div className="layout-summary">
        <h2>Mixed Crops Distribution</h2>
        <div className="crops-list">
          {layoutData.mixed_crops.map((cropInfo, index) => (
            <div key={index} className="crop-item">
              <span className="crop-name">{cropInfo.crop}</span>
              <span className="crop-percent">{cropInfo.area_percent}%</span>
            </div>
          ))}
        </div>
      </div>

      <div 
        ref={canvasContainerRef} 
        className="canvas-container"
      >
        <FarmCanvas 
          layout={layoutData.layout} 
          mixedCrops={layoutData.mixed_crops}
          containerWidth={containerSize.width}
          containerHeight={containerSize.height}
        />
      </div>

      <div className="layout-details">
        <h3>Layout Pattern: {layoutData.layout.pattern}</h3>
        <p>Dimensions: {layoutData.layout.width}m × {layoutData.layout.height}m</p>
      </div>
    </div>
  );
};

export default FarmVisualizer;