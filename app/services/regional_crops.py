"""
Regional Crop Constraints - Complete module for North Karnataka
Includes:
 - REGIONAL_CROPS for major districts
 - DEFAULT_NORTH_KARNATAKA fallback
 - Utilities: normalize(), detect_district_from_location()
 - Crop filtering: crop_match(), filter_crops_by_region()
 - Regional analysis: get_region_analysis()
 - Recommendations: generate_recommendations()
 
Drop-in ready: Replace your existing regional constraints module with this file.
"""

import re

# ----------------------- REGIONAL DATASET -----------------------
# District entries include: suitable_crops, unsuitable_crops, district_name,
# region, climate, rainfall_range (mm/year), soil_types
REGIONAL_CROPS = {
    "vijayapura": {
        "suitable_crops": [
            "wheat", "jowar", "bajra", "ragi", "maize", "cotton",
            "sugarcane", "sunflower", "groundnut", "soybean", "pigeonpeas",
            "chickpea", "mothbeans", "mungbean", "lentil", "pomegranate",
            "onion", "tomato", "chilli", "brinjal", "okra", "cucumber",
            "watermelon", "muskmelon", "coriander", "cumin", "fenugreek"
        ],
        "unsuitable_crops": [
            "coffee", "tea", "cardamom", "pepper", "coconut", "arecanut",
            "rubber", "cashew", "mango", "banana", "orange", "apple"
        ],
        "district_name": "Vijayapura (Bijapur)",
        "region": "North Karnataka",
        "climate": "Semi-arid",
        "rainfall_range": (400, 800),
        "soil_types": ["black soil", "red soil", "alluvial soil"]
    },
    "belagavi": {
        "suitable_crops": [
            "rice", "jowar", "ragi", "maize", "cotton", "sugarcane",
            "groundnut", "soybean", "pigeonpeas", "chickpea", "mothbeans",
            "mungbean", "lentil", "onion", "tomato", "chilli", "brinjal",
            "okra", "cucumber", "watermelon", "muskmelon", "pomegranate"
        ],
        "unsuitable_crops": ["coffee", "tea", "cardamom", "pepper", "rubber"],
        "district_name": "Belagavi (Belgaum)",
        "region": "North Karnataka",
        "climate": "Semi-arid to sub-humid",
        "rainfall_range": (600, 1200),
        "soil_types": ["black soil", "red soil", "alluvial soil", "laterite soil"]
    },
    "bagalkot": {
        "suitable_crops": [
            "jowar", "bajra", "ragi", "maize", "cotton", "sunflower",
            "groundnut", "soybean", "pigeonpeas", "chickpea", "mothbeans",
            "mungbean", "lentil", "onion", "tomato", "chilli", "brinjal"
        ],
        "unsuitable_crops": ["coffee", "tea", "cardamom", "pepper", "rubber", "coconut"],
        "district_name": "Bagalkot",
        "region": "North Karnataka",
        "climate": "Semi-arid",
        "rainfall_range": (400, 700),
        "soil_types": ["black soil", "red soil"]
    },
    "haveri": {
        "suitable_crops": [
            "rice", "jowar", "ragi", "maize", "cotton", "sugarcane",
            "groundnut", "soybean", "pigeonpeas", "chickpea", "mothbeans",
            "mungbean", "lentil", "onion", "tomato", "chilli", "brinjal"
        ],
        "unsuitable_crops": ["coffee", "tea", "cardamom", "pepper", "rubber"],
        "district_name": "Haveri",
        "region": "North Karnataka",
        "climate": "Semi-arid",
        "rainfall_range": (500, 900),
        "soil_types": ["black soil", "red soil", "alluvial soil"]
    },
    "gadag": {
        "suitable_crops": [
            "jowar", "bajra", "ragi", "maize", "cotton", "sunflower",
            "groundnut", "soybean", "pigeonpeas", "chickpea", "mothbeans",
            "mungbean", "lentil", "onion", "tomato", "chilli"
        ],
        "unsuitable_crops": ["coffee", "tea", "cardamom", "pepper", "rubber", "coconut", "rice"],
        "district_name": "Gadag",
        "region": "North Karnataka",
        "climate": "Semi-arid",
        "rainfall_range": (400, 600),
        "soil_types": ["black soil", "red soil"]
    },
    "raichur": {
        "suitable_crops": [
            "rice", "jowar", "bajra", "ragi", "maize", "cotton", "sunflower",
            "groundnut", "soybean", "pigeonpeas", "chickpea", "mothbeans",
            "mungbean", "lentil", "onion", "tomato", "chilli"
        ],
        "unsuitable_crops": ["coffee", "tea", "cardamom", "pepper", "rubber"],
        "district_name": "Raichur",
        "region": "North Karnataka",
        "climate": "Semi-arid",
        "rainfall_range": (400, 700),
        "soil_types": ["black soil", "red soil", "alluvial soil"]
    },
    "koppal": {
        "suitable_crops": [
            "jowar", "bajra", "ragi", "maize", "cotton", "sunflower",
            "groundnut", "soybean", "pigeonpeas", "chickpea", "mothbeans",
            "mungbean", "lentil", "onion", "tomato", "chilli"
        ],
        "unsuitable_crops": ["coffee", "tea", "cardamom", "pepper", "rubber", "coconut", "rice"],
        "district_name": "Koppal",
        "region": "North Karnataka",
        "climate": "Semi-arid",
        "rainfall_range": (400, 600),
        "soil_types": ["black soil", "red soil"]
    },
    "kalaburagi": {
        "suitable_crops": [
            "jowar", "bajra", "ragi", "maize", "cotton", "sunflower",
            "groundnut", "soybean", "pigeonpeas", "chickpea", "mothbeans",
            "mungbean", "lentil", "onion", "tomato", "chilli", "brinjal"
        ],
        "unsuitable_crops": ["coffee", "tea", "cardamom", "pepper", "rubber", "coconut"],
        "district_name": "Kalaburagi (Gulbarga)",
        "region": "North Karnataka",
        "climate": "Semi-arid",
        "rainfall_range": (400, 700),
        "soil_types": ["black soil", "red soil"]
    },
    "bidar": {
        "suitable_crops": [
            "rice", "jowar", "bajra", "ragi", "maize", "cotton", "sunflower",
            "groundnut", "soybean", "pigeonpeas", "chickpea", "mothbeans",
            "mungbean", "lentil", "onion", "tomato", "chilli"
        ],
        "unsuitable_crops": ["coffee", "tea", "cardamom", "pepper", "rubber"],
        "district_name": "Bidar",
        "region": "North Karnataka",
        "climate": "Semi-arid",
        "rainfall_range": (600, 900),
        "soil_types": ["black soil", "red soil", "alluvial soil"]
    },
    "ballari": {
        "suitable_crops": [
            "jowar", "bajra", "ragi", "maize", "cotton", "sunflower",
            "groundnut", "soybean", "pigeonpeas", "chickpea", "mothbeans",
            "mungbean", "lentil", "onion", "tomato", "chilli"
        ],
        "unsuitable_crops": ["coffee", "tea", "cardamom", "pepper", "rubber", "coconut", "rice"],
        "district_name": "Ballari (Bellary)",
        "region": "North Karnataka",
        "climate": "Semi-arid",
        "rainfall_range": (400, 600),
        "soil_types": ["black soil", "red soil"]
    },
}

