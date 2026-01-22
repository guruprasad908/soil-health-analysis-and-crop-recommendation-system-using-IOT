from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field, validator
from typing import Optional, Union
from datetime import datetime
from pathlib import Path
from .models.db_model import Prediction, NPKReading as NPKReadingModel, UNOReading as UNOReadingModel, Base
from .utils.database import SessionLocal, engine

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)
from .services.weather_service import (
    fetch_weather, 
    fetch_weather_forecast, 
    fetch_historical_weather, 
    fetch_historical_rainfall_range,
    fetch_historical_weather_openmeteo,
    fetch_historical_rainfall_range_openmeteo,
    reverse_geocode
)
from .services.fertilizer_advisor import get_soil_treatment, get_fertilizer_estimate
from .services.soil_health_scorer import calculate_soil_health_score
from .services.regional_crops import (
    filter_crops_by_region, 
    get_region_analysis,
    get_regional_constraints
)
from .utils.ensemble_methods import (
    soft_voting_ensemble,
    weighted_ensemble_predict,
    adjust_confidence_by_region,
    ensemble_with_uncertainty
)
from .services.market_price_service import fetch_crop_prices, get_price_trend, get_crop_recommendation
from .services.mixed_cropping import generate_mixed_layout
from .utils.pdf_generator import generate_pdf
from fastapi import UploadFile, File
from typing import List, Dict
import io
import pandas as pd
import joblib
import numpy as np
import os
from dotenv import load_dotenv
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import StandardScaler

# Load environment variables
load_dotenv()

# Configuration constants
MAX_NPK_READINGS_MEMORY = 100  # Maximum readings to keep in memory (fallback)
MAX_LAND_SIZE_ACRES = 10000  # Maximum land size in acres
MAX_NPK_VALUE = 200  # Maximum NPK value in mg/kg
MAX_DASHBOARD_LIMIT = 100  # Maximum readings to return from dashboard
MAX_RAINFALL_MM = 300  # Maximum rainfall in mm (matches dataset range: 20-300 mm)
MIN_RAINFALL_MM = 20   # Minimum rainfall in mm (matches dataset range)

