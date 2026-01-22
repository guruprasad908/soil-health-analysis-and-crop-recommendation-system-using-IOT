"""
Feature Engineering Utilities for Crop Prediction
Adds domain-specific features to improve model accuracy and confidence
"""
import pandas as pd
import numpy as np


def create_interaction_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Create interaction features from base features
    These help capture non-linear relationships
    """
    features = data.copy()
    
    # NPK Ratios (important for nutrient balance)
    features['N_P_ratio'] = features['N'] / (features['P'] + 1e-6)  # Avoid division by zero
    features['N_K_ratio'] = features['N'] / (features['K'] + 1e-6)
    features['P_K_ratio'] = features['P'] / (features['K'] + 1e-6)
    
    # NPK Statistics
    features['npk_sum'] = features['N'] + features['P'] + features['K']
    features['npk_mean'] = (features['N'] + features['P'] + features['K']) / 3
    features['npk_std'] = features[['N', 'P', 'K']].std(axis=1)
    features['npk_balance'] = 1 / (features['npk_std'] + 1)  # Higher when balanced
    
    # Climate Interactions
    features['temp_humidity'] = features['temperature'] * features['humidity']
    features['rainfall_temp'] = features['rainfall'] * features['temperature']
    features['rainfall_humidity'] = features['rainfall'] * features['humidity']
    
    # pH Interactions
    features['ph_temp'] = features['ph'] * features['temperature']
    features['ph_rainfall'] = features['ph'] * features['rainfall']
    
    # Nutrient-Climate Interactions
    features['N_temp'] = features['N'] * features['temperature']
    features['P_temp'] = features['P'] * features['temperature']
    features['K_temp'] = features['K'] * features['temperature']
    
    return features


def create_domain_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Create domain-specific agricultural features
    Based on agricultural science knowledge
    """
    features = data.copy()
    
    # Aridity Index (rainfall vs temperature)
    features['aridity_index'] = features['rainfall'] / (features['temperature'] + 1)
    
    # Growing Degree Days (simplified - base temp 10°C)
    features['growing_degree_days'] = np.maximum(0, features['temperature'] - 10) * 30
    
    # Soil Fertility Score (composite NPK score)
    features['soil_fertility_score'] = (
        (features['N'] / 200) * 0.4 +  # N typically 0-200
        (features['P'] / 145) * 0.3 +  # P typically 5-145
        (features['K'] / 205) * 0.3    # K typically 5-205
    )
    
    # Climate Suitability Index
    features['climate_suitability'] = (
        (features['temperature'] / 50) * 0.4 +
        (features['humidity'] / 100) * 0.3 +
        (features['rainfall'] / 300) * 0.3
    )
    
    # pH Suitability (optimal pH is around 6.5-7.5)
    features['ph_optimality'] = 1 - abs(features['ph'] - 7.0) / 3.5
    
    # Water Availability Index
    features['water_availability'] = features['rainfall'] * features['humidity'] / 100
    
    # Nutrient Efficiency (how well nutrients are utilized)
    features['nutrient_efficiency'] = (
        features['npk_sum'] / (features['temperature'] + features['rainfall'] + 1)
    )
    
    return features


def create_polynomial_features(data: pd.DataFrame, degree: int = 2) -> pd.DataFrame:
    """
    Create polynomial features (squared terms)
    Helps capture non-linear relationships
    """
    features = data.copy()
    
    # Square important features
    numeric_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    for col in numeric_cols:
        if col in features.columns:
            features[f'{col}_squared'] = features[col] ** 2
    
    return features


def engineer_features(data: pd.DataFrame, include_polynomial: bool = True) -> pd.DataFrame:
    """
    Main function to apply all feature engineering
    """
    features = data.copy()
    
    # Step 1: Interaction features
    features = create_interaction_features(features)
    
    # Step 2: Domain-specific features
    features = create_domain_features(features)
    
    # Step 3: Polynomial features (optional, can be computationally expensive)
    if include_polynomial:
        features = create_polynomial_features(features)
    
    # Replace infinite values with NaN, then fill with 0
    features = features.replace([np.inf, -np.inf], np.nan)
    features = features.fillna(0)
    
    return features


def get_feature_importance_features(base_features: list) -> list:
    """
    Get list of engineered feature names based on base features
    """
    engineered = base_features.copy()
    
    # Interaction features
    engineered.extend(['N_P_ratio', 'N_K_ratio', 'P_K_ratio'])
    engineered.extend(['npk_sum', 'npk_mean', 'npk_std', 'npk_balance'])
    engineered.extend(['temp_humidity', 'rainfall_temp', 'rainfall_humidity'])
    engineered.extend(['ph_temp', 'ph_rainfall'])
    engineered.extend(['N_temp', 'P_temp', 'K_temp'])
    
    # Domain features
    engineered.extend([
        'aridity_index', 'growing_degree_days', 'soil_fertility_score',
        'climate_suitability', 'ph_optimality', 'water_availability',
        'nutrient_efficiency'
    ])
    
    # Polynomial features
    for col in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']:
        engineered.append(f'{col}_squared')
    
    return engineered

