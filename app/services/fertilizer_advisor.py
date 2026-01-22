# Comprehensive fertilizer and soil treatment advisor with crop-specific recommendations

# Ideal NPK values (kg/acre) for all crops in the dataset
ideal_npk = {
    "rice": {"N": 90, "P": 40, "K": 40, "optimal_ph": (5.5, 7.0)},
    "wheat": {"N": 80, "P": 35, "K": 35, "optimal_ph": (6.0, 7.5)},
    "cotton": {"N": 100, "P": 45, "K": 50, "optimal_ph": (5.8, 8.0)},
    "maize": {"N": 120, "P": 60, "K": 40, "optimal_ph": (5.8, 7.0)},
    "sugarcane": {"N": 150, "P": 60, "K": 75, "optimal_ph": (6.0, 7.5)},
    "coconut": {"N": 150, "P": 55, "K": 120, "optimal_ph": (5.5, 7.0)},
    "apple": {"N": 100, "P": 50, "K": 80, "optimal_ph": (6.0, 7.0)},
    "banana": {"N": 200, "P": 50, "K": 300, "optimal_ph": (6.0, 7.5)},
    "blackgram": {"N": 20, "P": 40, "K": 20, "optimal_ph": (6.0, 7.5)},
    "chickpea": {"N": 20, "P": 50, "K": 20, "optimal_ph": (6.0, 7.5)},
    "coffee": {"N": 100, "P": 50, "K": 100, "optimal_ph": (6.0, 6.5)},
    "grapes": {"N": 80, "P": 40, "K": 100, "optimal_ph": (6.0, 7.0)},
    "jute": {"N": 60, "P": 30, "K": 30, "optimal_ph": (6.0, 7.5)},
    "kidneybeans": {"N": 20, "P": 50, "K": 20, "optimal_ph": (6.0, 7.5)},
    "lentil": {"N": 20, "P": 50, "K": 20, "optimal_ph": (6.0, 7.5)},
    "mango": {"N": 100, "P": 50, "K": 100, "optimal_ph": (5.5, 7.5)},
    "mothbeans": {"N": 20, "P": 40, "K": 20, "optimal_ph": (6.0, 7.5)},
    "mungbean": {"N": 20, "P": 40, "K": 20, "optimal_ph": (6.0, 7.5)},
    "muskmelon": {"N": 80, "P": 40, "K": 60, "optimal_ph": (6.0, 7.0)},
    "orange": {"N": 100, "P": 50, "K": 150, "optimal_ph": (6.0, 7.5)},
    "papaya": {"N": 200, "P": 50, "K": 200, "optimal_ph": (6.0, 7.0)},
    "pigeonpeas": {"N": 20, "P": 50, "K": 20, "optimal_ph": (6.0, 7.5)},
    "pomegranate": {"N": 100, "P": 50, "K": 100, "optimal_ph": (6.0, 7.5)},
    "watermelon": {"N": 80, "P": 40, "K": 60, "optimal_ph": (6.0, 7.0)},
    # North Karnataka specific crops
    "jowar": {"N": 60, "P": 30, "K": 30, "optimal_ph": (6.5, 8.5)},
    "bajra": {"N": 50, "P": 25, "K": 25, "optimal_ph": (6.0, 8.0)},
    "ragi": {"N": 50, "P": 30, "K": 30, "optimal_ph": (5.5, 7.5)},
    "greengram": {"N": 20, "P": 40, "K": 20, "optimal_ph": (6.5, 7.5)},
    "sunflower": {"N": 60, "P": 40, "K": 40, "optimal_ph": (6.5, 8.0)},
    "groundnut": {"N": 25, "P": 50, "K": 75, "optimal_ph": (6.0, 7.5)},
    "safflower": {"N": 50, "P": 30, "K": 30, "optimal_ph": (6.5, 8.0)},
    "onion": {"N": 100, "P": 50, "K": 50, "optimal_ph": (6.0, 7.5)},
    "tomato": {"N": 120, "P": 60, "K": 60, "optimal_ph": (6.0, 7.0)},
    "chilli": {"N": 100, "P": 50, "K": 50, "optimal_ph": (6.0, 7.5)},
    "soybean": {"N": 30, "P": 60, "K": 40, "optimal_ph": (6.0, 7.5)}
}