# Default constraints for North Karnataka (if district not found)
DEFAULT_NORTH_KARNATAKA = {
    "suitable_crops": [
        "rice", "jowar", "bajra", "ragi", "maize", "cotton", "sugarcane",
        "sunflower", "groundnut", "soybean", "pigeonpeas", "chickpea",
        "mothbeans", "mungbean", "lentil", "onion", "tomato", "chilli",
        "brinjal", "okra", "cucumber", "watermelon", "muskmelon"
    ],
    "unsuitable_crops": [
        "coffee", "tea", "cardamom", "pepper", "rubber", "coconut", "arecanut",
        "cashew", "mango", "banana", "orange", "apple"
    ],
    "region": "North Karnataka",
    "climate": "Semi-arid",
    "rainfall_range": (400, 900),
    "soil_types": ["black soil", "red soil", "alluvial soil", "laterite soil"]
}


# ----------------------- UTILITIES -----------------------

def normalize(text: str) -> str:
    """Lowercases + trims + keeps only alphabets & spaces for safe matching."""
    if not isinstance(text, str):
        return ""
    text = text.strip().lower()
    # keep letters and spaces only (remove punctuation, numbers)
    return re.sub(r"[^a-z\s]", "", text)


# ----------------------- DISTRICT DETECTION -----------------------

