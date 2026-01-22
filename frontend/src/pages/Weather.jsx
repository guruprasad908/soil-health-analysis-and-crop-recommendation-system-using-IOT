import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Line } from 'react-chartjs-2';
import { useTheme } from '../contexts/ThemeContext';
import { useTranslation } from '../hooks/useTranslation';
import '../pages/Weather.css';
import {
  getWeather,
  getWeatherForecast,
  getHistoricalWeather,
  getHistoricalWeatherRange,
  autoDetectLocation
} from '../services/api';
import { villages, districts, villagesByDistrict } from '../data/villages';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

// Simple Error Boundary Component
const ErrorBoundary = ({ children, fallback = null }) => {
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    const handleError = (error) => {
      console.error('Error caught by boundary:', error);
      setHasError(true);
    };

    // Add error listener
    window.addEventListener('error', handleError);
    
    return () => {
      window.removeEventListener('error', handleError);
    };
  }, []);

  if (hasError) {
    return fallback || (
      <div className="card error-card">
        <div className="error-message">
          <h3>Rendering Error</h3>
          <p>There was an error displaying this section. Please try again.</p>
        </div>
      </div>
    );
  }

  return children;
};

// Main Error Boundary for the entire Weather component
const WeatherErrorBoundary = ({ children }) => {
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    const handleError = (error) => {
      console.error('Critical error in Weather component:', error);
      setHasError(true);
    };

    window.addEventListener('error', handleError);
    
    return () => {
      window.removeEventListener('error', handleError);
    };
  }, []);

  if (hasError) {
    return (
      <div className="weather-view">
        <div className="container">
          <div className="card error-card">
            <div className="error-message">
              <h3>Weather Dashboard Error</h3>
              <p>There was a critical error loading the weather dashboard. Please refresh the page or try again later.</p>
              <button onClick={() => window.location.reload()}>Reload Page</button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return children;
};

const geocodeWithFallback = async (query) => {
  console.log('Geocoding query:', query);
  
  // Check if the query is a pincode (6 digits for India)
  const pincodePattern = /^(\d{6})$/;
  const pincodeMatch = query.match(pincodePattern);
  
  if (pincodeMatch) {
    // Handle pincode search
    const pincode = pincodeMatch[1];
    console.log('Detected pincode:', pincode);
    return await searchByPincode(pincode);
  }

  // First try the exact query as provided
  let results = await searchLocation(query);
  if (results && results.length > 0) {
    console.log('Found results for exact query:', results);
    return selectBestResult(results);
  }

  // If that fails, try parsing the query for city and district
  const parsedQuery = parseLocationQuery(query);
  console.log('Parsed query:', parsedQuery);
  
  if (parsedQuery.city && parsedQuery.district) {
    // Try various combinations
    const combinations = [
      `${parsedQuery.city} ${parsedQuery.district}`,
      `${parsedQuery.district} ${parsedQuery.city}`,
      `${parsedQuery.city}, ${parsedQuery.district}`,
      parsedQuery.city,
      parsedQuery.district
    ];
    
    for (const combination of combinations) {
      console.log('Trying combination:', combination);
      results = await searchLocation(combination);
      if (results && results.length > 0) {
        console.log('Found results for combination:', combination, results);
        return selectBestResult(results);
      }
    }
  } else if (parsedQuery.city) {
    // Just try the city if no district was parsed
    console.log('Trying city only:', parsedQuery.city);
    results = await searchLocation(parsedQuery.city);
    if (results && results.length > 0) {
      console.log('Found results for city:', parsedQuery.city, results);
      return selectBestResult(results);
    }
  }

  // Try fuzzy matching for common spelling variations
  const fuzzyQueries = generateFuzzyQueries(query);
  for (const fuzzyQuery of fuzzyQueries) {
    console.log('Trying fuzzy query:', fuzzyQuery);
    results = await searchLocation(fuzzyQuery);
    if (results && results.length > 0) {
      console.log('Found results for fuzzy query:', fuzzyQuery, results);
      return selectBestResult(results);
    }
  }

  // Fallback to OpenWeatherMap API if API key is available
  const apiKey = import.meta.env.VITE_OPENWEATHER_API_KEY;
  if (apiKey) {
    try {
      console.log('Trying OpenWeatherMap API');
      const response = await fetch(
        `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(query)}&limit=1&appid=${apiKey}`
      );

      if (response.ok) {
        const matches = await response.json();
        console.log('OpenWeatherMap results:', matches);
        if (matches && matches.length > 0) {
          return { lat: matches[0].lat, lon: matches[0].lon, name: matches[0].name, country: matches[0].country };
        }
      }
    } catch (error) {
      console.warn('OpenWeatherMap geocoding failed:', error);
    }
  }

  throw new Error('No results for that location. Try a nearby city, town, district, or 6-digit pincode.');
};

// Helper function to search location using Open-Meteo
const searchLocation = async (query) => {
  try {
    const response = await fetch(
      `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=10&language=en`
    );

    if (response.ok) {
      const data = await response.json();
      return data.results || [];
    }
  } catch (error) {
    console.warn('Open-Meteo geocoding failed for query:', query, error);
  }
  return [];
};

// Helper function to search by pincode using a dedicated API
const searchByPincode = async (pincode) => {
  try {
    // Try Postcode API for Indian pincodes
    const response = await fetch(
      `https://api.postalpincode.in/pincode/${pincode}`
    );
    
    if (response.ok) {
      const data = await response.json();
      console.log('Pincode API response:', data);
      
      if (data && data.length > 0 && data[0].Status === 'Success') {
        const postOffices = data[0].PostOffice;
        if (postOffices && postOffices.length > 0) {
          const postOffice = postOffices[0];
          // Get the district or city name to geocode
          const locationName = postOffice.District || postOffice.Block || postOffice.Name;
          const state = postOffice.State;
          
          // Try to geocode the location name
          const locationQuery = `${locationName} ${state}`;
          const results = await searchLocation(locationQuery);
          if (results && results.length > 0) {
            const result = selectBestResult(results);
            if (result) {
              return {
                ...result,
                name: `${postOffice.Name} (${pincode})`,
                pincode: pincode
              };
            }
          }
          
          // Fallback to just the location name
          return {
            lat: postOffice.Latitude || 0,
            lon: postOffice.Longitude || 0,
            name: `${postOffice.Name} (${pincode})`,
            country: 'India',
            pincode: pincode
          };
        }
      }
    }
  } catch (error) {
    console.warn('Pincode search failed:', error);
  }
  
  throw new Error(`No results found for pincode ${pincode}. Please verify the pincode.`);
};

// Helper function to select the best result (prefer India locations)
const selectBestResult = (results) => {
  if (!results || results.length === 0) return null;
  
  // Try to find Indian locations first
  const indiaResult = results.find(result => result.country_code === 'IN');
  const result = indiaResult || results[0];
  
  return { 
    lat: result.latitude, 
    lon: result.longitude, 
    name: result.name || 'Unknown Location', 
    country: result.country || result.admin1 || result.admin2 || 'Unknown' 
  };
};

// Helper function to parse location query for city and district
const parseLocationQuery = (query) => {
  // Common patterns for city, district combinations
  const patterns = [
    /(.+?)\s*,\s*(.+)/,           // city, district
    /(.+?)\s+(district|taluka|taluk|tehsil)\s+(.+)/i, // city district districtname
    /(.+?)\s+(.+)/,               // city district
    /(district|taluka|taluk|tehsil)\s+(.+)/i,         // district districtname
  ];
  
  for (const pattern of patterns) {
    const match = query.match(pattern);
    if (match) {
      if (pattern.toString().includes('(district|taluka|taluk|tehsil)') && match.length >= 3) {
        // Handle patterns like "Babaleshwar district Bidar"
        return {
          city: match[1].trim(),
          district: match[3].trim()
        };
      } else if (match.length >= 3) {
        // Handle patterns like "Babaleshwar, Bidar" or "Babaleshwar Bidar"
        return {
          city: match[1].trim(),
          district: match[2].trim()
        };
      } else if (match.length >= 2) {
        // Handle patterns like "district Bidar"
        return {
          city: '',
          district: match[2].trim()
        };
      }
    }
  }
  
  // If no pattern matches, treat the whole query as a city
  return {
    city: query.trim(),
    district: ''
  };
};

// Helper function to generate fuzzy queries for common spelling variations
const generateFuzzyQueries = (query) => {
  const queries = [query];
  
  // Common spelling variations
  const variations = {
    'aleshwar': 'aleshwar',
    'alesh': 'alesh',
    'leshwar': 'leshwar',
    'lesh': 'lesh',
    'baba': 'baba'
  };
  
  // Generate variations
  let fuzzyQuery = query;
  Object.keys(variations).forEach(key => {
    if (fuzzyQuery.includes(key)) {
      const value = variations[key];
      queries.push(fuzzyQuery.replace(key, value));
    }
  });
  
  // Try removing common suffixes
  if (query.endsWith('pur') || query.endsWith('garh') || query.endsWith('bad')) {
    queries.push(query.slice(0, -3));
  }
  
  return queries;
};

const Weather = () => {
  const { theme } = useTheme();
  const { t } = useTranslation();
  const [location, setLocation] = useState('');
  const [placeMeta, setPlaceMeta] = useState(null);
  const [current, setCurrent] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [historical, setHistorical] = useState(null);
  const [historicalRange, setHistoricalRange] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showHistory, setShowHistory] = useState(false);
  const [historyMethod, setHistoryMethod] = useState('range'); // 'single' or 'range'
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [daysRange, setDaysRange] = useState(7);
  const [showCharts, setShowCharts] = useState(false); // New state for charts
  const [activeFeature, setActiveFeature] = useState(''); // Track active feature
  // State for village selector
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const [selectedVillage, setSelectedVillage] = useState('');

  // Set default dates to past dates
  useEffect(() => {
    try {
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const weekAgo = new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);
      
      const endDateStr = yesterday.toISOString().split('T')[0];
      const startDateStr = weekAgo.toISOString().split('T')[0];
      
      setEndDate(endDateStr);
      setStartDate(startDateStr);
    } catch (err) {
      console.error('Error setting default dates:', err);
    }
  }, []);

  // Chart color configuration based on theme
  const chartColors = useMemo(() => {
    try {
      if (theme === 'dark') {
        return {
          temperature: {
            primary: 'rgba(255, 99, 132, 0.8)',
            secondary: 'rgba(255, 99, 132, 0.5)',
            border: 'rgba(255, 99, 132, 1)'
          },
          humidity: {
            primary: 'rgba(54, 162, 235, 0.8)',
            secondary: 'rgba(54, 162, 235, 0.5)',
            border: 'rgba(54, 162, 235, 1)'
          },
          rainfall: {
            primary: 'rgba(75, 192, 192, 0.8)',
            secondary: 'rgba(75, 192, 192, 0.5)',
            border: 'rgba(75, 192, 192, 1)'
          },
          wind: {
            primary: 'rgba(153, 102, 255, 0.8)',
            secondary: 'rgba(153, 102, 255, 0.5)',
            border: 'rgba(153, 102, 255, 1)'
          },
          text: '#f4fff9',
          grid: 'rgba(123, 216, 143, 0.2)',
          background: 'rgba(18, 53, 36, 0.95)'
        };
      } else {
        return {
          temperature: {
            primary: 'rgba(220, 53, 69, 0.8)',
            secondary: 'rgba(220, 53, 69, 0.5)',
            border: 'rgba(220, 53, 69, 1)'
          },
          humidity: {
            primary: 'rgba(33, 110, 180, 0.8)',
            secondary: 'rgba(33, 110, 180, 0.5)',
            border: 'rgba(33, 110, 180, 1)'
          },
          rainfall: {
            primary: 'rgba(40, 167, 69, 0.8)',
            secondary: 'rgba(40, 167, 69, 0.5)',
            border: 'rgba(40, 167, 69, 1)'
          },
          wind: {
            primary: 'rgba(111, 66, 193, 0.8)',
            secondary: 'rgba(111, 66, 193, 0.5)',
            border: 'rgba(111, 66, 193, 1)'
          },
          text: '#164025',
          grid: 'rgba(45, 138, 72, 0.2)',
          background: 'rgba(255, 255, 255, 0.92)'
        };
      }
    } catch (err) {
      console.error('Error setting chart colors:', err);
      // Return default colors
      return {
        temperature: {
          primary: 'rgba(220, 53, 69, 0.8)',
          secondary: 'rgba(220, 53, 69, 0.5)',
          border: 'rgba(220, 53, 69, 1)'
        },
        humidity: {
          primary: 'rgba(33, 110, 180, 0.8)',
          secondary: 'rgba(33, 110, 180, 0.5)',
          border: 'rgba(33, 110, 180, 1)'
        },
        rainfall: {
          primary: 'rgba(40, 167, 69, 0.8)',
          secondary: 'rgba(40, 167, 69, 0.5)',
          border: 'rgba(40, 167, 69, 1)'
        },
        wind: {
          primary: 'rgba(111, 66, 193, 0.8)',
          secondary: 'rgba(111, 66, 193, 0.5)',
          border: 'rgba(111, 66, 193, 1)'
        },
        text: '#164025',
        grid: 'rgba(45, 138, 72, 0.2)',
        background: 'rgba(255, 255, 255, 0.92)'
      };
    }
  }, [theme]);

  const handleLookup = async (type) => {
    if (!location.trim()) {
      setError('Please enter a village, district, or coordinates.');
      return;
    }

    setLoading(true);
    setError('');
    setActiveFeature(type); // Set the active feature
    setShowHistory(false); // Hide historical input when switching to other features

    try {
      const { lat, lon, name, country } = await geocodeWithFallback(location.trim());
      console.log('Geocoded location:', { lat, lon, name, country });
      setPlaceMeta({ name: name || 'Unknown', country: country || '' });

      if (type === 'current') {
        const data = await getWeather(lat, lon);
        if (data.error) {
          throw new Error(data.error);
        }
        setCurrent(data);
        setForecast(null);
        setHistorical(null);
        setHistoricalRange(null);
      } else if (type === 'forecast') {
        const data = await getWeatherForecast(lat, lon);
        console.log('Forecast data received:', data);
        if (data.error) {
          throw new Error(data.error);
        }
        // Ensure location data is properly set
        const locationName = data.location || name || 'Unknown Location';
        const countryName = data.country || country || '';
        
        const forecastData = {
          ...data,
          location: locationName,
          country: countryName
        };
        
        console.log('Setting forecast data with location:', forecastData);
        setForecast(forecastData);
        setCurrent(null);
        setHistorical(null);
        setHistoricalRange(null);
      } else if (type === 'rainfall-trend') {
        // Fetch 2 years of historical rainfall data
        const endDate = new Date();
        endDate.setDate(endDate.getDate() - 1); // Yesterday
        const startDate = new Date();
        startDate.setFullYear(startDate.getFullYear() - 2); // 2 years ago
        
        const startStr = startDate.toISOString().split('T')[0];
        const endStr = endDate.toISOString().split('T')[0];
        
        console.log('Fetching rainfall trend data for:', lat, lon, startStr, endStr);
        const data = await getHistoricalWeatherRange(lat, lon, null, startStr, endStr);
        console.log('Received rainfall trend raw data:', JSON.stringify(data, null, 2));
        
        if (data.error) {
          throw new Error(data.error);
        }
        
        // Process data for rainfall trends
        const processedData = processRainfallTrendData(data);
        console.log('Processed rainfall trend data:', JSON.stringify(processedData, null, 2));
        
        setHistoricalRange(processedData);
        setCurrent(null);
        setForecast(null);
        setHistorical(null);
      }
    } catch (err) {
      console.error('Error in handleLookup:', err);
      setError(err.message || 'Unable to fetch weather information right now. Please try a nearby city, town, district, or 6-digit pincode.');
      setCurrent(null);
      setForecast(null);
      setHistorical(null);
      setHistoricalRange(null);
    } finally {
      setLoading(false);
    }
  };

  // Process rainfall trend data to calculate trends over 2 years
  const processRainfallTrendData = (data) => {
    try {
      console.log('Starting to process rainfall data:', data);
      
      if (!data) {
        console.warn('No data provided to processRainfallTrendData');
        return null;
      }
      
      if (!data.data) {
        console.warn('No data.data provided to processRainfallTrendData');
        return data;
      }
      
      console.log('Processing rainfall data with', data.data.length, 'records');
      
      // Group data by month and year for trend analysis
      const monthlyData = {};
      const yearlyData = {};
      
      data.data.forEach((day, index) => {
        try {
          if (!day || !day.date) {
            console.warn('Skipping invalid day data at index', index, day);
            return;
          }
          
          const date = new Date(day.date);
          if (isNaN(date.getTime())) {
            console.warn('Invalid date in day data:', day.date);
            return;
          }
          
          const monthYear = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
          const year = date.getFullYear();
          
          // Monthly aggregation
          if (!monthlyData[monthYear]) {
            monthlyData[monthYear] = {
              totalRainfall: 0,
              count: 0,
              year: year,
              month: date.getMonth() + 1
            };
          }
          // Use simple logical OR fallback for rainfall data as per specification
          const rainfall = day.rain || day.precipitation || 0;
          monthlyData[monthYear].totalRainfall += rainfall;
          monthlyData[monthYear].count++;
          
          // Yearly aggregation
          if (!yearlyData[year]) {
            yearlyData[year] = {
              totalRainfall: 0,
              count: 0
            };
          }
          yearlyData[year].totalRainfall += rainfall;
          yearlyData[year].count++;
        } catch (dayError) {
          console.error('Error processing day at index', index, day, dayError);
        }
      });
      
      console.log('Monthly data groups:', Object.keys(monthlyData).length);
      console.log('Yearly data groups:', Object.keys(yearlyData).length);
      
      // Calculate averages
      const monthlyAverages = Object.keys(monthlyData).map(key => ({
        monthYear: key,
        averageRainfall: monthlyData[key].totalRainfall / monthlyData[key].count,
        totalRainfall: monthlyData[key].totalRainfall,
        year: monthlyData[key].year,
        month: monthlyData[key].month
      }));
      
      const yearlyAverages = Object.keys(yearlyData).map(key => ({
        year: parseInt(key),
        averageRainfall: yearlyData[key].totalRainfall / yearlyData[key].count,
        totalRainfall: yearlyData[key].totalRainfall
      }));
      
      console.log('Monthly averages:', monthlyAverages.length);
      console.log('Yearly averages:', yearlyAverages.length);
      
      // Add trend analysis to the data
      const trendAnalysis = calculateRainfallTrends(monthlyAverages);
      console.log('Trend analysis:', trendAnalysis);
      
      const result = {
        ...data,
        monthlyAverages: monthlyAverages || [],
        yearlyAverages: yearlyAverages || [],
        trendAnalysis: trendAnalysis || null
      };
      
      console.log('Final processed data:', result);
      return result;
    } catch (error) {
      console.error('Error processing rainfall trend data:', error);
      return data || null;
    }
  };

  // Calculate rainfall trends
  const calculateRainfallTrends = (monthlyData) => {
    try {
      console.log('Calculating trends with monthly data:', monthlyData);
      
      if (!monthlyData || monthlyData.length < 2) {
        console.warn('Insufficient data for trend calculation:', monthlyData?.length);
        return null;
      }
      
      console.log('Calculating trends with', monthlyData.length, 'monthly data points');
      
      // Calculate overall trend
      const firstHalf = monthlyData.slice(0, Math.floor(monthlyData.length / 2));
      const secondHalf = monthlyData.slice(Math.floor(monthlyData.length / 2));
      
      const firstAvg = firstHalf.reduce((sum, month) => sum + (month.averageRainfall || 0), 0) / (firstHalf.length || 1);
      const secondAvg = secondHalf.reduce((sum, month) => sum + (month.averageRainfall || 0), 0) / (secondHalf.length || 1);
      
      const overallTrend = secondAvg - firstAvg;
      
      // Calculate seasonal trends (last 12 months vs previous 12 months)
      const recentData = monthlyData.slice(-12);
      const previousData = monthlyData.slice(-24, -12);
      
      const recentAvg = recentData.length > 0 
        ? recentData.reduce((sum, month) => sum + (month.averageRainfall || 0), 0) / recentData.length 
        : 0;
      const previousAvg = previousData.length > 0 
        ? previousData.reduce((sum, month) => sum + (month.averageRainfall || 0), 0) / previousData.length 
        : 0;
      
      const seasonalTrend = recentAvg - previousAvg;
      
      return {
        overallTrend,
        seasonalTrend,
        trendDirection: overallTrend > 0 ? 'increasing' : overallTrend < 0 ? 'decreasing' : 'stable',
        seasonalDirection: seasonalTrend > 0 ? 'increasing' : seasonalTrend < 0 ? 'decreasing' : 'stable',
        recentAverage: recentAvg,
        previousAverage: previousAvg
      };
    } catch (error) {
      console.error('Error calculating rainfall trends:', error);
      return null;
    }
  };

  const handleHistoricalLookup = async () => {
    if (!location.trim()) {
      setError('Please enter a village, district, or coordinates.');
      return;
    }

    if (!startDate || !endDate) {
      setError('Please select both start and end dates.');
      return;
    }

    setLoading(true);
    setError('');
    setActiveFeature('historical'); // Set the active feature

    try {
      const { lat, lon, name, country } = await geocodeWithFallback(location.trim());
      console.log('Geocoded location:', { lat, lon, name, country });
      setPlaceMeta({ name: name || 'Unknown', country: country || '' });

      // Use free Open-Meteo API for date range historical data
      let start = startDate;
      let end = endDate;
      
      // Validate that dates are not in the future
      const today = new Date().toISOString().split('T')[0];
      if (start > today || end > today) {
        throw new Error('Historical weather data is only available for past dates. Please select dates before today.');
      }
      
      // Validate that start date is before end date
      if (start > end) {
        throw new Error('Start date must be before end date.');
      }
      
      const data = await getHistoricalWeatherRange(lat, lon, null, start, end);
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      setHistoricalRange(data);
      setHistorical(null);
      setCurrent(null);
      setForecast(null);
    } catch (err) {
      setError(err.message || 'Unable to fetch historical weather information right now. Please try a nearby city, district, or state.');
    } finally {
      setLoading(false);
    }
  };

  const renderCurrentWeather = () => {
    if (!current) return null;

    return (
      <section className="card current-card">
        <div className="section-heading">
          <h2>{t('weather.liveWeather')}</h2>
          {placeMeta && (
            <p className="section-subtitle">
              {placeMeta.name}
              {placeMeta.country ? `, ${placeMeta.country}` : ''}
            </p>
          )}
        </div>

        <div className="current-grid">
          <div className="highlight">
            <span className="badge">Temperature</span>
            <div className="temp-value">{current.temperature?.toFixed?.(1) ?? current.temperature}°C</div>
            <p className="description">{current.weather ?? 'No description available'}</p>
          </div>

          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-label">Humidity</div>
              <div className="metric-value">{current.humidity}%</div>
              <div className="metric-note">Ideal range 50-80%</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Wind Speed</div>
              <div className="metric-value">{current.wind_speed?.toFixed?.(1) ?? current.wind_speed} m/s</div>
              <div className="metric-note">Direction {current.wind_direction || 0}°</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Rainfall (1h)</div>
              <div className="metric-value">{current.rain_1h ?? 0} mm</div>
              <div className="metric-note">3h total {current.rain_3h ?? 0} mm</div>
            </div>
          </div>
        </div>

        <div className="advice-strip">
          <div>
            <h3>Field Advisory</h3>
            <p>
              Combine rainfall and humidity to calibrate irrigation. Rainfall above 5 mm in the last hour signals a
              good window to pause irrigation and focus on drainage.
            </p>
          </div>
        </div>
      </section>
    );
  };

  const renderForecast = () => {
    if (!forecast) return null;

    const daily = forecast.forecast ?? [];
    const detailed = forecast.detailed ?? [];

    console.log('Rendering forecast data:', forecast);
    console.log('Location data - location:', forecast.location, 'country:', forecast.country);
    console.log('Daily forecast data:', daily);
    console.log('Detailed forecast data:', detailed);

    return (
      <section className="card forecast-card">
        <div className="section-heading">
          <h2>{t('weather.forecast')}</h2>
          <p className="section-subtitle">
            {forecast.location && forecast.location !== 'Unknown' && forecast.location.trim() !== '' ? forecast.location : 'Unknown Location'}
            {forecast.country && forecast.country.trim() !== '' ? `, ${forecast.country}` : ''}
          </p>
        </div>

        <div className="forecast-grid">
          {daily && daily.length > 0 ? (
            daily.map((day) => (
              <article className="forecast-item" key={day.date}>
                <span className="forecast-date">{day.date ? new Date(day.date).toLocaleDateString() : 'N/A'}</span>
                <div className="forecast-temp">
                  <strong>{typeof day.max_temp === 'number' ? day.max_temp.toFixed(1) : 'N/A'}°C</strong>
                  <span>{typeof day.min_temp === 'number' ? day.min_temp.toFixed(1) : 'N/A'}°C</span>
                </div>
                <p className="forecast-note">Avg humidity {typeof day.avg_humidity === 'number' ? day.avg_humidity.toFixed(0) : 'N/A'}%</p>
                <div className="rain-block">
                  <span>Total {typeof day.total_rainfall === 'number' ? day.total_rainfall.toFixed(1) : 0} mm</span>
                  <span>Chance {typeof day.max_rainfall_probability === 'number' ? day.max_rainfall_probability.toFixed(0) : 0}%</span>
                </div>
                <span className="conditions">{day.conditions || 'Unknown'}</span>
              </article>
            ))
          ) : (
            <p>No forecast data available</p>
          )}
        </div>

        {detailed && detailed.length > 0 && (
          <div className="hourly-panel">
            <h3>Next 24 Hours (3-hour slices)</h3>
            <div className="hourly-grid">
              {detailed.slice(0, 8).map((slot, index) => (
                <div className="hourly-card" key={index}>
                  <span className="hourly-time">{slot.datetime ? new Date(slot.datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'N/A'}</span>
                  <div className="hourly-temp">{slot.temperature?.toFixed(1) ?? 'N/A'}°C</div>
                  <div className="hourly-rain">{slot.rain?.toFixed?.(1) ?? 0} mm</div>
                  <div className="hourly-probability">{slot.rainfall_probability?.toFixed?.(0) ?? 0}% chance</div>
                  <div className="hourly-conditions">{slot.weather ?? 'N/A'}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </section>
    );
  };

  const renderHistoricalWeather = () => {
    if (!historical) return null;

    return (
      <section className="card historical-card">
        <div className="section-heading">
          <h2>{t('weather.historicalData')}</h2>
          <p className="section-subtitle">
            {historical.location}
            {historical.country ? `, ${historical.country}` : ''}
          </p>
        </div>

        <div className="current-grid">
          <div className="highlight">
            <span className="badge">Historical Date</span>
            <div className="temp-value">{new Date(historical.date).toLocaleDateString()}</div>
            <p className="description">{historical.weather ?? 'No description available'}</p>
          </div>

          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-label">Temperature</div>
              <div className="metric-value">{historical.temperature?.toFixed?.(1) ?? historical.temperature}°C</div>
              <div className="metric-note">Min: {historical.min_temp?.toFixed?.(1) ?? 'N/A'}°C | Max: {historical.max_temp?.toFixed?.(1) ?? 'N/A'}°C</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Humidity</div>
              <div className="metric-value">{historical.humidity ?? 'N/A'}%</div>
              <div className="metric-note">Current reading</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Rainfall</div>
              <div className="metric-value">{historical.rain ?? 0} mm</div>
              <div className="metric-note">Precipitation: {historical.precipitation ?? 0}mm</div>
            </div>
          </div>
        </div>
      </section>
    );
  };

  const renderHistoricalRange = () => {
    if (!historicalRange) return null;

    const tempChart = generateTemperatureChart;
    const humidityChart = generateHumidityChart;
    const rainfallChart = generateRainfallChart;
    const comparativeChart = generateComparativeChart;

    return (
      <section className="card historical-range-card">
        <div className="section-heading">
          <h2>📊 {t('weather.historicalData')}</h2>
          {historicalRange.location && (
            <p className="section-subtitle">
              {historicalRange.location}
              {historicalRange.country ? `, ${historicalRange.country}` : ''}
            </p>
          )}
          <button 
            className="toggle-charts-btn" 
            onClick={() => setShowCharts(!showCharts)}
          >
            {showCharts ? 'Hide Charts' : 'Show Charts'}
          </button>
        </div>

        {showCharts && (
          <div className="charts-container">
            <div className="chart-grid">
              {tempChart && (
                <div className="chart-wrapper">
                  <h3>Temperature Trends</h3>
                  <div className="chart-container">
                    <Line key={`temp-${theme}`} data={tempChart} options={lineChartOptions} />
                  </div>
                </div>
              )}
              
              {humidityChart && (
                <div className="chart-wrapper">
                  <h3>Humidity Trends</h3>
                  <div className="chart-container">
                    <Line key={`humidity-${theme}`} data={humidityChart} options={lineChartOptions} />
                  </div>
                </div>
              )}
              
              {rainfallChart && (
                <div className="chart-wrapper">
                  <h3>Rainfall Patterns</h3>
                  <div className="chart-container">
                    <Line key={`rainfall-${theme}`} data={rainfallChart} options={lineChartOptions} />
                  </div>
                </div>
              )}
              
              {comparativeChart && (
                <div className="chart-wrapper">
                  <h3>Temperature vs Humidity</h3>
                  <div className="chart-container">
                    <Line key={`comparative-${theme}`} data={comparativeChart} options={comparativeChartOptions} />
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="historical-data-grid">
          <div className="metric-summary">
            <div className="metric-card">
              <div className="metric-label">Average Temperature</div>
              <div className="metric-value">
                {historicalRange.data?.length ? 
                  (historicalRange.data.reduce((sum, day) => sum + (day.temperature || day.temp || 0), 0) / historicalRange.data.length).toFixed(1) : 
                  'N/A'}°C
              </div>
              <div className="metric-note">{historicalRange.data?.length || 0} days</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Average Rainfall</div>
              <div className="metric-value">
                {historicalRange.data?.length ? 
                  (historicalRange.data.reduce((sum, day) => sum + (day.rain || day.precipitation || 0), 0) / historicalRange.data.length).toFixed(1) : 
                  'N/A'}mm
              </div>
              <div className="metric-note">Per day</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Total Rainfall</div>
              <div className="metric-value">
                {historicalRange.data?.length ? 
                  (historicalRange.data.reduce((sum, day) => sum + (day.rain || day.precipitation || 0), 0)).toFixed(1) : 
                  'N/A'}mm
              </div>
              <div className="metric-note">{historicalRange.data?.length || 0} days</div>
            </div>
          </div>

          <div className="daily-data-table">
            <h3>
              Daily Weather Data
              {historicalRange.data?.length > 0 && (
                <span className="table-subtitle">
                  ({historicalRange.data.length} days)
                </span>
              )}
            </h3>
            <div className="table-info">
              <p>Showing first 10 days of data. Calculations are based on all {historicalRange.data?.length || 0} days in the selected period.</p>
            </div>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Temp (°C)</th>
                    <th>Rainfall (mm)</th>
                    <th>Weather</th>
                  </tr>
                </thead>
                <tbody>
                  {historicalRange.data?.slice(0, 10).map((day, index) => (
                    <tr key={index}>
                      <td>{day.date || day.time}</td>
                      <td>{(day.temperature || day.temp || 0).toFixed(1)}</td>
                      <td>{(day.rain || day.precipitation || 0).toFixed(1)}</td>
                      <td>{day.weather || (day.rain > 0 || day.precipitation > 0 ? 'Rainy' : 'Clear') || 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {historicalRange.data?.length > 10 && (
              <div className="table-note">
                <p>Showing first 10 of {historicalRange.data.length} records. Scroll horizontally to see more data, or use a smaller date range for detailed view.</p>
              </div>
            )}
          </div>
        </div>
      </section>
    );
  };

  // Generate chart data for monthly averages - moved outside render function
  const monthlyChartData = useMemo(() => {
    try {
      console.log('Generating monthly chart data with historicalRange:', historicalRange);
      
      if (!historicalRange || !historicalRange.monthlyAverages || historicalRange.monthlyAverages.length === 0) {
        console.log('No monthly averages data available');
        return null;
      }
      
      const { monthlyAverages } = historicalRange;
      
      // Take last 24 months for the chart
      const last24Months = monthlyAverages.slice(-24);
      console.log('Last 24 months data:', last24Months);
      
      const labels = last24Months.map(item => {
        try {
          if (!item || !item.year || !item.month) {
            console.warn('Invalid item for date formatting:', item);
            return item.monthYear || 'Unknown';
          }
          const date = new Date(item.year, item.month - 1);
          return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
        } catch (e) {
          console.warn('Error formatting date for item:', item, e);
          return item.monthYear || 'Unknown';
        }
      });
      
      console.log('Chart labels:', labels);
      
      const data = last24Months.map(item => {
        if (!item) return 0;
        const value = item.averageRainfall || 0;
        return isNaN(value) ? 0 : value;
      });
      
      console.log('Chart data values:', data);
      
      return {
        labels,
        datasets: [
          {
            label: 'Monthly Average Rainfall (mm)',
            data,
            borderColor: chartColors.rainfall?.border || 'rgba(75, 192, 192, 1)',
            backgroundColor: chartColors.rainfall?.secondary || 'rgba(75, 192, 192, 0.5)',
            tension: 0.4,
            fill: true
          }
        ]
      };
    } catch (error) {
      console.error('Error generating monthly chart data:', error);
      return null;
    }
  }, [historicalRange, chartColors]);

  // Generate chart data for yearly averages - moved outside render function
  const yearlyChartData = useMemo(() => {
    try {
      console.log('Generating yearly chart data with historicalRange:', historicalRange);
      
      if (!historicalRange || !historicalRange.yearlyAverages || historicalRange.yearlyAverages.length === 0) {
        console.log('No yearly averages data available');
        return null;
      }
      
      const { yearlyAverages } = historicalRange;
      
      const labels = yearlyAverages.map(item => {
        if (!item) return 'Unknown';
        return item.year || 'Unknown';
      });
      
      console.log('Yearly chart labels:', labels);
      
      const data = yearlyAverages.map(item => {
        if (!item) return 0;
        const value = item.averageRainfall || 0;
        return isNaN(value) ? 0 : value;
      });
      
      console.log('Yearly chart data values:', data);
      
      return {
        labels,
        datasets: [
          {
            label: 'Yearly Average Rainfall (mm)',
            data,
            borderColor: chartColors.temperature?.border || 'rgba(220, 53, 69, 1)',
            backgroundColor: chartColors.temperature?.secondary || 'rgba(220, 53, 69, 0.5)',
            tension: 0.4,
            fill: true
          }
        ]
      };
    } catch (error) {
      console.error('Error generating yearly chart data:', error);
      return null;
    }
  }, [historicalRange, chartColors]);

  const renderRainfallTrend = () => {
    try {
      console.log('Starting to render rainfall trend with data:', historicalRange);
      
      if (!historicalRange) {
        console.log('No historicalRange data to render');
        return (
          <section className="card">
            <div className="no-data">
              <h3>Rainfall Trend Data</h3>
              <p>No data available to display.</p>
            </div>
          </section>
        );
      }
      
      const { trendAnalysis, monthlyAverages, yearlyAverages } = historicalRange;
      console.log('Data breakdown - trendAnalysis:', trendAnalysis, 'monthlyAverages:', monthlyAverages, 'yearlyAverages:', yearlyAverages);
      
      console.log('Using pre-generated monthly chart data:', monthlyChartData);
      console.log('Using pre-generated yearly chart data:', yearlyChartData);

      return (
        <section className="card historical-range-card">
          <div className="section-heading">
            <h2>🌧 {t('weather.rainfallTrend')}</h2>
            {historicalRange.location && (
              <p className="section-subtitle">
                {historicalRange.location}
                {historicalRange.country ? `, ${historicalRange.country}` : ''}
              </p>
            )}
          </div>
          
          {trendAnalysis && (
            <div className="trend-summary">
              <div className="metrics-grid">
                <div className="metric-card">
                  <div className="metric-label">Overall Trend</div>
                  <div className="metric-value">
                    {trendAnalysis.overallTrend > 0 ? '↗' : trendAnalysis.overallTrend < 0 ? '↘' : '→'} 
                    {Math.abs(trendAnalysis.overallTrend || 0).toFixed(1)}mm
                  </div>
                  <div className="metric-note">
                    {trendAnalysis.trendDirection === 'increasing' ? 'Increasing' : 
                     trendAnalysis.trendDirection === 'decreasing' ? 'Decreasing' : 'Stable'}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Seasonal Trend</div>
                  <div className="metric-value">
                    {trendAnalysis.seasonalTrend > 0 ? '↗' : trendAnalysis.seasonalTrend < 0 ? '↘' : '→'} 
                    {Math.abs(trendAnalysis.seasonalTrend || 0).toFixed(1)}mm
                  </div>
                  <div className="metric-note">
                    {trendAnalysis.seasonalDirection === 'increasing' ? 'Increasing' : 
                     trendAnalysis.seasonalDirection === 'decreasing' ? 'Decreasing' : 'Stable'}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Recent Average</div>
                  <div className="metric-value">{(trendAnalysis.recentAverage || 0).toFixed(1)}mm</div>
                  <div className="metric-note">Last 12 months</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Previous Average</div>
                  <div className="metric-value">{(trendAnalysis.previousAverage || 0).toFixed(1)}mm</div>
                  <div className="metric-note">Previous 12 months</div>
                </div>
              </div>
            </div>
          )}
          
          <div className="charts-container">
            <div className="chart-grid">
              {monthlyChartData && (
                <div className="chart-wrapper">
                  <h3>Monthly Rainfall Trends (Last 24 Months)</h3>
                  <div className="chart-container">
                    <ErrorBoundary fallback={<div className="chart-error">Error loading monthly chart</div>}>
                      <Line key={`monthly-rainfall-${theme}`} data={monthlyChartData} options={lineChartOptions} />
                    </ErrorBoundary>
                  </div>
                </div>
              )}
              
              {yearlyChartData && (
                <div className="chart-wrapper">
                  <h3>Yearly Rainfall Trends</h3>
                  <div className="chart-container">
                    <ErrorBoundary fallback={<div className="chart-error">Error loading yearly chart</div>}>
                      <Line key={`yearly-rainfall-${theme}`} data={yearlyChartData} options={lineChartOptions} />
                    </ErrorBoundary>
                  </div>
                </div>
              )}
            </div>
          </div>
          
          <div className="historical-data-grid">
            <div className="daily-data-table">
              <h3>
                Monthly Rainfall Summary
                {monthlyAverages?.length > 0 && (
                  <span className="table-subtitle">
                    ({monthlyAverages.length} months)
                  </span>
                )}
              </h3>
              <div className="table-container">
                <table>
                  <thead>
                    <tr>
                      <th>Month-Year</th>
                      <th>Avg Rainfall (mm)</th>
                      <th>Total Rainfall (mm)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {monthlyAverages?.slice(-10).map((item, index) => (
                      <tr key={index}>
                        <td>{item?.monthYear || 'Unknown'}</td>
                        <td>{(item?.averageRainfall || 0).toFixed(1)}</td>
                        <td>{(item?.totalRainfall || 0).toFixed(1)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {monthlyAverages?.length > 10 && (
                <div className="table-note">
                  <p>Showing last 10 of {monthlyAverages?.length || 0} months. Scroll horizontally to see more data.</p>
                </div>
              )}
            </div>
          </div>
        </section>
      );
    } catch (error) {
      console.error('Error rendering rainfall trend:', error);
      return (
        <section className="card error-card">
          <div className="error-message">
            <h3>Rainfall Trend Error</h3>
            <p>There was an error displaying the rainfall trend data. Please try again.</p>
            <button 
              className="btn-primary" 
              onClick={() => handleLookup('rainfall-trend')}
              style={{ marginTop: '1rem' }}
            >
              Retry
            </button>
            <details style={{marginTop: '10px', fontSize: '0.8em'}}>
              <summary>Error details</summary>
              <pre>{error.message}</pre>
            </details>
          </div>
        </section>
      );
    }
  };

  // Generate temperature trend chart data
  const generateTemperatureChart = useMemo(() => {
    if (!historicalRange || !historicalRange.data) return null;
    
    const dates = historicalRange.data.map(day => day.date || day.time);
    const temperatures = historicalRange.data.map(day => day.temperature || day.temp || 0);
    
    return {
      labels: dates,
      datasets: [
        {
          label: 'Average Temperature (°C)',
          data: temperatures,
          borderColor: chartColors.temperature.border,
          backgroundColor: chartColors.temperature.secondary,
          tension: 0.4,
          fill: true
        }
      ]
    };
  }, [historicalRange, chartColors]);

  // Generate humidity trend chart data
  const generateHumidityChart = useMemo(() => {
    if (!historicalRange || !historicalRange.data) return null;
    
    const dates = historicalRange.data.map(day => day.date || day.time);
    const humidity = historicalRange.data.map(day => day.humidity || 0);
    
    // If no humidity data (Open-Meteo free tier), show a message instead
    if (humidity.every(h => h === 0)) {
      return null;
    }
    
    return {
      labels: dates,
      datasets: [
        {
          label: 'Average Humidity (%)',
          data: humidity,
          borderColor: chartColors.humidity.border,
          backgroundColor: chartColors.humidity.secondary,
          tension: 0.4,
          fill: true
        }
      ]
    };
  }, [historicalRange, chartColors]);

  // Generate rainfall trend chart data
  const generateRainfallChart = useMemo(() => {
    if (!historicalRange || !historicalRange.data) return null;
    
    const dates = historicalRange.data.map(day => day.date || day.time);
    const rainfall = historicalRange.data.map(day => day.rain || day.precipitation || 0);
    
    // If all rainfall values are 0, return null to avoid displaying an empty chart
    if (rainfall.every(r => r === 0)) {
      return null;
    }
    
    return {
      labels: dates,
      datasets: [
        {
          label: 'Daily Rainfall (mm)',
          data: rainfall,
          borderColor: chartColors.rainfall.border,
          backgroundColor: chartColors.rainfall.secondary,
          tension: 0.4,
          fill: true
        }
      ]
    };
  }, [historicalRange, chartColors]);

  // Generate comparative weather chart
  const generateComparativeChart = useMemo(() => {
    if (!historicalRange || !historicalRange.data) return null;
    
    const dates = historicalRange.data.map(day => day.date || day.time);
    const temperatures = historicalRange.data.map(day => day.temperature || day.temp || 0);
    const humidity = historicalRange.data.map(day => day.humidity || 0);
    
    // If no humidity data (Open-Meteo free tier), only show temperature
    if (humidity.every(h => h === 0)) {
      return {
        labels: dates,
        datasets: [
          {
            label: 'Temperature (°C)',
            data: temperatures,
            borderColor: chartColors.temperature.border,
            backgroundColor: chartColors.temperature.secondary,
            yAxisID: 'y',
            tension: 0.4
          }
        ]
      };
    }
    
    return {
      labels: dates,
      datasets: [
        {
          label: 'Temperature (°C)',
          data: temperatures,
          borderColor: chartColors.temperature.border,
          backgroundColor: chartColors.temperature.secondary,
          yAxisID: 'y',
          tension: 0.4
        },
        {
          label: 'Humidity (%)',
          data: humidity,
          borderColor: chartColors.humidity.border,
          backgroundColor: chartColors.humidity.secondary,
          yAxisID: 'y1',
          tension: 0.4
        }
      ]
    };
  }, [historicalRange, chartColors]);

  // Chart options with theme support
  const lineChartOptions = useMemo(() => {
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
          text: 'Weather Trends',
          color: chartColors.text,
          font: {
            size: 16,
            weight: 'bold',
          },
        },
      },
      scales: {
        y: {
          beginAtZero: false,
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

  const comparativeChartOptions = useMemo(() => {
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
          text: 'Temperature & Humidity Comparison',
          color: chartColors.text,
          font: {
            size: 16,
            weight: 'bold',
          },
        },
      },
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Temperature (°C)',
            color: chartColors.text,
          },
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
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Humidity (%)',
            color: chartColors.text,
          },
          grid: {
            drawOnChartArea: false,
            color: chartColors.grid,
          },
          ticks: {
            color: chartColors.text,
            font: {
              size: 12,
            },
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

  return (
    <div className="weather-view">
      <div className="container">
        <div className="section-heading">
          <h1>🌦 {t('weather.title')}</h1>
          <p className="section-subtitle">
            Real-time weather, forecasts, and historical patterns to inform your agronomic decisions.
          </p>
        </div>

        <section className="card search-panel">
          <div className="search-form-group">
            <div className="form-group">
              <label htmlFor="location">
                Location
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
                        setLocation(locationData.location);
                        // Reset dropdowns when using GPS
                        setSelectedDistrict('');
                        setSelectedVillage('');
                      } else {
                        setError('Could not detect location. Please enter manually.');
                      }
                    } catch (err) {
                      setError('Location access denied or failed. Please enter location manually.');
                    }
                  }}
                  style={{
                    marginLeft: '8px',
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
                  📍 Use My Location
                </button>
              </label>
              
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
                  <option value="">Select District</option>
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
                          setLocation(`${village.name}, ${village.district}`);
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
                    <option value="">Select Village/City</option>
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
                type="text"
                value={location}
                onChange={(e) => {
                  setLocation(e.target.value);
                  // Reset dropdowns when typing manually
                  if (e.target.value && !e.target.value.includes(selectedVillage)) {
                    setSelectedDistrict('');
                    setSelectedVillage('');
                  }
                }}
                placeholder="Or type manually: e.g., Babaleshwar, Vijayapura"
              />
            </div>
          </div>
          
          <div className="action-buttons">
            <button 
              className={`btn-secondary ${activeFeature === 'current' ? 'active' : ''}`} 
              onClick={() => handleLookup('current')}
            >
              {t('weather.liveWeather')}
            </button>
            <button 
              className={`btn-secondary ${activeFeature === 'forecast' ? 'active' : ''}`} 
              onClick={() => handleLookup('forecast')}
            >
              {t('weather.forecast')}
            </button>
            <button 
              className={`btn-secondary ${activeFeature === 'historical' ? 'active' : ''}`} 
              onClick={() => {
                setShowHistory(!showHistory);
                if (!showHistory) {
                  setActiveFeature('historical');
                  // Clear other states when showing historical input
                  setCurrent(null);
                  setForecast(null);
                  setHistorical(null);
                  setHistoricalRange(null);
                }
              }}
            >
              {t('weather.historicalData')}
            </button>
            <button 
              className={`btn-secondary ${activeFeature === 'rainfall-trend' ? 'active' : ''}`} 
              onClick={() => handleLookup('rainfall-trend')}
              disabled={loading}
            >
              {loading && activeFeature === 'rainfall-trend' ? 'Loading...' : t('weather.rainfallTrend')}
            </button>
          </div>
        </section>

        {error && (
          <section className="card error-card">
            <div className="error-message">
              <h3>Error</h3>
              <p>{error}</p>
            </div>
          </section>
        )}

        {loading && (
          <section className="card loading-card">
            <div className="loading-spinner">
              <div className="spinner"></div>
              <p>Loading weather data...</p>
            </div>
          </section>
        )}

        {!loading && (
          <ErrorBoundary fallback={<div className="card"><p>Error loading weather data. Please try again.</p></div>}>
            <>
              {current && (
                <ErrorBoundary fallback={<div className="card"><p>Error loading current weather data.</p></div>}>
                  {renderCurrentWeather()}
                </ErrorBoundary>
              )}
              {forecast && (
                <ErrorBoundary fallback={<div className="card"><p>Error loading forecast data.</p></div>}>
                  {renderForecast()}
                </ErrorBoundary>
              )}
              {historical && (
                <ErrorBoundary fallback={<div className="card"><p>Error loading historical weather data.</p></div>}>
                  {renderHistoricalWeather()}
                </ErrorBoundary>
              )}
              {historicalRange && activeFeature === 'rainfall-trend' && (
                <ErrorBoundary fallback={<div className="card"><p>Error loading rainfall trend data.</p></div>}>
                  {renderRainfallTrend()}
                </ErrorBoundary>
              )}
              {historicalRange && activeFeature === 'historical' && (
                <ErrorBoundary fallback={<div className="card"><p>Error loading historical range data.</p></div>}>
                  {renderHistoricalRange()}
                </ErrorBoundary>
              )}
              {showHistory && activeFeature === 'historical' && !historical && !historicalRange && (
                <section className="card historical-input-card">
                  <div className="section-heading">
                    <h2>{t('weather.historicalData')}</h2>
                    <p className="section-subtitle">Select a date range to view historical weather data</p>
                  </div>
                  
                  <div className="historical-form">
                    <div className="form-row">
                      <div className="form-group">
                        <label htmlFor="start-date">Start Date</label>
                        <input
                          id="start-date"
                          type="date"
                          value={startDate}
                          onChange={(e) => setStartDate(e.target.value)}
                          max={new Date().toISOString().split('T')[0]}
                        />
                      </div>
                      
                      <div className="form-group">
                        <label htmlFor="end-date">End Date</label>
                        <input
                          id="end-date"
                          type="date"
                          value={endDate}
                          onChange={(e) => setEndDate(e.target.value)}
                          max={new Date().toISOString().split('T')[0]}
                        />
                      </div>
                    </div>
                    
                    <div className="form-actions">
                      <button 
                        className="btn-primary"
                        onClick={handleHistoricalLookup}
                        disabled={loading}
                      >
                        {loading ? 'Loading...' : 'Fetch Historical Data'}
                      </button>
                    </div>
                  </div>
                </section>
              )}
            </>
          </ErrorBoundary>
        )}
      </div>
    </div>
  );
};

export default function WeatherPage() {
  return (
    <WeatherErrorBoundary>
      <Weather />
    </WeatherErrorBoundary>
  );
}