# Optimal NPK ranges (min-max) for each crop
optimal_npk_ranges = {
    "rice": {"N": (70, 110), "P": (30, 50), "K": (30, 50)},
    "wheat": {"N": (60, 100), "P": (25, 45), "K": (25, 45)},
    "cotton": {"N": (80, 120), "P": (35, 55), "K": (40, 60)},
    "maize": {"N": (100, 140), "P": (50, 70), "K": (30, 50)},
    "sugarcane": {"N": (130, 170), "P": (50, 70), "K": (65, 85)},
    "coconut": {"N": (130, 170), "P": (45, 65), "K": (100, 140)},
    "apple": {"N": (80, 120), "P": (40, 60), "K": (60, 100)},
    "banana": {"N": (180, 220), "P": (40, 60), "K": (280, 320)},
    "blackgram": {"N": (10, 30), "P": (30, 50), "K": (10, 30)},
    "chickpea": {"N": (10, 30), "P": (40, 60), "K": (10, 30)},
    "coffee": {"N": (80, 120), "P": (40, 60), "K": (80, 120)},
    "grapes": {"N": (60, 100), "P": (30, 50), "K": (80, 120)},
    "jute": {"N": (50, 70), "P": (20, 40), "K": (20, 40)},
    "kidneybeans": {"N": (10, 30), "P": (40, 60), "K": (10, 30)},
    "lentil": {"N": (10, 30), "P": (40, 60), "K": (10, 30)},
    "mango": {"N": (80, 120), "P": (40, 60), "K": (80, 120)},
    "mothbeans": {"N": (10, 30), "P": (30, 50), "K": (10, 30)},
    "mungbean": {"N": (10, 30), "P": (30, 50), "K": (10, 30)},
    "muskmelon": {"N": (60, 100), "P": (30, 50), "K": (50, 70)},
    "orange": {"N": (80, 120), "P": (40, 60), "K": (130, 170)},
    "papaya": {"N": (180, 220), "P": (40, 60), "K": (180, 220)},
    "pigeonpeas": {"N": (10, 30), "P": (40, 60), "K": (10, 30)},
    "pomegranate": {"N": (80, 120), "P": (40, 60), "K": (80, 120)},
    "watermelon": {"N": (60, 100), "P": (30, 50), "K": (50, 70)},
    # North Karnataka crops
    "jowar": {"N": (40, 80), "P": (20, 40), "K": (20, 40)},
    "bajra": {"N": (35, 65), "P": (15, 35), "K": (15, 35)},
    "ragi": {"N": (40, 70), "P": (20, 40), "K": (20, 40)},
    "greengram": {"N": (10, 30), "P": (30, 50), "K": (10, 30)},
    "sunflower": {"N": (50, 80), "P": (30, 50), "K": (30, 50)},
    "groundnut": {"N": (15, 35), "P": (40, 60), "K": (60, 90)},
    "safflower": {"N": (40, 60), "P": (20, 40), "K": (20, 40)},
    "onion": {"N": (80, 120), "P": (40, 60), "K": (40, 60)},
    "tomato": {"N": (90, 150), "P": (45, 75), "K": (45, 75)},
    "chilli": {"N": (80, 120), "P": (40, 60), "K": (40, 60)},
    "soybean": {"N": (20, 40), "P": (50, 70), "K": (30, 50)}
}

# Soil type specific recommendations
soil_type_tips = {
    "alluvial soil": "Rich in nutrients, good water retention. Suitable for most crops.",
    "black soil": "High clay content, retains moisture well. Ideal for cotton, wheat, and pulses.",
    "red soil": "Well-drained, slightly acidic. Good for fruits, vegetables, and pulses.",
    "laterite soil": "Acidic, low fertility. Requires organic matter addition. Suitable for tea, coffee, cashew.",
    "sandy soil": "Well-drained but low nutrient retention. Requires frequent irrigation and organic matter.",
    "peaty soil": "High organic matter, acidic. Good for vegetables but may need pH adjustment."
}