def detect_district_from_location(location: str) -> str:
    """
    Detect district from location string (case-insensitive)
    Returns district key or 'default' if not found.

    Matching strategy:
    - Normalize input (lowercase + alpha-only)
    - Exact normalized token check via district_map keys
    - Keys are checked in descending length order to reduce false short matches
    """
    if not location:
        return "default"

    location_clean = normalize(location)

    # Expanded mapping: tokens/aliases -> district key
    district_map = {
        # VIJAYAPURA (Bijapur)
        "vijayapura": "vijayapura",
        "bijapur": "vijayapura",
        "basavana bagewadi": "vijayapura",
        "basavana": "vijayapura",
        "sindgi": "vijayapura",
        "indi": "vijayapura",
        "muddebihal": "vijayapura",
        "babaleshwar": "vijayapura",
        "tikota": "vijayapura",
        "talikoti": "vijayapura",
        "kolhar": "vijayapura",
        "almel": "vijayapura",
        "hulsoor": "vijayapura",
        "nidoni": "vijayapura",
        "jambagi": "vijayapura",
        # Extended Vijayapura villages
        "kakhandaki": "vijayapura", "kambagi": "vijayapura",
        "kanabur": "vijayapura", "karjol": "vijayapura",
        "katral": "vijayapura", "kodabagi": "vijayapura",
        "lingadalli": "vijayapura", "mamadapur": "vijayapura",
        "mangalur": "vijayapura", "nagaral": "vijayapura",
        "nandyal": "vijayapura", "sangapur": "vijayapura",
        "sarawad": "vijayapura", "savanalli": "vijayapura",
        "shirabur": "vijayapura", "tajapur": "vijayapura",
        "tonsyal": "vijayapura", "yakkundi": "vijayapura",
        "adavisangapur": "vijayapura", "arjunagi": "vijayapura",
        "babalad": "vijayapura", "bellubbi": "vijayapura",
        "bolachikkalaki": "vijayapura", "chikkagalagali": "vijayapura",
        "dadamatti": "vijayapura", "dasyal": "vijayapura",
        "devapur": "vijayapura", "devara gennur": "vijayapura",
        "dhanyal": "vijayapura", "dudihal": "vijayapura",
        "gunadal": "vijayapura", "halagani": "vijayapura",
        "hangaragi": "vijayapura", "hanumasagar": "vijayapura",
        "hebbalahatti": "vijayapura", "hokkundi": "vijayapura",
        "honaganahalli": "vijayapura", "hosur": "vijayapura",
        "jainapur": "vijayapura", "kakanagiri": "vijayapura",
        "kengalagutti": "vijayapura", "kumathe": "vijayapura",
        "madagunaki": "vijayapura", "sutagundi": "vijayapura",
        "tiganibidare": "vijayapura", "uppaladinni": "vijayapura",
        "agasabal": "vijayapura", "ambalanur": "vijayapura",
        "bisanal": "vijayapura", "bommanahalli": "vijayapura",

        # BELAGAVI (Belgaum)
        "belagavi": "belagavi", "belgaum": "belagavi",
        "gokak": "belagavi", "khanapur": "belagavi",
        "saundatti": "belagavi", "athani": "belagavi",
        "chikkodi": "belagavi",

        # BAGALKOT
        "bagalkot": "bagalkot",
        "badami": "bagalkot", "pattadakal": "bagalkot",
        "aihole": "bagalkot", "mudhol": "bagalkot",
        "jamkhandi": "bagalkot",

        # HAVERI
        "haveri": "haveri",
        "hirekerur": "haveri", "savanur": "haveri",
        "hangal": "haveri", "byadgi": "haveri",
        "shiggaon": "haveri",

        # GADAG
        "gadag": "gadag",
        "nargund": "gadag", "mundargi": "gadag",
        "ron": "gadag",

        # RAICHUR
        "raichur": "raichur",
        "lingsugur": "raichur", "sindhnur": "raichur",
        "manvi": "raichur",

        # KOPPAL
        "koppal": "koppal",
        "yelburga": "koppal", "gangavathi": "koppal",
        "kushtagi": "koppal",

        # Other: include district-level keys for future matches
        "kalaburagi": "kalaburagi", "gulbarga": "kalaburagi",
        "bidar": "bidar",
        "ballari": "ballari", "bellary": "ballari",
    }

    # Check keys in descending length to reduce accidental short matches
    for key in sorted(district_map.keys(), key=lambda x: -len(x)):
        if key in location_clean:
            return district_map[key]

    return "default"


def get_regional_constraints(location: str):
    """Return region-specific constraints (district-level) for a location string."""
    district = detect_district_from_location(location)
    return REGIONAL_CROPS.get(district, DEFAULT_NORTH_KARNATAKA)


# ----------------------- CROP FILTERING -----------------------

