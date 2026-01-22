import math

# Database of compatible intercrops
# Format: Main Crop -> [List of compatible intercrops]
INTERCROP_RULES = {
    "Rice": ["Black gram", "Green gram", "Soybean"],
    "Maize": ["Beans", "Cowpea", "Groundnut", "Soybean", "Pumpkin"],
    "Wheat": ["Mustard", "Chickpea", "Lentil"],
    "Sorghum": ["Pigeonpeas", "Cowpea", "Soybean"],
    "Pearl Millet": ["Moth bean", "Cluster bean", "Green gram"],
    "Finger Millet": ["Pigeonpeas", "Field bean"],
    "Chickpea": ["Mustard", "Linseed", "Barley"],
    "Pigeonpeas": ["Sorghum", "Maize", "Pearl Millet", "Groundnut"],
    "Groundnut": ["Maize", "Sorghum", "Pearl Millet", "Sunflower"],
    "Cotton": ["Black gram", "Green gram", "Cowpea", "Soybean"],
    "Sugarcane": ["Potato", "Onion", "Coriander", "Mustard"],
    "Potato": ["Wheat", "Maize", "Sugarcane"],
    "Onion": ["Sugarcane", "Chilli"],
    "Tomato": ["Marigold", "Onion"],
    "Brinjal": ["Chilli", "Beans"],
    "Chilli": ["Onion", "Garlic"],
    "Cabbage": ["Tomato", "Spinach"],
    "Cauliflower": ["Spinach", "Peas"],
    "Peas": ["Cauliflower", "Cabbage", "Carrot"],
    "Beans": ["Maize", "Radish"],
    "Soybean": ["Maize", "Sorghum", "Cotton"],
    "Sunflower": ["Groundnut", "Pigeonpeas"],
    "Mustard": ["Wheat", "Chickpea"],
    "Jute": ["Rice", "Vegetables"],
    "Barley": ["Chickpea", "Lentil"],
    "Lentil": ["Wheat", "Barley"],
    "Black gram": ["Sorghum", "Maize", "Cotton"],
    "Green gram": ["Sorghum", "Maize", "Cotton"],
    "Cowpea": ["Maize", "Sorghum"],
    "Moth bean": ["Pearl Millet"],
    "Horse gram": ["Niger"],
    "Coconut": ["Banana", "Turmeric", "Ginger", "Pineapple"],
    "Arecanut": ["Banana", "Pepper", "Cardamom", "Cocoa"],
    "Coffee": ["Pepper", "Cardamom", "Orange"],
    "Tea": ["Silver Oak"],
    "Rubber": ["Pineapple", "Banana"],
    "Cashewnut": ["Pineapple"],
    "Mango": ["Turmeric", "Ginger", "Vegetables"],
    "Banana": ["Coconut", "Arecanut"],
    "Grapes": ["Vegetables"],
    "Pomegranate": ["Vegetables"],
    "Papaya": ["Vegetables"],
    "Orange": ["Coffee"],
    "Apple": ["Vegetables"],
    "Turmeric": ["Coconut", "Arecanut", "Mango"],
    "Ginger": ["Coconut", "Arecanut", "Mango"]
}

def get_compatible_crops(main_crop):
    """Get list of compatible crops for a given main crop"""
    return INTERCROP_RULES.get(main_crop, ["Beans", "Vegetables"]) # Default fallback

def calculate_farm_dimensions(land_size_acres):
    """
    Calculate approximate square dimensions in meters for a given acreage.
    1 acre = 4046.86 square meters
    """
    sq_meters = land_size_acres * 4046.86
    side_length = math.sqrt(sq_meters)
    return round(side_length, 2), round(side_length, 2)

def generate_mixed_layout(main_crop, land_size_acres=1.0):
    """
    Generate a mixed cropping layout for the given crop and land size.
    Returns a dictionary with layout details and sections.
    """
    width, height = calculate_farm_dimensions(land_size_acres)
    
    # Get compatible intercrops
    intercrops = get_compatible_crops(main_crop)
    # Select the best one (for simplicity, take the first one)
    secondary_crop = intercrops[0] if intercrops else "Beans"
    
    # Define layout pattern (Strip Cropping is common)
    # 70% Main Crop, 30% Intercrop
    main_ratio = 0.7
    secondary_ratio = 0.3
    
    # Create sections
    sections = []
    
    # Pattern: Strip Cropping (Vertical Strips)
    # We'll create 5 strips: Main, Secondary, Main, Secondary, Main
    
    num_strips = 5
    strip_width = width / num_strips
    
    current_x = 0
    
    # Alternating strips
    for i in range(num_strips):
        is_main = i % 2 == 0 # Even indices are main crop (0, 2, 4) -> 3 strips
        
        crop_name = main_crop if is_main else secondary_crop
        
        sections.append({
            "x": round(current_x, 2),
            "y": 0,
            "w": round(strip_width, 2),
            "h": round(height, 2),
            "crop": crop_name,
            "type": "Main" if is_main else "Intercrop"
        })
        
        current_x += strip_width

    # Calculate actual area percentages based on strips
    # 3 strips of Main, 2 strips of Secondary
    # Total 5 strips. Main = 3/5 = 60%, Secondary = 2/5 = 40%
    # Let's adjust to be closer to 70/30 if possible, but 60/40 is fine for strip cropping
    
    mixed_crops = [
        {"crop": main_crop, "area_percent": 60, "role": "Main Crop"},
        {"crop": secondary_crop, "area_percent": 40, "role": "Intercrop"}
    ]

    return {
        "main_crop": main_crop,
        "land_size_acres": land_size_acres,
        "layout": {
            "width": width,
            "height": height,
            "pattern": "Strip Intercropping",
            "sections": sections
        },
        "mixed_crops": mixed_crops
    }