# Reinforcement Learning Model Class (needed for joblib loading)
class CropRecommendationRL:
    """RL model for crop recommendation using Q-Learning"""
    def __init__(self, crops, learning_rate=0.1, discount_factor=0.95, epsilon=0.2):
        self.crops = crops
        self.n_crops = len(crops)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = {}
        self.experience_buffer = []
        self.max_buffer_size = 10000
        self.total_predictions = 0
        self.total_feedback = 0
        self.success_rate = 0.0
    
    def _get_state_key(self, features):
        n_bins = int(features['N'] // 20)
        p_bins = int(features['P'] // 20)
        k_bins = int(features['K'] // 20)
        temp_bins = int(features['temperature'] // 5)
        rainfall_bins = int(features['rainfall'] // 200)
        ph_bins = int(features['ph'] * 2)
        soil_type = features['soil_type_encoded']
        return f"{n_bins}_{p_bins}_{k_bins}_{temp_bins}_{rainfall_bins}_{ph_bins}_{soil_type}"
    
    def _initialize_state(self, state_key):
        if state_key not in self.q_table:
            self.q_table[state_key] = {crop: np.random.uniform(0, 0.1) for crop in self.crops}
    
    def predict(self, features):
        state_key = self._get_state_key(features)
        self._initialize_state(state_key)
        self.total_predictions += 1
        if np.random.random() < self.epsilon:
            crop = np.random.choice(self.crops)
            confidence = 0.5
        else:
            q_values = self.q_table[state_key]
            crop = max(q_values, key=q_values.get)
            max_q = q_values[crop]
            min_q = min(q_values.values())
            confidence = (max_q - min_q) / (max_q + 1e-6) if max_q > min_q else 0.5
        return crop, confidence
    
    def get_top_recommendations(self, features, top_n=3):
        state_key = self._get_state_key(features)
        self._initialize_state(state_key)
        q_values = self.q_table[state_key]
        sorted_crops = sorted(q_values.items(), key=lambda x: x[1], reverse=True)
        recommendations = []
        for i, (crop, q_val) in enumerate(sorted_crops[:top_n]):
            max_q = sorted_crops[0][1]
            min_q = sorted_crops[-1][1]
            confidence = (q_val - min_q) / (max_q - min_q + 1e-6) if max_q > min_q else 1.0 / (i + 1)
            recommendations.append({'crop': crop, 'confidence': min(confidence, 1.0), 'q_value': float(q_val)})
        return recommendations
    
    def update(self, features, recommended_crop, actual_crop, reward):
        from datetime import datetime
        state_key = self._get_state_key(features)
        self._initialize_state(state_key)
        experience = {'state': state_key, 'action': recommended_crop, 'reward': reward, 'actual': actual_crop, 'timestamp': datetime.now().isoformat()}
        self.experience_buffer.append(experience)
        if len(self.experience_buffer) > self.max_buffer_size:
            self.experience_buffer.pop(0)
        old_q = self.q_table[state_key][recommended_crop]
        max_next_q = self.q_table[state_key][actual_crop] if actual_crop in self.crops else max(self.q_table[state_key].values())
        new_q = old_q + self.learning_rate * (reward + self.discount_factor * max_next_q - old_q)
        self.q_table[state_key][recommended_crop] = new_q
        if actual_crop in self.crops and actual_crop != recommended_crop:
            self.q_table[state_key][actual_crop] += self.learning_rate * reward
        self.total_feedback += 1
        self.success_rate = sum(1 for e in self.experience_buffer if e['reward'] > 0) / max(len(self.experience_buffer), 1)
    
    def get_stats(self):
        return {'total_predictions': self.total_predictions, 'total_feedback': self.total_feedback, 'success_rate': self.success_rate, 'states_explored': len(self.q_table), 'experience_buffer_size': len(self.experience_buffer), 'learning_rate': self.learning_rate, 'epsilon': self.epsilon}

# Wrapper class for models that need scaled data (needed for loading StackingClassifier)
class ScaledModel(BaseEstimator, ClassifierMixin):
    def __init__(self, base_model):
        self.base_model = base_model
        self.scaler = StandardScaler()
        self.model = None  # type: Optional[ClassifierMixin]
    
    def fit(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model = self.base_model
        self.model.fit(X_scaled, y)
        return self
    
    def predict(self, X):
        if self.model is None:
            raise ValueError("Model has not been fitted yet.")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)  # type: ignore
    
    def predict_proba(self, X):
        if self.model is None:
            raise ValueError("Model has not been fitted yet.")
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)  # type: ignore
    
    @property
    def classes_(self):
        if self.model is None:
            raise ValueError("Model has not been fitted yet.")
        return self.model.classes_  # type: ignore

app = FastAPI()

# CORS configuration - allow frontend origin from environment or default to localhost
# Get allowed origins from environment or use defaults
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", f"{FRONTEND_URL},http://localhost:3000").split(",")
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS]

# In development, allow all origins; in production, restrict to specific domains
ENV = os.getenv("ENV", "development")
if ENV == "production":
    cors_origins = ALLOWED_ORIGINS
else:
    cors_origins = ["*"]  # Development: allow all

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register ScaledModel in sys.modules for joblib unpickling
import sys
from types import ModuleType

# Register ScaledModel in all possible module paths where it might be saved
if 'app.models.train_model' not in sys.modules:
    mock_module = ModuleType('app.models.train_model')
    mock_module.ScaledModel = ScaledModel
    sys.modules['app.models.train_model'] = mock_module

# Register in __main__ module (where it might have been saved)
if '__main__' not in sys.modules:
    sys.modules['__main__'] = ModuleType('__main__')
sys.modules['__main__'].ScaledModel = ScaledModel

# Also register in the current module
if __name__ not in sys.modules:
    sys.modules[__name__] = ModuleType(__name__)
sys.modules[__name__].ScaledModel = ScaledModel

# Load all available models with error handling
models = {}
try:
    models["Stacking Classifier"] = joblib.load("app/models/rf_model.joblib")
    print("✅ Loaded Stacking Classifier")
except Exception as e:
    print(f"⚠️ Could not load Stacking Classifier: {e}")
    print(f"   Note: Other models are still available")

try:
    models["Random Forest"] = joblib.load("app/models/random_forest.joblib")
    print("✅ Loaded Random Forest")
except Exception as e:
    print(f"⚠️ Could not load Random Forest: {e}")

try:
    models["Gradient Boosting"] = joblib.load("app/models/gradient_boosting.joblib")
    print("✅ Loaded Gradient Boosting")
except Exception as e:
    print(f"⚠️ Could not load Gradient Boosting: {e}")

try:
    models["Decision Tree"] = joblib.load("app/models/decision_tree.joblib")
    print("✅ Loaded Decision Tree")
except Exception as e:
    print(f"⚠️ Could not load Decision Tree: {e}")

# Try loading new enhanced models
try:
    models["LightGBM"] = joblib.load("app/models/lightgbm.joblib")
    print("✅ Loaded LightGBM")
except Exception as e:
    print(f"⚠️ Could not load LightGBM: {e}")

try:
    models["CatBoost"] = joblib.load("app/models/catboost.joblib")
    print("✅ Loaded CatBoost")
except Exception as e:
    print(f"⚠️ Could not load CatBoost: {e}")

try:
    models["XGBoost"] = joblib.load("app/models/xgboost.joblib")
    print("✅ Loaded XGBoost")
except Exception as e:
    print(f"⚠️ Could not load XGBoost: {e}")

try:
    models["AdaBoost"] = joblib.load("app/models/adaboost.joblib")
    print("✅ Loaded AdaBoost")
except Exception as e:
    print(f"⚠️ Could not load AdaBoost: {e}")

# Load Reinforcement Learning model
try:
    models["Reinforcement Learning"] = joblib.load("app/models/rl_model.joblib")
    print("✅ Loaded Reinforcement Learning Model")
except Exception as e:
    print(f"⚠️ Could not load Reinforcement Learning: {e}")

if not models:
    raise RuntimeError("❌ No models could be loaded! Please train models first.")

# Default model (use Random Forest if Stacking Classifier not available, as it has same accuracy)
if "Stacking Classifier" in models:
    default_model = models["Stacking Classifier"]
elif "Random Forest" in models:
    default_model = models["Random Forest"]  # Same 99.55% accuracy
else:
    default_model = list(models.values())[0] if models else None

# Load encoder
try:
    soil_encoder = joblib.load("app/models/soil_encoder.joblib")
    print("✅ Loaded soil encoder")
except Exception as e:
    print(f"❌ Could not load soil encoder: {e}")
    raise



# Valid soil types from the encoder
VALID_SOIL_TYPES = ["alluvial soil", "black soil", "red soil", "laterite soil", "sandy soil", "peaty soil"]

# 📥 Manual input schema with validation
class SoilInput(BaseModel):
    farmer_name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=10, max_length=15)
    location: Optional[str] = Field(None, min_length=1, max_length=100, description="Village/Town name (optional - can be auto-detected)")
    land_size: float = Field(..., gt=0, le=MAX_LAND_SIZE_ACRES)  # Between 0 and MAX_LAND_SIZE_ACRES acres
    N: float = Field(..., ge=0, le=MAX_NPK_VALUE)  # Nitrogen: 0-MAX_NPK_VALUE mg/kg
    P: float = Field(..., ge=0, le=MAX_NPK_VALUE)  # Phosphorus: 0-MAX_NPK_VALUE mg/kg
    K: float = Field(..., ge=0, le=MAX_NPK_VALUE)  # Potassium: 0-MAX_NPK_VALUE mg/kg
    temperature: float = Field(..., ge=-10, le=50)  # Temperature: -10 to 50°C
    humidity: float = Field(..., ge=0, le=100)  # Humidity: 0-100%
    ph: float = Field(..., ge=3.0, le=10.0)  # pH: 3.0-10.0
    rainfall: float = Field(..., ge=0, description="Rainfall in mm")
    soil_type: str
    model_name: str = Field(default="Random Forest", description="ML model to use for prediction")
    
    @validator('soil_type')
    def validate_soil_type(cls, v):
        if v.lower() not in [s.lower() for s in VALID_SOIL_TYPES]:
            raise ValueError(f"Soil type must be one of: {', '.join(VALID_SOIL_TYPES)}")
        # Normalize to match encoder format
        for valid_type in VALID_SOIL_TYPES:
            if v.lower() == valid_type.lower():
                return valid_type
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        # Basic phone validation - should contain only digits, +, -, spaces
        cleaned = ''.join(c for c in v if c.isdigit() or c in '+-() ')
        if len(cleaned.replace(' ', '').replace('-', '').replace('+', '').replace('(', '').replace(')', '')) < 10:
            raise ValueError("Phone number must contain at least 10 digits")
        return v


# NPK Reading from ESP8266 sensor
class NPKReading(BaseModel):
    n: int
    p: int
    k: int
    device_id: Optional[str] = "ESP8266"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class NPKDataInput(BaseModel):
    n: int
    p: int
    k: int
    device_id: Optional[str] = "ESP8266"

class UNODataInput(BaseModel):
    temperature: float
    humidity: float
    moisture: int
    device_id: Optional[str] = "ArduinoUNO"

# Soil Reading from Arduino UNO R4 WiFi
class SoilReading(BaseModel):
    Soil: int
    Temp: float
    Hum: float
    device_id: Optional[str] = "UNO_R4"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# New model for soil sensor data from Arduino
class SoilSensorData(BaseModel):
    Soil: int
    Temp: float
    Hum: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)



@app.get("/")
def home():
    return {"message": "🌾 Soil Health & Crop Recommendation API is running!"}

@app.get("/models")
def get_available_models():
    """Get list of available ML models"""
    model_info = {
        "Stacking Classifier": {
            "name": "Stacking Classifier",
            "description": "Best ensemble model combining top 4 models (99.55% accuracy)",
            "type": "Ensemble"
        },
        "Random Forest": {
            "name": "Random Forest",
            "description": "Random Forest with 150 trees (99.55% accuracy) - Recommended",
            "type": "Tree-based"
        },
        "Gradient Boosting": {
            "name": "Gradient Boosting",
            "description": "Gradient Boosting Classifier (98.64% accuracy)",
            "type": "Boosting"
        },
        "Decision Tree": {
            "name": "Decision Tree",
            "description": "Single Decision Tree Classifier (98.86% accuracy)",
            "type": "Tree-based"
        },
        "AdaBoost": {
            "name": "AdaBoost",
            "description": "AdaBoost Classifier (87.50% accuracy)",
            "type": "Boosting"
        },
        "Reinforcement Learning": {
            "name": "Reinforcement Learning",
            "description": "Q-Learning model that learns from farmer feedback",
            "type": "Adaptive"
        },
        "LightGBM": {
            "name": "LightGBM",
            "description": "Light Gradient Boosting Machine (99.32% accuracy)",
            "type": "Boosting"
        },
        "CatBoost": {
            "name": "CatBoost",
            "description": "CatBoost Classifier (99.55% accuracy)",
            "type": "Boosting"
        },
        "XGBoost": {
            "name": "XGBoost",
            "description": "Extreme Gradient Boosting",
            "type": "Boosting"
        }
    }
    # Filter model_info to only include available models
    available_info = {k: v for k, v in model_info.items() if k in models}
    
    # Determine default (Random Forest if Stacking not available)
    default = "Stacking Classifier" if "Stacking Classifier" in models else "Random Forest"
    
    return {
        "available_models": list(models.keys()),
        "model_details": available_info,
        "default": default
    }

# 🌍 Auto-detect location from GPS coordinates
@app.get("/auto-location")
async def auto_detect_location(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """
    Auto-detect village/town name from GPS coordinates.
    Perfect for farmers - just use GPS and we'll find the location!
    Uses multiple geocoding services for better accuracy, especially for Indian locations.
    """
    try:
        # Validate coordinates
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return {
                "location": f"{lat:.4f}, {lon:.4f}",
                "latitude": lat,
                "longitude": lon,
                "success": False,
                "error": "Invalid coordinates"
            }
        
        location_name = await reverse_geocode(lat, lon)
        
        if not location_name or location_name == f"{lat:.4f}, {lon:.4f}":
            # If we only got coordinates, try one more time with a slight delay
            import asyncio
            await asyncio.sleep(0.5)  # Small delay for rate limiting
            location_name = await reverse_geocode(lat, lon)
        
        if not location_name:
            # Final fallback: return coordinates as location
            location_name = f"{lat:.4f}, {lon:.4f}"
        
        return {
            "location": location_name,
            "latitude": lat,
            "longitude": lon,
            "success": True,
            "source": "GPS + Reverse Geocoding"
        }
    except Exception as e:
        print(f"❌ Auto-location error: {e}")
        return {
            "location": f"{lat:.4f}, {lon:.4f}",
            "latitude": lat,
            "longitude": lon,
            "success": False,
            "error": str(e)
        }

# 📅 5-Day Weather Forecast
@app.get("/weather-forecast")
async def get_weather_forecast(lat: float = Query(...), lon: float = Query(...)):
    try:
        return await fetch_weather_forecast(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching forecast: {str(e)}")

# 🌦 Optional weather viewer endpoint
@app.get("/weather")
async def get_weather(lat: float = Query(...), lon: float = Query(...)):
    try:
        return await fetch_weather(lat, lon)
    except Exception as e:
        return {"error": str(e)}

# 📅 Historical weather data endpoint (free Open-Meteo version)
@app.get("/weather-history-free")
async def get_weather_history_free(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format")
):
    """
    Fetch historical weather data using Open-Meteo (FREE, no API key required)
    Provides 80+ years of historical weather data
    """
    try:
        return await fetch_historical_rainfall_range_openmeteo(lat, lon, start_date=start_date, end_date=end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical weather data: {str(e)}")

# 🌾 Mixed Cropping Layout Endpoint
@app.get("/mixed-cropping-layout-v2")
def get_mixed_cropping_layout(
    crop: str = Query(..., description="Main crop name"),
    land_size: float = Query(1.0, description="Land size in acres")
):
    """
    Generate a mixed cropping layout for a given crop and land size.
    Returns layout dimensions, sections, and compatible intercrops.
    """
    try:
        return generate_mixed_layout(crop, land_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating layout: {str(e)}")

# 🧠 Crop prediction using manual values only
@app.post("/predict")
def predict_crop(data: SoilInput):
    try:
        # Auto-detect location if not provided (placeholder - frontend will handle this)
        # Input validation warnings
        warnings = []
        
        # Check for extreme values
        if data.N > 150:
            warnings.append("⚠️ Very high nitrogen levels detected. May cause excessive vegetative growth.")
        if data.P > 80:
            warnings.append("⚠️ Very high phosphorus levels detected. May interfere with micronutrient uptake.")
        if data.K > 150:
            warnings.append("⚠️ Very high potassium levels detected. May cause magnesium deficiency.")
        
        if data.ph < 4.5 or data.ph > 9.0:
            warnings.append("⚠️ Extreme pH value detected. Soil may need significant treatment.")
        
        # Select model based on user choice
        selected_model_name = data.model_name
        use_ensemble = False
        
        # Check if user wants ensemble
        if selected_model_name == "Ensemble (Soft Voting)" or selected_model_name == "Ensemble":
            use_ensemble = True
            if len(models) < 2:
                warnings.append("⚠️ Ensemble requires at least 2 models. Using single model instead.")
                use_ensemble = False
                selected_model_name = list(models.keys())[0] if models else None
        elif selected_model_name not in models:
            # Use first available model as default
            selected_model_name = list(models.keys())[0] if models else None
            if selected_model_name:
                warnings.append(f"⚠️ Invalid model name. Using: {selected_model_name}")
            else:
                raise HTTPException(status_code=500, detail="No models available")
        
        selected_model = models.get(selected_model_name) if not use_ensemble else None
        
        # 🔢 Encode input
        try:
            soil_type_encoded = soil_encoder.transform([data.soil_type])[0]
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid soil type: {data.soil_type}. Must be one of: {', '.join(VALID_SOIL_TYPES)}")
        
        # Adjust rainfall data - divide by 2 to match dataset expectations
        adjusted_rainfall = data.rainfall / 2 if data.rainfall > 300 else data.rainfall
        
        features = pd.DataFrame([{
            "N": data.N, "P": data.P, "K": data.K,
            "temperature": data.temperature, "humidity": data.humidity,
            "ph": data.ph, "rainfall": adjusted_rainfall,
            "soil_type_encoded": soil_type_encoded
        }])

        # Get prediction with confidence scores using selected model or ensemble
        if use_ensemble and len(models) > 1:
            # Use ensemble method for better confidence
            try:
                # Get class names from first available model
                first_model = list(models.values())[0]
                class_names = first_model.classes_
                
                # Use weighted ensemble
                ensemble_result = weighted_ensemble_predict(models, features, class_names)
                predicted_crop = ensemble_result["predicted_crop"]
                prediction_proba = ensemble_result["probabilities"]
                main_confidence = ensemble_result["confidence"]
                
                # Get top 5 crops from ensemble
                top_indices = np.argsort(prediction_proba)[-5:][::-1]
                all_top_crops = [class_names[idx] for idx in top_indices]
                
            except Exception as e:
                # Fallback to single model if ensemble fails
                warnings.append(f"⚠️ Ensemble prediction failed: {e}. Using single model.")
                use_ensemble = False
                selected_model = models.get(selected_model_name)
                predicted_crop = selected_model.predict(features)[0]
                prediction_proba = selected_model.predict_proba(features)[0]
                class_names = selected_model.classes_
                top_indices = np.argsort(prediction_proba)[-5:][::-1]
                all_top_crops = [class_names[idx] for idx in top_indices]
                main_confidence = float(prediction_proba[np.where(class_names == predicted_crop)[0][0]] * 100)
        elif selected_model_name == "Reinforcement Learning":
            # Handle RL model differently - it has custom predict method
            try:
                rl_model = models.get("Reinforcement Learning")
                # Convert features to dict format for RL model
                # Use adjusted rainfall for RL model as well
                adjusted_rainfall = data.rainfall / 2 if data.rainfall > 300 else data.rainfall
                
                features_dict = {
                    'N': data.N,
                    'P': data.P,
                    'K': data.K,
                    'temperature': data.temperature,
                    'humidity': data.humidity,
                    'ph': data.ph,
                    'rainfall': adjusted_rainfall,
                    'soil_type_encoded': soil_type_encoded
                }
                
                # Get top recommendations from RL model
                recommendations = rl_model.get_top_recommendations(features_dict, top_n=5)
                predicted_crop = recommendations[0]['crop']
                main_confidence = recommendations[0]['confidence'] * 100
                
                # Build all_top_crops and prediction_proba
                all_top_crops = [rec['crop'] for rec in recommendations]
                prediction_proba = np.array([rec['confidence'] for rec in recommendations])
                class_names = np.array(all_top_crops)
                
            except Exception as e:
                warnings.append(f"⚠️ RL model error: {e}. Using fallback.")
                # Fallback to another model
                fallback_model = models.get("Random Forest") or models.get("Stacking Classifier") or list(models.values())[0]
                predicted_crop = fallback_model.predict(features)[0]
                prediction_proba = fallback_model.predict_proba(features)[0]
                class_names = fallback_model.classes_
                top_indices = np.argsort(prediction_proba)[-5:][::-1]
                all_top_crops = [class_names[idx] for idx in top_indices]
                main_confidence = float(prediction_proba[np.where(class_names == predicted_crop)[0][0]] * 100)
        else:
            # Use single model
            predicted_crop = selected_model.predict(features)[0]
            prediction_proba = selected_model.predict_proba(features)[0]
            class_names = selected_model.classes_
            top_indices = np.argsort(prediction_proba)[-5:][::-1]
            all_top_crops = [class_names[idx] for idx in top_indices]
            main_confidence = float(prediction_proba[np.where(class_names == predicted_crop)[0][0]] * 100)
        
        # Auto-detect location if not provided
        location_to_use = data.location
        if not location_to_use or location_to_use.strip() == "":
            location_to_use = "Location not specified"
        
        # 🌾 REGIONAL CROP FILTERING - Critical for preventing unrealistic predictions
        # Filter crops to only include regionally appropriate ones
        filtered_crops = filter_crops_by_region(all_top_crops, location_to_use)
        
        # Get the best regionally suitable crop
        suitable_crop = None
        for crop_info in filtered_crops:
            if crop_info["suitable"]:
                suitable_crop = crop_info["crop"]
                break
        
        # If no suitable crop found, use the first filtered crop (or fallback to original)
        if not suitable_crop:
            if filtered_crops:
                suitable_crop = filtered_crops[0]["crop"]
            else:
                suitable_crop = predicted_crop  # Fallback to original prediction
        
        # Update predicted_crop to regionally suitable one
        predicted_crop = suitable_crop
        
        # Adjust main confidence based on regional suitability (if not already set by ensemble)
        if not use_ensemble:
            crop_idx = np.where(class_names == predicted_crop)[0]
            if len(crop_idx) > 0:
                main_confidence = float(prediction_proba[crop_idx[0]] * 100)
            else:
                # If crop not in model classes, use average confidence
                main_confidence = float(np.mean(prediction_proba) * 100)
        
        # Adjust main confidence based on regional suitability
        is_suitable = any(c["suitable"] for c in filtered_crops if c["crop"] == predicted_crop)
        main_confidence = adjust_confidence_by_region(
            main_confidence,
            predicted_crop,
            location_to_use,
            is_suitable
        )
        
        # Get top 3 crops (regionally filtered) with confidence
        top_crops = []
        for crop_info in filtered_crops[:3]:
            crop_name = crop_info["crop"]
            crop_idx = np.where(class_names == crop_name)[0]
            if len(crop_idx) > 0:
                confidence = float(prediction_proba[crop_idx[0]] * 100)
                # Adjust confidence based on regional suitability
                confidence = adjust_confidence_by_region(
                    confidence, 
                    crop_name, 
                    location_to_use,
                    crop_info.get("suitable", True)
                )
            else:
                confidence = 0.0
            top_crops.append({
                "crop": crop_name,
                "confidence": confidence,
                "region_verified": crop_info.get("region_verified", False),
                "suitable": crop_info.get("suitable", False)
            })
        
        # Get comprehensive regional analysis
        soil_data = {
            "N": data.N,
            "P": data.P,
            "K": data.K,
            "temperature": data.temperature,
            "humidity": data.humidity,
            "ph": data.ph,
            "rainfall": data.rainfall,
            "soil_type": data.soil_type
        }
        regional_analysis = get_region_analysis(location_to_use, predicted_crop, soil_data)
        
        # Add regional warnings if crop is unsuitable
        if regional_analysis["is_unsuitable"]:
            warnings.append(f"⚠️ REGIONAL WARNING: {predicted_crop} is not typically grown in {regional_analysis['region']}. Consider regionally appropriate alternatives.")
        elif not regional_analysis["is_regionally_suitable"]:
            warnings.append(f"ℹ️ Note: {predicted_crop} may not be the most common crop in {regional_analysis['region']}. Verify local suitability.")
        
        # Calculate soil health score using adjusted rainfall
        adjusted_rainfall = data.rainfall / 2 if data.rainfall > 300 else data.rainfall
        soil_health = calculate_soil_health_score(
            data.N, data.P, data.K, data.ph,
            data.temperature, data.humidity, adjusted_rainfall, data.soil_type
        )
        
        # Get crop-specific recommendations
        soil_treatment = get_soil_treatment(
            data.ph, data.N, data.P, data.K,
            predicted_crop=predicted_crop,
            soil_type=data.soil_type
        )
        fertilizer_estimate = get_fertilizer_estimate(predicted_crop, {
            "N": data.N, "P": data.P, "K": data.K
        }, data.land_size)

        # Store in DB
        db = SessionLocal()
        try:
            db.add(Prediction(
                farmer_name=data.farmer_name,
                phone=data.phone,
                location=location_to_use,
                land_size=data.land_size,
                nitrogen=data.N,
                phosphorus=data.P,
                potassium=data.K,
                temperature=data.temperature,
                humidity=data.humidity,
                ph=data.ph,
                rainfall=data.rainfall,
                soil_type=data.soil_type,
                predicted_crop=predicted_crop,
                model_used="Ensemble (Soft Voting)" if use_ensemble else selected_model_name,
                confidence=main_confidence,
                soil_health_score=soil_health["overall_score"],
                timestamp=datetime.utcnow()
            ))
            db.commit()
        except Exception as e:
            db.rollback()
            warnings.append(f"⚠️ Could not save to database: {str(e)}")
        finally:
            db.close()

        # Get market price information for the predicted crop
        market_recommendation = None
        try:
            # Extract state from location if possible
            state = None
            if data.location:
                # Simple state extraction (in a real implementation, you might want to use a more sophisticated approach)
                location_parts = data.location.split(',')
                if len(location_parts) > 1:
                    state = location_parts[-1].strip()
            
            # Mock market recommendation (in a real implementation, you would call the market price service)
            market_recommendation = {
                "crop": predicted_crop,
                "recommendation": "Market data integration is available in the system. In a production environment, this would show real-time market prices.",
                "current_price_range": {
                    "min": 2000,
                    "max": 3500,
                    "average": 2750
                },
                "best_market": {
                    "name": "Local Market",
                    "state": state or "Your State",
                    "price": 2750,
                    "unit": "₹/Quintal"
                }
            }
        except Exception as e:
            warnings.append(f"⚠️ Could not fetch market price data: {str(e)}")

        # PDF Report
        report_data = data.dict()
        report_data.update({
            "predicted_crop": predicted_crop,
            "confidence": main_confidence,
            "model_used": "Ensemble (Soft Voting)" if use_ensemble else selected_model_name,
            "top_crops": top_crops,
            "soil_treatment": soil_treatment,
            "fertilizer_estimate": fertilizer_estimate,
            "soil_health": soil_health,
            "warnings": warnings,
            "market_recommendation": market_recommendation
        })

        filename = f"{data.farmer_name.replace(' ', '_')}_report.pdf"
        try:
            generate_pdf(report_data, filename)
        except Exception as e:
            warnings.append(f"⚠️ Could not generate PDF report: {str(e)}")

        return {
            "predicted_crop": predicted_crop,
            "confidence": main_confidence,
            "model_used": "Ensemble (Soft Voting)" if use_ensemble else selected_model_name,
            "top_alternatives": top_crops[1:] if len(top_crops) > 1 else [],  # Exclude the main prediction
            "rainfall_used": data.rainfall,
            "soil_treatment": soil_treatment,
            "fertilizer_estimate": fertilizer_estimate,
            "soil_health": soil_health,
            "market_recommendation": market_recommendation,
            "warnings": warnings,
            "pdf_url": f"/download?farmer_name={data.farmer_name}",
            # 🌾 Regional Analysis - NEW
            "regional_analysis": regional_analysis,
            "region_verified": True,
            "location": location_to_use
        }

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


# 📊 Get historical predictions for dashboard
@app.get("/dashboard")
def get_dashboard_data(limit: int = Query(50, le=MAX_DASHBOARD_LIMIT)):
    db = SessionLocal()
    try:
        # Get recent predictions ordered by timestamp
        predictions = db.query(Prediction).order_by(Prediction.timestamp.desc()).limit(limit).all()
        
        # Convert to dict and format
        data = []
        for pred in predictions:
            data.append({
                "id": pred.id,
                "farmer_name": pred.farmer_name,
                "location": pred.location,
                "land_size": pred.land_size,
                "predicted_crop": pred.predicted_crop,
                "model_used": pred.model_used,
                "confidence": pred.confidence,
                "soil_health_score": pred.soil_health_score,
                "timestamp": pred.timestamp.isoformat()
            })
        
        return {"predictions": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()

# 📜 History endpoint (alias for dashboard with optional filtering)
@app.get("/history")
def get_history(limit: int = Query(100, le=MAX_DASHBOARD_LIMIT)):
    return get_dashboard_data(limit)

# ⚖️ Model Comparison Endpoint
@app.post("/compare-models")
def compare_models(data: SoilInput):
    try:
        results = []
        
        # Encode input once
        try:
            soil_type_encoded = soil_encoder.transform([data.soil_type])[0]
        except ValueError:
            soil_type_encoded = 0 # Fallback
            
        # Adjust rainfall
        adjusted_rainfall = data.rainfall / 2 if data.rainfall > 300 else data.rainfall
        
        features = pd.DataFrame([{
            "N": data.N, "P": data.P, "K": data.K,
            "temperature": data.temperature, "humidity": data.humidity,
            "ph": data.ph, "rainfall": adjusted_rainfall,
            "soil_type_encoded": soil_type_encoded
        }])
        
        # Run all models
        for name, model in models.items():
            try:
                # Special handling for Reinforcement Learning model (different API)
                if name == "Reinforcement Learning":
                    # RL model uses dict-based features instead of DataFrame
                    features_dict = {
                        'N': data.N,
                        'P': data.P,
                        'K': data.K,
                        'temperature': data.temperature,
                        'humidity': data.humidity,
                        'ph': data.ph,
                        'rainfall': adjusted_rainfall,
                        'soil_type_encoded': soil_type_encoded
                    }
                    
                    # Get top recommendation from RL model
                    recommendations = model.get_top_recommendations(features_dict, top_n=1)
                    if recommendations:
                        recommended = recommendations[0]
                        results.append({
                            "model": name,
                            "predicted_crop": recommended['crop'],
                            "confidence": recommended['confidence'] * 100,
                            "success": True
                        })
                    else:
                        results.append({
                            "model": name,
                            "error": "No recommendations available",
                            "success": False
                        })
                else:
                    # Standard sklearn-based models
                    predicted_crop = model.predict(features)[0]
                    prediction_proba = model.predict_proba(features)[0]
                    class_names = model.classes_
                    confidence = float(prediction_proba[np.where(class_names == predicted_crop)[0][0]] * 100)
                    
                    results.append({
                        "model": name,
                        "predicted_crop": predicted_crop,
                        "confidence": confidence,
                        "success": True
                    })
            except Exception as e:
                    results.append({
                        "model": name,
                        "error": str(e),
                        "success": False
                    })
        
        # Apply regional filtering to all results
        # Extract just the crop names for filtering
        predicted_crops = [r['predicted_crop'] for r in results if r.get('success')]
        
        # Get filtered status for these crops
        filtered_status = filter_crops_by_region(predicted_crops, data.location)
        
        # Map back to results
        final_results = []
        for res in results:
            if not res.get('success'):
                final_results.append(res)
                continue
                
            # Find matching filter status
            crop_name = res['predicted_crop']
            status = next((f for f in filtered_status if f['crop'] == crop_name), None)
            
            if status:
                res['is_suitable'] = status['suitable']
                res['region_verified'] = True
                
                # If unsuitable, add warning
                if not status['suitable']:
                    res['warning'] = "Not suitable for this region"
            
            final_results.append(res)
            
        return {"results": final_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")



# 📈 Get model statistics
@app.get("/model-stats")
def get_model_stats():
    try:
        # Get RL model stats if available
        rl_stats = {}
        if "Reinforcement Learning" in models:
            rl_model = models["Reinforcement Learning"]
            rl_stats = rl_model.get_stats()
        
        return {
            "total_models": len(models),
            "available_models": list(models.keys()),
            "rl_model_stats": rl_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting model stats: {str(e)}")


# 🔄 Reinforcement Learning Feedback Endpoint
@app.post("/rl-feedback")
def rl_feedback(feedback: dict):
    try:
        # Validate required fields
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_type', 'recommended_crop', 'actual_crop', 'success']
        for field in required_fields:
            if field not in feedback:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Validate soil type
        if feedback['soil_type'] not in VALID_SOIL_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid soil type. Must be one of: {', '.join(VALID_SOIL_TYPES)}")
        
        # Get RL model
        if "Reinforcement Learning" not in models:
            raise HTTPException(status_code=500, detail="Reinforcement Learning model not loaded")
        
        rl_model = models["Reinforcement Learning"]
        
        # Prepare features for the model
        try:
            soil_type_encoded = soil_encoder.transform([feedback['soil_type']])[0]
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid soil type: {feedback['soil_type']}")
        
        features = {
            'N': feedback['N'],
            'P': feedback['P'],
            'K': feedback['K'],
            'temperature': feedback['temperature'],
            'humidity': feedback['humidity'],
            'ph': feedback['ph'],
            'rainfall': feedback['rainfall'],
            'soil_type_encoded': soil_type_encoded
        }
        
        # Calculate reward based on feedback
        if feedback['success']:
            if feedback['recommended_crop'] == feedback['actual_crop']:
                reward = 1.0  # Perfect match
            else:
                reward = 0.5  # Farmer chose different crop but it worked
        else:
            reward = -1.0  # Recommendation didn't work
        
        # Update model
        rl_model.update(
            features=features,
            recommended_crop=feedback['recommended_crop'],
            actual_crop=feedback['actual_crop'],
            reward=reward
        )
        
        # Save updated model
        joblib.dump(rl_model, "app/models/rl_model.joblib")
        
        # Get updated statistics
        stats = rl_model.get_stats()
        
        return {
            "message": "Feedback received and model updated successfully!",
            "reward": reward,
            "model_stats": stats,
            "improvement": "Model is learning from your feedback and will get better over time."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feedback: {str(e)}")

# 📄 Download PDF Report
@app.get("/download")
async def download_pdf(farmer_name: str = Query(..., description="Farmer name for the report")):
    """
    Download a generated PDF report by farmer name.
    """
    try:
        # Sanitize filename
        safe_farmer_name = "_".join(farmer_name.split())
        filename = f"{safe_farmer_name}_report.pdf"
        
        # Get absolute path for reports directory
        reports_dir = Path(__file__).parent.parent / "reports"
        file_path = reports_dir / filename
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/pdf'
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading report: {str(e)}")

# Market Price Endpoint
from app.services.market_prices import get_market_prices

@app.get("/market-prices")
async def get_prices(crop: str, district: str = "Karnataka"):
    try:
        return get_market_prices(crop, district)
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 📡 Sensor Data Endpoints

@app.post("/api/sensor/npk")
def receive_npk_data(data: NPKDataInput):
    """
    Receive NPK sensor data from ESP8266
    """
    db = SessionLocal()
    try:
        reading = NPKReadingModel(
            n=data.n,
            p=data.p,
            k=data.k,
            device_id=data.device_id,
            timestamp=datetime.utcnow()
        )
        db.add(reading)
        db.commit()
        db.refresh(reading)
        return {"status": "success", "message": "Data received", "id": reading.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()


@app.post("/api/sensor/uno-data")
def receive_uno_data(data: UNODataInput):
    """
    Receive Temperature, Humidity, and Moisture data from Arduino UNO
    """
    db = SessionLocal()
    try:
        reading = UNOReadingModel(
            temperature=data.temperature,
            humidity=data.humidity,
            moisture=data.moisture,
            device_id=data.device_id,
            timestamp=datetime.utcnow()
        )
        db.add(reading)
        db.commit()
        db.refresh(reading)
        return {"status": "success", "message": "Data received", "id": reading.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()


@app.get("/api/sensor/uno-dashboard")
def get_uno_dashboard_data(limit: int = 10):
    """
    Get recent Arduino UNO readings for the dashboard
    """
    db = SessionLocal()
    try:
        readings = db.query(UNOReadingModel).order_by(UNOReadingModel.timestamp.desc()).limit(limit).all()
        
        # Calculate averages
        avg_temp = 0
        avg_hum = 0
        avg_moist = 0
        
        if readings:
            avg_temp = sum(r.temperature for r in readings) / len(readings)
            avg_hum = sum(r.humidity for r in readings) / len(readings)
            avg_moist = sum(r.moisture for r in readings) / len(readings)
        
        return {
            "readings": [
                {
                    "id": r.id,
                    "temperature": r.temperature,
                    "humidity": r.humidity,
                    "moisture": r.moisture,
                    "device_id": r.device_id,
                    "timestamp": r.timestamp.isoformat()
                } for r in readings
            ],
            "averages": {
                "temperature": avg_temp,
                "humidity": avg_hum,
                "moisture": avg_moist
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard data: {str(e)}")
    finally:
        db.close()

@app.get("/api/sensor/dashboard")
def get_sensor_dashboard_data(limit: int = Query(20, le=100)):
    """
    Get latest sensor readings for the dashboard
    """
    db = SessionLocal()
    try:
        # Get recent NPK readings
        readings = db.query(NPKReadingModel).order_by(NPKReadingModel.timestamp.desc()).limit(limit).all()
        
        # Calculate averages (from last 50 readings for better accuracy)
        avg_readings = db.query(NPKReadingModel).order_by(NPKReadingModel.timestamp.desc()).limit(50).all()
        
        avg_n = 0
        avg_p = 0
        avg_k = 0
        
        if avg_readings:
            avg_n = sum(r.n for r in avg_readings) / len(avg_readings)
            avg_p = sum(r.p for r in avg_readings) / len(avg_readings)
            avg_k = sum(r.k for r in avg_readings) / len(avg_readings)
            
        return {
            "readings": [
                {
                    "id": r.id,
                    "N": r.n, # Map back to uppercase for frontend compatibility if needed, or update frontend
                    "P": r.p,
                    "K": r.k,
                    "device_id": r.device_id,
                    "timestamp": r.timestamp.isoformat()
                } for r in readings
            ],
            "averages": {
                "N": avg_n,
                "P": avg_p,
                "K": avg_k
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard data: {str(e)}")
    finally:
        db.close()

# 🎮 Command System for Dual Trigger
# Simple in-memory store for commands (sufficient for single device)
command_store = {
    "pending_command": None
}

@app.post("/api/sensor/trigger-next")
def trigger_next_reading():
    """
    Queue a 'next' command for the ESP8266
    """
    command_store["pending_command"] = "next"
    return {"status": "success", "message": "Command queued"}

@app.get("/api/sensor/command")
def get_pending_command():
    """
    ESP8266 polls this to check for commands
    """
    return {"command": command_store["pending_command"]}

@app.post("/api/sensor/command/clear")
def clear_command():
    """
    ESP8266 calls this after executing the command
    """
    command_store["pending_command"] = None
    return {"status": "success", "message": "Command cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)