def crop_match(crop: str, crop_list: list) -> bool:
    """
    Improved matching:
    1. Exact normalized match first
    2. Conservative substring checks (crop within list item or vice versa)
    This reduces false positives from simple substring overlaps.
    """
    c = normalize(crop)
    normalized_list = [normalize(x) for x in crop_list]

    if not c:
        return False

    # Exact match
    if c in normalized_list:
        return True

    # Conservative substring match:
    # Allow if the crop token is contained in a list token (e.g., 'mung' inside 'mungbean')
    # or if a list token is contained in the crop (for user-entered longer names)
    for item in normalized_list:
        if c == item:
            return True
        if len(c) > 3 and (c in item or item in c):
            return True

    return False


def filter_crops_by_region(predicted_crops: list, location: str) -> list:
    """
    Filter predicted crops using regional constraints.
    Returns list of dicts: {"crop": ..., "suitable": bool, "region_verified": True}
    If all predicted crops are removed (e.g., all unsuitable), returns top 5 suitable crops as fallback.
    """
    constraints = get_regional_constraints(location)
    suitable = constraints.get("suitable_crops", [])
    unsuitable = constraints.get("unsuitable_crops", [])

    filtered = []
    seen = set()

    for crop in predicted_crops:
        # Normalize original crop string for matching, preserve original in output
        if isinstance(crop, str):
            original = crop
        else:
            original = str(crop)

        c_norm = normalize(original)

        # Remove explicitly unsuitable crops
        if crop_match(c_norm, unsuitable):
            continue

        is_suitable = crop_match(c_norm, suitable)

        # deduplicate by normalized token
        if c_norm in seen:
            continue
        seen.add(c_norm)

        filtered.append({
            "crop": original,
            "suitable": is_suitable,
            "region_verified": True
        })

    # fallback when nothing is left
    if not filtered:
        return [{"crop": crop, "suitable": True, "region_verified": True}
                for crop in suitable[:5]]

    return filtered


# ----------------------- REGION ANALYSIS -----------------------

def get_region_analysis(location: str, predicted_crop: str, soil_data: dict) -> dict:
    """
    Provide a detailed region analysis given:
    - location (string; detected to district)
    - predicted_crop (string)
    - soil_data (dict; expected keys: 'rainfall' (mm), 'soil_type' (string))
    """
    constraints = get_regional_constraints(location)

    crop_norm = normalize(predicted_crop)
    suitable = constraints.get("suitable_crops", [])
    unsuitable = constraints.get("unsuitable_crops", [])

    is_suitable = crop_match(crop_norm, suitable)
    is_unsuitable = crop_match(crop_norm, unsuitable)

    # Rainfall check (safe handling if rainfall missing or NaN)
    try:
        rainfall = float(soil_data.get("rainfall", 0) or 0)
    except (ValueError, TypeError):
        rainfall = 0.0

    r_min, r_max = constraints.get("rainfall_range", (400, 900))
    rainfall_ok = (r_min <= rainfall <= r_max)

    # Soil type check - normalize both sides and check membership
    soil_type = normalize(soil_data.get("soil_type", ""))
    soil_ok = False
    for st in constraints.get("soil_types", []):
        if normalize(st) in soil_type:
            soil_ok = True
            break

    return {
        "region": constraints.get("district_name", "North Karnataka"),
        "predicted_crop": predicted_crop,
        "is_regionally_suitable": is_suitable and not is_unsuitable,
        "is_unsuitable": is_unsuitable,
        "suitable_crops": constraints.get("suitable_crops", []),
        "climate": constraints.get("climate"),
        "rainfall_range": constraints.get("rainfall_range"),
        "current_rainfall": rainfall,
        "rainfall_adequate": rainfall_ok,
        "soil_type": soil_type,
        "soil_suitable": soil_ok,
        "recommendations": generate_recommendations(
            is_suitable, is_unsuitable, rainfall_ok, soil_ok, constraints
        )
    }


# ----------------------- RECOMMENDATIONS -----------------------

def generate_recommendations(is_suitable, is_unsuitable, rain_ok, soil_ok, constraints):
    """
    Build human-friendly recommendation objects (type, message, optional alternatives)
    """
    rec = []

    if is_unsuitable:
        rec.append({
            "type": "warning",
            "message": f"⚠️ {constraints.get('district_name','This region')} is not suitable for this crop.",
            "alternatives": constraints.get("suitable_crops", [])[:5]
        })

    if not rain_ok:
        rec.append({
            "type": "info",
            "message": "💧 Rainfall is outside the optimal range for this crop. Consider irrigation, water-conserving practices, or an alternative crop."
        })

    if not soil_ok:
        rec.append({
            "type": "info",
            "message": "🌱 Soil type may require amendment for optimal growth (e.g., organic matter, pH adjustments)."
        })

    if is_suitable and rain_ok and soil_ok:
        rec.append({
            "type": "success",
            "message": "✅ This crop is well-suited for your region and current conditions."
        })

    return rec
