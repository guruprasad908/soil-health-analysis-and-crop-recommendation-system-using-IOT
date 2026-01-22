# 🌾 Soil Health & Intelligent Crop Recommendation System

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

A comprehensive agricultural decision support system that provides intelligent crop recommendations, fertilizer suggestions, and soil health analysis based on real-time soil data and environmental conditions.

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Environment Setup](#-environment-setup)
- [Installation & Setup](#-installation--setup)
- [API Endpoints](#-api-endpoints)
- [Hardware Integration](#-hardware-integration)
- [Testing & Validation](#-testing--validation)
- [Deployment](#-deployment)
- [Future Improvements](#-future-improvements)
- [License & Contributors](#-license--contributors)

## 🎯 Project Overview

The Soil Health & Intelligent Crop Recommendation System is a cutting-edge agricultural technology solution designed to empower farmers with data-driven insights for optimal crop selection and soil management. This intelligent system integrates multiple data sources and advanced analytics to provide comprehensive agricultural recommendations.

### Key Components

1. **IoT Soil Sensors**: Real-time monitoring of NPK levels, soil moisture, temperature, and humidity
2. **ESP32 Microcontroller**: Wireless data transmission from field sensors to cloud backend
3. **FastAPI Backend**: High-performance REST API for data processing and ML predictions
4. **PostgreSQL Database**: Secure storage of farmer data, predictions, and historical records
5. **React Frontend**: Modern, responsive user interface with multilingual support (English/Kannada)
6. **OpenWeather API**: Real-time weather data integration for accurate predictions
7. **PDF Report Generation**: Professional advisory reports with embedded visualizations
8. **Fertilizer Recommendation Engine**: Crop-specific nutrient management suggestions

### Project Goals

- **Enhance Agricultural Productivity**: Provide precise crop recommendations based on soil conditions
- **Optimize Resource Usage**: Reduce fertilizer waste through targeted recommendations
- **Improve Soil Health**: Monitor and advise on long-term soil sustainability
- **Support Data-Driven Farming**: Enable farmers to make informed decisions with scientific backing
- **Increase Profitability**: Connect crop recommendations with market price analysis

## 🏗️ System Architecture

```mermaid
graph TB
    A[IoT Sensors] --> B[ESP32 Microcontroller]
    B --> C[FastAPI Backend]
    C --> D[Machine Learning Models]
    C --> E[PostgreSQL Database]
    C --> F[External APIs]
    D --> G[Crop Recommendation Engine]
    D --> H[Fertilizer Suggestion Engine]
    D --> I[Soil Health Scoring]
    D --> J[Market Price Analysis]
    F --> K[OpenWeather API]
    F --> L[Open-Meteo API]
    C --> M[React Frontend]
    G --> N[PDF Reports]
    H --> N
    I --> N
    J --> N
    N --> O[Farmer Users]
    E --> P[Historical Analytics]
    
    style A fill:#4CAF50,stroke:#388E3C
    style B fill:#2196F3,stroke:#0D47A1
    style C fill:#FF9800,stroke:#E65100
    style D fill:#9C27B0,stroke:#4A148C
    style E fill:#9C27B0,stroke:#4A148C
    style F fill:#F44336,stroke:#B71C1C
    style M fill:#009688,stroke:#1B5E20
    style N fill:#FF5722,stroke:#BF360C
```

### System Flow

1. **Data Collection**: IoT sensors collect real-time soil data (NPK, moisture, temperature, humidity)
2. **Transmission**: ESP32 microcontroller transmits data via Wi-Fi to FastAPI backend
3. **Processing**: Backend validates and processes incoming data
4. **Analysis**: ML models analyze soil conditions and environmental factors
5. **Prediction**: System generates crop recommendations with confidence scores
6. **Storage**: All data is securely stored in PostgreSQL database
7. **Visualization**: React frontend presents results with interactive charts
8. **Reporting**: PDF reports are generated for farmer reference

## ⚙️ Key Features

### 🌱 Core Agricultural Features

- **Smart Crop Prediction**
  - Multi-model selection (Stacking Classifier, Random Forest, Gradient Boosting, Decision Tree)
  - Confidence scores for all predictions (0-100%)
  - Top 3 alternative crop recommendations
  - Crop-specific soil treatment recommendations
  - Comprehensive fertilizer recommendations for 22 crops
  - Soil health scoring (0-100 scale with category classification)
  - Input validation with contextual warnings
  - Automated PDF report generation

- **Model Comparison Engine**
  - Side-by-side comparison of all available ML models
  - Confidence score visualization across models
  - Consensus prediction identification
  - Feature importance analysis

- **Historical Data & Analytics**
  - Comprehensive prediction history tracking
  - Farmer-specific data filtering
  - Soil health trend analysis with charts
  - Confidence trend visualization
  - Crop distribution analysis

- **Batch Prediction Processing**
  - CSV file upload for bulk soil sample analysis
  - Parallel processing of multiple predictions
  - Results export in CSV/Excel formats
  - Summary statistics generation

### 🌤️ Weather Services

- **Real-time Weather Data**
  - Current temperature, humidity, and rainfall
  - Weather condition descriptions
  - Wind speed and direction metrics

- **Forecast Services**
  - 7-day weather predictions
  - Daily temperature min/max values
  - Rainfall probability forecasts
  - Temperature and rainfall trend charts

- **Historical Weather Analysis**
  - Past weather data retrieval
  - Seasonal pattern recognition
  - Climate trend identification

### 🧪 Soil Health Assessment

- **Comprehensive Scoring System**
  - Overall health score (0-100 scale)
  - Category classification (Excellent/Good/Fair/Poor/Very Poor)
  - Component breakdown:
    - NPK Balance (40 points)
    - pH Score (20 points)
    - Nutrient Balance (15 points)
    - Environmental Conditions (15 points)
    - Soil Type Suitability (10 points)
  - Personalized improvement recommendations

### 🧾 Fertilizer Recommendation Engine

- **NPK Analysis**
  - Current soil nutrient level assessment
  - Crop-specific optimal nutrient ranges
  - Deficiency and excess identification
  - Application timing suggestions

- **Recommendation Features**
  - Specific fertilizer quantity calculations
  - Organic alternative suggestions
  - Land size-based dosage adjustments
  - Application schedule planning

### 📊 Data Management & Export

- **Database Storage**
  - All predictions with metadata storage
  - Model usage tracking
  - Confidence and soil health score logging
  - Indexed for fast query performance

- **Data Export Capabilities**
  - CSV export for data analysis
  - Excel export for spreadsheet integration
  - Farmer/phone-based filtering
  - Complete prediction history retrieval

### 📱 User Interface Features

- **Modern Dashboard**
  - Responsive design for all devices
  - Dark/light mode toggle
  - Multilingual support (English/Kannada)
  - Intuitive navigation system

- **Interactive Visualizations**
  - NPK level bar charts
  - Soil health component breakdown
  - Weather forecast trend charts
  - Historical trend analysis
  - Crop distribution visualization

## 🧠 Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **ML Library**: scikit-learn, pandas, numpy
- **PDF Generation**: ReportLab with matplotlib
- **HTTP Client**: httpx for async requests

### Frontend
- **Framework**: React.js with React Router
- **State Management**: React Context API
- **Styling**: CSS3 with custom properties
- **Charts**: Chart.js with react-chartjs-2
- **Icons**: Lucide React icon library
- **Build Tool**: Vite.js for fast development

### Hardware
- **Microcontroller**: ESP32 for IoT sensor integration
- **Sensors**: NPK sensors, DHT22 (temperature/humidity), soil moisture sensors
- **Communication**: Wi-Fi for data transmission

### APIs & Services
- **Weather Data**: OpenWeather API (primary) and Open-Meteo API (free alternative)
- **Geocoding**: Reverse geocoding for location data
- **Market Data**: Integration with agricultural price APIs

## 🌍 Environment Setup

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# .env.example (Do not commit)
DATABASE_URL=postgresql://postgres:password@localhost:5432/soil_health_db
OPENWEATHER_API_KEY=your_openweather_api_key_here
SECRET_KEY=changeme
ENV=development
```

### IoT Sensor Integration

The system is designed to receive data from IoT sensors including:
- **NPK Sensor**: Measures Nitrogen, Phosphorus, Potassium levels (0-200 mg/kg)
- **Soil Moisture Sensor**: Capacitive sensing for water content (0-100%)
- **DHT22 Sensor**: Temperature (-40°C to 80°C) and Humidity (0-100%)
- **pH Sensor**: Soil acidity measurement (3.0-10.0 pH)
- **Soil Temperature Sensor**: Additional temperature measurement for soil conditions

These sensors are connected to an ESP32 microcontroller which transmits data to the backend API via HTTP POST requests.

## 🧰 Installation & Setup

### Prerequisites

- **Python**: 3.9 or higher
- **Node.js**: 14 or higher
- **PostgreSQL**: 12 or higher
- **Git**: For version control
- **OpenWeather API Key**: For weather data (optional but recommended)

### Backend Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/soil-crop-recommender.git
   cd soil-crop-recommender
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file:
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   OPENWEATHER_API_KEY=your_openweather_api_key
   ```

5. **Database Initialization**
   ```bash
   python create_tables.py
   ```

6. **Run Backend Server**
   ```bash
   # Development mode
   uvicorn app.main:app --reload
   
   # Production mode
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

### Frontend Setup

1. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Run Development Server**
   ```bash
   npm run dev
   ```

4. **Build for Production**
   ```bash
   npm run build
   ```

### Hardware Setup

1. **Sensor Connection**
   - Connect NPK sensor to ESP32 analog pins
   - Connect DHT22 to digital pin with pull-up resistor
   - Connect pH sensor to analog input
   - Power all sensors with 3.3V from ESP32

2. **ESP32 Programming**
   - Install Arduino IDE
   - Add ESP32 board support
   - Flash sensor reading firmware
   - Configure Wi-Fi credentials

## 📡 API Endpoints

### Core Endpoints

- `GET /` - Health check endpoint
- `GET /models` - List available ML models with details
- `POST /predict` - Single crop prediction with comprehensive analysis
- `GET /download?farmer_name={name}` - Download PDF report

### Advanced Endpoints

- `POST /compare-models` - Compare predictions across all models
- `GET /history` - Retrieve prediction history with filtering
- `POST /batch-predict` - Process multiple predictions from CSV upload
- `GET /weather-forecast` - 7-day weather forecast data
- `POST /explain-prediction` - Feature importance explanation
- `GET /export` - Export data in CSV/Excel formats

### Weather Endpoints

- `GET /weather` - Current weather conditions
- `GET /weather-history` - Historical weather data
- `GET /weather-history-free` - Free Open-Meteo historical data

### Market Analysis Endpoints

- `GET /market-prices` - Current crop market prices
- `GET /price-trend` - Historical price trend analysis
- `GET /market-recommendation` - Market-based selling advice

### Example API Request/Response

#### Crop Prediction Request
```json
{
  "farmer_name": "Ramesh Kumar",
  "phone": "9876543210",
  "location": "Bidar, Karnataka",
  "land_size": 5.5,
  "N": 85,
  "P": 42,
  "K": 68,
  "temperature": 28.5,
  "humidity": 65,
  "ph": 6.8,
  "rainfall": 1100,
  "soil_type": "black soil",
  "model_name": "Stacking Classifier"
}
```

#### Crop Prediction Response
```json
{
  "predicted_crop": "Rice",
  "confidence": 95.2,
  "model_used": "Stacking Classifier",
  "top_alternatives": [
    {"crop": "Wheat", "confidence": 87.6},
    {"crop": "Maize", "confidence": 82.3}
  ],
  "soil_treatment": [
    "✅ Current nitrogen levels are adequate for rice cultivation",
    "⚠️ Phosphorus levels are slightly below optimal range"
  ],
  "fertilizer_estimate": "For 5.5 acres: Nitrogen (Urea): 247.5 kg, Phosphorus (DAP): 165 kg",
  "soil_health": {
    "overall_score": 82.5,
    "category": "Good",
    "breakdown": {
      "nitrogen_level": 14,
      "phosphorus_level": 10,
      "potassium_level": 12
    }
  },
  "pdf_url": "/download?farmer_name=Ramesh_Kumar"
}
```

## 🔌 Hardware Integration

### Sensor Suite

#### Primary Sensors
- **NPK Sensor**: Measures Nitrogen, Phosphorus, Potassium levels (0-200 mg/kg)
- **Soil Moisture Sensor**: Capacitive sensing for water content (0-100%)
- **DHT22 Sensor**: Temperature (-40°C to 80°C) and Humidity (0-100%)
- **pH Sensor**: Soil acidity measurement (3.0-10.0 pH)
- **Soil Temperature Sensor**: Additional temperature measurement for soil conditions

#### Sensor Specifications
- **Operating Voltage**: 3.3V-5V DC
- **Communication**: Analog and digital outputs
- **Accuracy**: ±2% for NPK, ±0.1 pH for acidity
- **Response Time**: <5 seconds for stable readings

### ESP32 Microcontroller

#### Hardware Features
- **Processor**: Dual-core 32-bit LX6 microprocessor
- **Connectivity**: Wi-Fi 802.11 b/g/n, Bluetooth
- **Memory**: 520 KB SRAM, external flash support
- **GPIO**: 34 programmable pins
- **Power**: 2.3V to 3.6V operation

#### Firmware Implementation
```cpp
// Arduino sketch for ESP32 sensor data transmission
#include <WiFi.h>
#include <HTTPClient.h>

void setup() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  // Sensor initialization
}

void loop() {
  // Read sensor values
  int N = readNitrogen();
  int P = readPhosphorus();
  int K = readPotassium();
  float soil_temp = readSoilTemperature();
  float soil_moisture = readSoilMoisture();
  float humidity = readHumidity();
  
  // Send data to backend
  sendDataToAPI(N, P, K, soil_temp, soil_moisture, humidity);
  
  delay(300000); // 5-minute intervals
}
```

### Data Transmission Protocol

#### Serial Communication
- **Baud Rate**: 115200 bps
- **Data Format**: JSON over HTTP POST
- **Security**: HTTPS encryption
- **Error Handling**: Retry logic with exponential backoff

#### Data Structure
```json
{
  "N": 85,
  "P": 42,
  "K": 68,
  "soil_temperature": 26.5,
  "soil_moisture": 45.2,
  "air_humidity": 65.0,
  "device_id": "ESP32-ABC123",
  "timestamp": "2025-11-10T14:30:00Z"
}
```

## 🧪 Testing & Validation

### API Endpoint Testing

#### Manual Testing
- **Tool**: Postman or curl
- **Coverage**: All endpoints tested with sample data
- **Validation**: Response structure and data accuracy verified

#### Example Test Cases
```bash
# Health check
curl http://localhost:8000/

# Crop prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"farmer_name":"Test Farmer","phone":"1234567890",...}'

# Weather data
curl "http://localhost:8000/weather?lat=17.5&lon=78.5"
```

### Model Validation

#### Accuracy Testing
- **Cross-validation**: 5-fold validation on training dataset
- **Holdout Testing**: Separate test dataset evaluation
- **Performance Metrics**: Accuracy, precision, recall, F1-score

#### Edge Case Testing
- **Invalid Inputs**: Boundary value testing
- **Missing Data**: Null value handling
- **Extreme Conditions**: Out-of-range parameter testing

### Integration Testing

#### End-to-End Workflows
1. **Prediction Flow**: Sensor data → ML model → PDF report
2. **History Tracking**: Data storage → retrieval → visualization
3. **Batch Processing**: CSV upload → parallel processing → export

#### Performance Testing
- **Response Times**: <2 seconds for prediction requests
- **Concurrent Users**: 100+ simultaneous requests
- **Database Queries**: Optimized with proper indexing

### Hardware Testing

#### Sensor Calibration
- **Laboratory Comparison**: Sensor vs. lab results
- **Field Validation**: Real-world condition testing
- **Long-term Stability**: 30-day continuous operation

#### Communication Testing
- **Network Resilience**: Wi-Fi dropout recovery
- **Data Integrity**: Transmission error detection
- **Power Management**: Low-power operation modes

## ☁️ Deployment

### Render.com Deployment
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment
```bash
# Build for production
cd frontend
npm run build

# Serve built files with any static server
npx serve -s dist
```

## 🚀 Future Improvements

### Technical Enhancements

#### Advanced ML Models
- **Deep Learning Integration**: Neural networks for complex pattern recognition
- **Reinforcement Learning**: Adaptive recommendation based on outcomes
- **Transfer Learning**: Pre-trained models for new crop varieties
- **Ensemble Methods**: Advanced stacking with meta-learning

#### IoT Expansion
- **Wireless Sensor Networks**: Mesh networking for large farms
- **Edge Computing**: On-device preprocessing for faster response
- **Satellite Integration**: Remote sensing for large-scale monitoring
- **Drone Technology**: Aerial data collection and analysis

#### Database Optimization
- **Time-Series Storage**: Specialized databases for temporal data
- **Data Lake Architecture**: Big data processing capabilities
- **Real-time Analytics**: Stream processing for instant insights
- **Geospatial Indexing**: Location-based query optimization

### Research Extensions

#### Crop Yield Prediction
- **Growth Modeling**: Mathematical models for yield estimation
- **Environmental Factors**: Advanced weather impact analysis
- **Historical Trends**: Long-term yield pattern recognition
- **Market Correlation**: Yield vs. price relationship analysis

#### Disease Prediction
- **Symptom Recognition**: Image-based disease identification
- **Preventive Measures**: Early warning systems
- **Treatment Recommendations**: Integrated pest management
- **Spread Modeling**: Disease propagation prediction

#### Sustainable Practices
- **Carbon Footprint**: Environmental impact assessment
- **Water Management**: Smart irrigation scheduling
- **Organic Farming**: Chemical-free cultivation support
- **Biodiversity**: Ecosystem health monitoring

