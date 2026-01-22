# Soil & Crop Recommender System - Phase 2 Technical Documentation

## 1. System Architecture

The system is built on a **Microservices-inspired Monolithic Architecture** using **FastAPI**. It is designed for high availability, fault tolerance, and ease of deployment.

### 1.1 Backend Core (`app/main.py`)
*   **Framework**: FastAPI (Asynchronous, High Performance).
*   **API Design**: RESTful endpoints with strict Pydantic data validation.
*   **Concurrency**: Uses `async/await` for non-blocking I/O operations (Weather APIs, Database).
*   **CORS**: Configured for cross-origin resource sharing to support the React frontend.

### 1.2 Database Layer (`app/models/db_model.py`)
We use **SQLite** with **SQLAlchemy ORM** for data persistence. The schema is optimized for reporting and analytics.

*   **`Prediction` Table**: Stores every prediction request.
    *   *Columns*: `farmer_name`, `phone`, `location`, `land_size`, `N`, `P`, `K`, `ph`, `predicted_crop`, `confidence`, `soil_health_score`, `timestamp`.
    *   *Purpose*: Enables the "Download Report" feature and future analytics on regional soil trends.
*   **`NPKReading` Table**: Stores raw sensor data from IoT devices (ESP8266/Arduino).
    *   *Columns*: `N`, `P`, `K`, `device_id`, `timestamp`.

### 1.3 External Services Integration (`app/services/weather_service.py`)
We implemented a **Triple-Fallback Architecture** for critical external data to ensure 99.9% uptime.

*   **Geocoding Strategy**:
    1.  **Nominatim (OpenStreetMap)**: Primary source (Best for Indian village names).
    2.  **OpenWeather Geocoding**: Secondary fallback.
    3.  **Open-Meteo Geocoding**: Tertiary fallback (Free, no key required).
*   **Weather Data Strategy**:
    1.  **OpenWeather API**: Primary source for real-time data.
    2.  **Open-Meteo API**: Automatic fallback if OpenWeather fails (Rate limit/Key error).
    3.  **Historical Data**: Fetches 80+ years of data from Open-Meteo Archive for robust climate analysis.

---

## 2. Machine Learning Architecture

The core of the system is a sophisticated **Ensemble Learning Pipeline** designed to maximize prediction accuracy and minimize risk.

### 2.1 Model Inventory
We utilize a diverse set of algorithms to capture different patterns in the soil data:
1.  **Stacking Classifier (Meta-Learner)**: Combines predictions from all base models.
2.  **Random Forest**: Handles non-linear relationships and feature interactions.
3.  **LightGBM**: Gradient boosting framework optimized for speed and efficiency.
4.  **CatBoost**: Handles categorical features (like Soil Type) natively.
5.  **XGBoost**: Optimized distributed gradient boosting.
6.  **Reinforcement Learning (RL)**: Q-Learning agent that adapts to user feedback.

### 2.2 Model Selection & Experimental Results (`notebooks/fianl notebook .ipynb`)

We conducted extensive experiments comparing 7 different algorithms to find the optimal solution.

**Experimental Results (Accuracy on Test Set):**
1.  **Random Forest**: **99.55%** (Best Single Model)
2.  **Stacking Classifier**: **99.55%** (Selected for Production)
3.  **LightGBM / Gradient Boosting**: 98.64%
4.  **Decision Tree**: 98.86%
5.  **KNN**: 98.18%
6.  **Logistic Regression**: 98.18%
7.  **SVM**: 97.95%

### 2.3 The "Why Stacking?" Defense
*Question: "If Random Forest gives 99.55%, why complicate it with Stacking?"*

**The Technical Answer:**
While Random Forest is excellent, relying on a single algorithm creates a **Single Point of Failure**.
*   **Bias-Variance Tradeoff**: Random Forest reduces variance (overfitting) but can have bias. Gradient Boosting reduces bias. SVM finds optimal hyperplanes.
*   **The Stacking Advantage**: Our Stacking Classifier uses a **Logistic Regression Meta-Learner** to learn the *patterns of errors* made by the base models.
    *   *Scenario*: If Random Forest confuses "Rice" and "Jute" (similar conditions), but SVM separates them well, the Stacking model learns to trust SVM for that specific case.
*   **Conclusion**: We chose Stacking not just for accuracy, but for **Reliability** and **Robustness** across diverse real-world soil conditions. It is the industry standard for high-stakes prediction systems.

### 2.4 Ensemble Strategy (`app/utils/ensemble_methods.py`)
We use a **Weighted Soft Voting** mechanism. Instead of simple majority voting, we weight the probability outputs of each model based on their validation accuracy.

**Weights Configuration:**
*   **Stacking Classifier**: 25% (Highest weight due to superior generalization)
*   **Random Forest**: 20%
*   **LightGBM**: 20%
*   **CatBoost**: 15%
*   **Gradient Boosting**: 10%
*   **XGBoost**: 10%

**Formula:**
$$ P_{final}(class) = \frac{\sum (P_{model}(class) \times Weight_{model})}{\sum Weights} $$

### 2.3 Uncertainty Quantification
We don't just predict; we measure **Confidence**.
*   **Model Agreement**: We calculate how many models agree on the top prediction.
*   **Standard Deviation**: We measure the spread of confidence scores across models.
*   **Result**: If high uncertainty is detected, the system flags the prediction for manual review.

---

## 3. Core Algorithms & Logic

### 3.1 Soil Health Scoring (`app/services/soil_health_scorer.py`)
A proprietary algorithm that calculates a 0-100 score based on 5 weighted factors:
1.  **NPK Balance (40%)**: Penalizes nutrient deficiency or toxicity.
2.  **pH Suitability (20%)**: Checks deviation from neutral pH (6.5-7.5).
3.  **Nutrient Ratios (15%)**: Evaluates N:P and N:K balance (e.g., N:P > 4:1 is bad).
4.  **Environmental Fit (15%)**: Scores temperature/rainfall suitability.
5.  **Soil Type Factor (10%)**: Base fertility of the soil type.

### 3.2 Fertilizer Recommendation Engine (`app/services/fertilizer_advisor.py`)
A deterministic rule-based engine that ensures agronomic correctness.
*   **Logic**: `Required_Fertilizer = (Ideal_NPK_for_Crop - Current_Soil_NPK) * Land_Size`
*   **Safety**: If `Current > Ideal`, it warns of toxicity instead of recommending fertilizer.
*   **Output**: Generates a precise schedule (Basal Dose vs. Top Dressing).

### 3.3 Regional "Safety Guard" (`app/services/regional_crops.py`)
A final post-processing filter that overrides ML predictions if they violate regional constraints.
*   **Database**: Contains hardcoded rules for North Karnataka districts (e.g., Vijayapura, Raichur).
*   **Rule**: If ML predicts "Coffee" for "Vijayapura", the Guard blocks it (due to rainfall mismatch) and suggests the next best crop (e.g., "Jowar").

---

## 4. Market Price Integration

*   **Source**: Agmarknet (Government of India).
*   **Implementation**: `app/services/market_prices.py`.
*   **Reliability**: Includes a **Simulation Mode** with realistic data for North Karnataka mandis to ensure the dashboard never looks empty during demos or API downtimes.