def get_soil_treatment(ph, N, P, K, predicted_crop=None, soil_type=None):
    """
    Get crop-specific soil treatment recommendations with excess nutrient detection.
    
    Args:
        ph: Soil pH value
        N, P, K: Current nutrient levels (mg/kg)
        predicted_crop: Name of predicted crop (for crop-specific recommendations)
        soil_type: Type of soil (for soil-specific tips)
    
    Returns:
        List of treatment suggestions
    """
    suggestions = []
    
    # Crop-specific pH recommendations
    if predicted_crop and predicted_crop.lower() in ideal_npk:
        crop_lower = predicted_crop.lower()
        ph_min, ph_max = ideal_npk[crop_lower]["optimal_ph"]
        
        if ph < ph_min:
            suggestions.append(f"🔸 Soil pH ({ph:.1f}) is below optimal range ({ph_min}-{ph_max}) for {predicted_crop}. Add lime (2-4 tons/acre) or wood ash to raise pH.")
        elif ph > ph_max:
            suggestions.append(f"🔸 Soil pH ({ph:.1f}) is above optimal range ({ph_min}-{ph_max}) for {predicted_crop}. Add gypsum (1-2 tons/acre) or organic compost to lower pH.")
        elif ph_min <= ph <= ph_max:
            suggestions.append(f"✅ Soil pH ({ph:.1f}) is within optimal range ({ph_min}-{ph_max}) for {predicted_crop}.")
    else:
        # Generic pH recommendations if crop not specified
        if ph < 6.0:
            suggestions.append("🔸 Soil is acidic (pH < 6.0). Add lime or wood ash to raise pH.")
        elif ph > 7.5:
            suggestions.append("🔸 Soil is alkaline (pH > 7.5). Add gypsum or organic compost to lower pH.")
        elif 6.0 <= ph <= 7.5:
            suggestions.append("✅ Soil pH is within acceptable range (6.0-7.5).")
    
    # Crop-specific NPK recommendations
    if predicted_crop and predicted_crop.lower() in optimal_npk_ranges:
        crop_lower = predicted_crop.lower()
        ideal = ideal_npk[crop_lower]
        ranges = optimal_npk_ranges[crop_lower]
        
        # Nitrogen
        n_min, n_max = ranges["N"]
        if N < n_min:
            suggestions.append(f"🔸 Nitrogen ({N} mg/kg) is low for {predicted_crop}. Optimal range: {n_min}-{n_max}. Add compost, green manure, or urea ({ideal['N'] - N:.0f} kg/acre needed).")
        elif N > n_max:
            suggestions.append(f"⚠️ Nitrogen ({N} mg/kg) is excessive for {predicted_crop}. Optimal range: {n_min}-{n_max}. Reduce nitrogen application to avoid excessive vegetative growth.")
        else:
            suggestions.append(f"✅ Nitrogen ({N} mg/kg) is within optimal range for {predicted_crop}.")
        
        # Phosphorus
        p_min, p_max = ranges["P"]
        if P < p_min:
            suggestions.append(f"🔸 Phosphorus ({P} mg/kg) is low for {predicted_crop}. Optimal range: {p_min}-{p_max}. Add rock phosphate, bone meal, or PSB biofertilizer ({ideal['P'] - P:.0f} kg/acre needed).")
        elif P > p_max:
            suggestions.append(f"⚠️ Phosphorus ({P} mg/kg) is excessive for {predicted_crop}. Optimal range: {p_min}-{p_max}. High P can interfere with micronutrient uptake.")
        else:
            suggestions.append(f"✅ Phosphorus ({P} mg/kg) is within optimal range for {predicted_crop}.")
        
        # Potassium
        k_min, k_max = ranges["K"]
        if K < k_min:
            suggestions.append(f"🔸 Potassium ({K} mg/kg) is low for {predicted_crop}. Optimal range: {k_min}-{k_max}. Add wood ash, banana peel powder, or potash ({ideal['K'] - K:.0f} kg/acre needed).")
        elif K > k_max:
            suggestions.append(f"⚠️ Potassium ({K} mg/kg) is excessive for {predicted_crop}. Optimal range: {k_min}-{k_max}. High K can cause magnesium deficiency.")
        else:
            suggestions.append(f"✅ Potassium ({K} mg/kg) is within optimal range for {predicted_crop}.")
    else:
        # Generic NPK recommendations if crop not specified
        if N < 50:
            suggestions.append("🔸 Nitrogen is low (< 50 mg/kg). Add compost, green manure, or urea.")
        elif N > 120:
            suggestions.append("⚠️ Nitrogen is excessive (> 120 mg/kg). Reduce nitrogen application.")
        
        if P < 30:
            suggestions.append("🔸 Phosphorus is low (< 30 mg/kg). Add rock phosphate or bone meal.")
        elif P > 60:
            suggestions.append("⚠️ Phosphorus is excessive (> 60 mg/kg). High P can interfere with micronutrient uptake.")
        
        if K < 30:
            suggestions.append("🔸 Potassium is low (< 30 mg/kg). Add banana peels or potash.")
        elif K > 100:
            suggestions.append("⚠️ Potassium is excessive (> 100 mg/kg). High K can cause magnesium deficiency.")
    
    # Soil type specific recommendations
    if soil_type and soil_type.lower() in soil_type_tips:
        soil_lower = soil_type.lower()
        suggestions.append(f"🌱 {soil_type_tips[soil_lower]}")
    
    # Nutrient ratio warnings
    if N > 0 and P > 0 and K > 0:
        np_ratio = N / P
        nk_ratio = N / K
        if np_ratio > 3:
            suggestions.append("⚠️ N:P ratio is high (>3:1). Consider balancing with phosphorus.")
        if nk_ratio > 2:
            suggestions.append("⚠️ N:K ratio is high (>2:1). Consider balancing with potassium.")
    
    return suggestions


