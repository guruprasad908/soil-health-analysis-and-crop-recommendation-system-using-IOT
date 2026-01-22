"""
Soil Health Scoring System
Calculates overall soil health score based on NPK, pH, and other factors
"""

def calculate_soil_health_score(N, P, K, ph, temperature, humidity, rainfall, soil_type):
    """
    Calculate overall soil health score (0-100)
    
    Args:
        N, P, K: Nutrient levels (mg/kg)
        ph: Soil pH
        temperature: Temperature in Celsius
        humidity: Humidity percentage
        rainfall: Rainfall in mm
        soil_type: Type of soil
    
    Returns:
        dict with overall score, category, and breakdown
    """
    scores = {}
    max_scores = {}
    
    # 1. NPK Balance Score (40 points max)
    # Optimal ranges: N: 50-100, P: 30-60, K: 30-80
    npk_score = 0
    
    # Nitrogen score (15 points)
    if 50 <= N <= 100:
        n_score = 15
    elif 40 <= N < 50 or 100 < N <= 120:
        n_score = 12
    elif 30 <= N < 40 or 120 < N <= 140:
        n_score = 8
    else:
        n_score = 4
    scores['nitrogen'] = n_score
    max_scores['nitrogen'] = 15
    
    # Phosphorus score (12 points)
    if 30 <= P <= 60:
        p_score = 12
    elif 25 <= P < 30 or 60 < P <= 70:
        p_score = 10
    elif 20 <= P < 25 or 70 < P <= 80:
        p_score = 6
    else:
        p_score = 3
    scores['phosphorus'] = p_score
    max_scores['phosphorus'] = 12
    
    # Potassium score (13 points)
    if 30 <= K <= 80:
        k_score = 13
    elif 25 <= K < 30 or 80 < K <= 100:
        k_score = 10
    elif 20 <= K < 25 or 100 < K <= 120:
        k_score = 6
    else:
        k_score = 3
    scores['potassium'] = k_score
    max_scores['potassium'] = 13
    
    npk_score = n_score + p_score + k_score
    
    # 2. pH Score (20 points max)
    # Optimal pH: 6.0-7.5
    if 6.0 <= ph <= 7.5:
        ph_score = 20
    elif 5.5 <= ph < 6.0 or 7.5 < ph <= 8.0:
        ph_score = 15
    elif 5.0 <= ph < 5.5 or 8.0 < ph <= 8.5:
        ph_score = 10
    else:
        ph_score = 5
    scores['ph'] = ph_score
    max_scores['ph'] = 20
    
    # 3. Nutrient Balance Score (15 points max)
    # Check NPK ratios
    balance_score = 15
    if N > 0 and P > 0 and K > 0:
        np_ratio = N / P
        nk_ratio = N / K
        
        # Ideal ratios: N:P around 2:1, N:K around 1.5:1
        if 1.5 <= np_ratio <= 3.0:
            balance_score -= 0
        elif 1.0 <= np_ratio < 1.5 or 3.0 < np_ratio <= 4.0:
            balance_score -= 3
        else:
            balance_score -= 6
        
        if 1.0 <= nk_ratio <= 2.5:
            balance_score -= 0
        elif 0.5 <= nk_ratio < 1.0 or 2.5 < nk_ratio <= 3.5:
            balance_score -= 3
        else:
            balance_score -= 6
    else:
        balance_score = 0
    
    scores['nutrient_balance'] = max(0, balance_score)
    max_scores['nutrient_balance'] = 15
    
    # 4. Environmental Conditions Score (15 points max)
    env_score = 0
    
    # Temperature (5 points) - optimal: 20-30°C
    if 20 <= temperature <= 30:
        temp_score = 5
    elif 15 <= temperature < 20 or 30 < temperature <= 35:
        temp_score = 3
    else:
        temp_score = 1
    scores['temperature'] = temp_score
    max_scores['temperature'] = 5
    
    # Humidity (5 points) - optimal: 50-80%
    if 50 <= humidity <= 80:
        hum_score = 5
    elif 40 <= humidity < 50 or 80 < humidity <= 90:
        hum_score = 3
    else:
        hum_score = 1
    scores['humidity'] = hum_score
    max_scores['humidity'] = 5
    
    # Rainfall (5 points) - optimal: 100-300mm
    if 100 <= rainfall <= 300:
        rain_score = 5
    elif 50 <= rainfall < 100 or 300 < rainfall <= 400:
        rain_score = 3
    else:
        rain_score = 1
    scores['rainfall'] = rain_score
    max_scores['rainfall'] = 5
    
    env_score = temp_score + hum_score + rain_score
    
    # 5. Soil Type Suitability (10 points max)
    # Different soil types have different inherent fertility
    soil_scores = {
        "alluvial soil": 10,
        "black soil": 9,
        "red soil": 7,
        "laterite soil": 5,
        "sandy soil": 6,
        "peaty soil": 8
    }
    soil_score = soil_scores.get(soil_type.lower(), 5)
    scores['soil_type'] = soil_score
    max_scores['soil_type'] = 10
    
    # Calculate total score
    total_score = npk_score + ph_score + scores['nutrient_balance'] + env_score + soil_score
    max_possible = sum(max_scores.values())
    
    # Normalize to 0-100 scale
    normalized_score = (total_score / max_possible) * 100
    
    # Determine category
    if normalized_score >= 80:
        category = "Excellent"
        color = "green"
    elif normalized_score >= 65:
        category = "Good"
        color = "blue"
    elif normalized_score >= 50:
        category = "Fair"
        color = "yellow"
    elif normalized_score >= 35:
        category = "Poor"
        color = "orange"
    else:
        category = "Very Poor"
        color = "red"
    
    return {
        "overall_score": round(normalized_score, 1),
        "category": category,
        "color": color,
        "breakdown": scores,
        "max_scores": max_scores,
        "recommendations": get_health_recommendations(normalized_score, scores, N, P, K, ph)
    }

def get_health_recommendations(score, breakdown, N, P, K, ph):
    """Get recommendations based on soil health score"""
    recommendations = []
    
    if score < 50:
        recommendations.append("🔴 Urgent: Soil health is poor. Immediate intervention required.")
    
    if breakdown['nitrogen'] < 10:
        recommendations.append("🔸 Add nitrogen-rich fertilizers or organic compost.")
    
    if breakdown['phosphorus'] < 8:
        recommendations.append("🔸 Apply phosphorus fertilizers or bone meal.")
    
    if breakdown['potassium'] < 8:
        recommendations.append("🔸 Add potassium sources like wood ash or potash.")
    
    if breakdown['ph'] < 15:
        if ph < 6.0:
            recommendations.append("🔸 Add lime to raise pH.")
        else:
            recommendations.append("🔸 Add gypsum or organic matter to lower pH.")
    
    if breakdown['nutrient_balance'] < 10:
        recommendations.append("🔸 Balance NPK ratios through targeted fertilization.")
    
    if score >= 80:
        recommendations.append("✅ Excellent soil health! Maintain with regular organic matter addition.")
    
    return recommendations