def get_fertilizer_estimate(predicted_crop, current_npk, land_size):
    """
    Get detailed fertilizer recommendations based on crop, current NPK, and land size.
    
    Args:
        predicted_crop: Name of predicted crop
        current_npk: Dict with N, P, K values (mg/kg)
        land_size: Land size in acres
    
    Returns:
        Detailed fertilizer recommendation string
    """
    crop_lower = predicted_crop.lower()
    
    if crop_lower not in ideal_npk:
        return f"⚠️ Fertilizer data not available for {predicted_crop}. Please consult agricultural experts for specific recommendations."
    
    ideal = ideal_npk[crop_lower]
    current_N = current_npk.get("N", 0)
    current_P = current_npk.get("P", 0)
    current_K = current_npk.get("K", 0)
    
    # Calculate required NPK (difference between ideal and current)
    required_npk = {
        "N": max(0, ideal["N"] - current_N),
        "P": max(0, ideal["P"] - current_P),
        "K": max(0, ideal["K"] - current_K)
    }
    
    # Calculate total dosage for the land size (values are per acre)
    total_dosage = {
        "N": required_npk["N"] * land_size,
        "P": required_npk["P"] * land_size,
        "K": required_npk["K"] * land_size
    }
    
    # Build professional recommendation message
    recommendations = []
    
    recommendations.append("═" * 60)
    recommendations.append(f"FERTILIZER RECOMMENDATIONS FOR {predicted_crop.upper()}")
    recommendations.append("═" * 60)
    recommendations.append("")
    
    # Farm Details
    recommendations.append("FARM DETAILS")
    recommendations.append("─" * 60)
    recommendations.append(f"Land Size: {land_size} acres")
    recommendations.append(f"Current Soil NPK: N={current_N} | P={current_P} | K={current_K} mg/kg")
    recommendations.append(f"Optimal NPK for {predicted_crop}: N={ideal['N']} | P={ideal['P']} | K={ideal['K']} kg/acre")
    recommendations.append("")
    
    if total_dosage["N"] > 0 or total_dosage["P"] > 0 or total_dosage["K"] > 0:
        recommendations.append("FERTILIZER APPLICATION SCHEDULE")
        recommendations.append("─" * 60)
        
        if total_dosage["N"] > 0:
            recommendations.append(f"\n🔹 NITROGEN (N): {total_dosage['N']:.1f} kg total ({required_npk['N']:.1f} kg/acre)")
            recommendations.append("   Application Method:")
            recommendations.append(f"   • Basal (50%): {total_dosage['N']*0.5:.1f} kg at sowing")
            recommendations.append(f"   • First Top Dressing (25%): {total_dosage['N']*0.25:.1f} kg at tillering stage")
            recommendations.append(f"   • Second Top Dressing (25%): {total_dosage['N']*0.25:.1f} kg at flowering stage")
        
        if total_dosage["P"] > 0:
            recommendations.append(f"\n🔹 PHOSPHORUS (P₂O₅): {total_dosage['P']:.1f} kg total ({required_npk['P']:.1f} kg/acre)")
            recommendations.append("   Application Method:")
            recommendations.append(f"   • Full dose as basal: {total_dosage['P']:.1f} kg before sowing/transplanting")
        
        if total_dosage["K"] > 0:
            recommendations.append(f"\n🔹 POTASSIUM (K₂O): {total_dosage['K']:.1f} kg total ({required_npk['K']:.1f} kg/acre)")
            recommendations.append("   Application Method:")
            recommendations.append(f"   • Basal (50%): {total_dosage['K']*0.5:.1f} kg at sowing")
            recommendations.append(f"   • Top Dressing (50%): {total_dosage['K']*0.5:.1f} kg at flowering stage")
        
        if total_dosage["N"] == 0 and total_dosage["P"] == 0 and total_dosage["K"] == 0:
            recommendations.append("✓ Soil NPK levels are adequate")
            recommendations.append("  Continue regular organic matter application to maintain soil health")
    else:
        recommendations.append("SOIL NUTRIENT STATUS")
        recommendations.append("─" * 60)
        recommendations.append(f"✓ Excellent: Soil NPK levels are already optimal for {predicted_crop}")
        recommendations.append("  Maintain soil health through:")
        recommendations.append("  • Regular organic compost application")
        recommendations.append("  • Crop rotation practices")
        recommendations.append("  • Green manuring between seasons")
    
    # Organic alternatives
    recommendations.append("")
    recommendations.append("ORGANIC & BIO-FERTILIZER ALTERNATIVES")
    recommendations.append("─" * 60)
    recommendations.append(f"Farm Yard Manure (FYM): {land_size * 5:.0f}-{land_size * 10:.0f} tons")
    recommendations.append(f"  └─ Application: {5}-{10} tons/acre (provides balanced NPK)")
    recommendations.append("\nCompost: Well-decomposed organic compost")
    recommendations.append(f"  └─ Application: {land_size * 3:.0f}-{land_size * 5:.0f} tons total")
    recommendations.append("\nGreen Manure: Dhaincha, Sunhemp, or other leguminous crops")
    recommendations.append("  └─ Benefits: Natural nitrogen fixation, improves soil structure")
    recommendations.append("\nBio-Fertilizers:")
    recommendations.append("  • Rhizobium: 200g/acre (for nitrogen fixation)")
    recommendations.append("  • PSB (Phosphate Solubilizing Bacteria): 200g/acre")
    recommendations.append("  • Azospirillum: 200g/acre (for nitrogen fixation)")
    recommendations.append("  • VAM (Vesicular Arbuscular Mycorrhiza): Enhances P uptake")
    
    recommendations.append("")
    recommendations.append("═" * 60)
    recommendations.append("Note: Apply fertilizers based on soil test results and local")
    recommendations.append("agricultural extension recommendations for best results.")
    recommendations.append("═" * 60)
    
    return "\n".join(recommendations)
