"""
Generate realistic North Karnataka crop dataset
Based on agricultural research and regional data
"""

import pandas as pd
import numpy as np
from datetime import datetime

# North Karnataka Districts
DISTRICTS = [
    'Vijayapura', 'Bagalkot', 'Kalaburagi', 'Bidar', 'Yadgir',
    'Raichur', 'Koppal', 'Gadag', 'Haveri', 'Ballari'
]

# Soil types in North Karnataka
SOIL_TYPES = ['black soil', 'red soil', 'alluvial soil', 'laterite soil']

# North Karnataka specific crops with their optimal growing conditions
NORTH_KARNATAKA_CROPS = {
    # CEREALS & MILLETS (Main crops of the region)
    'jowar': {
        'N': (40, 60), 'P': (25, 40), 'K': (30, 45),
        'temperature': (25, 32), 'humidity': (45, 65), 'ph': (6.5, 8.5),
        'rainfall': (450, 750), 'soil_types': ['black soil', 'red soil'],
        'priority': 'high', 'yield': (10, 15)  # quintals/acre
    },
    'bajra': {
        'N': (35, 55), 'P': (20, 35), 'K': (25, 40),
        'temperature': (26, 35), 'humidity': (40, 60), 'ph': (6.0, 8.0),
        'rainfall': (400, 650), 'soil_types': ['red soil', 'alluvial soil'],
        'priority': 'high', 'yield': (8, 12)
    },
    'ragi': {
        'N': (40, 65), 'P': (30, 45), 'K': (35, 50),
        'temperature': (20, 30), 'humidity': (50, 70), 'ph': (5.5, 7.5),
        'rainfall': (600, 1000), 'soil_types': ['red soil', 'laterite soil'],
        'priority': 'medium', 'yield': (12, 18)
    },
    'wheat': {
        'N': (60, 80), 'P': (35, 50), 'K': (40, 55),
        'temperature': (15, 25), 'humidity': (50, 70), 'ph': (6.0, 7.5),
        'rainfall': (450, 650), 'soil_types': ['black soil', 'alluvial soil'],
        'priority': 'medium', 'yield': (15, 22)
    },
    'maize': {
        'N': (70, 100), 'P': (40, 60), 'K': (45, 65),
        'temperature': (21, 30), 'humidity': (55, 75), 'ph': (5.5, 7.5),
        'rainfall': (600, 1000), 'soil_types': ['black soil', 'alluvial soil', 'red soil'],
        'priority': 'high', 'yield': (18, 28)
    },
    
    # PULSES
    'chickpea': {
        'N': (20, 35), 'P': (25, 40), 'K': (20, 35),
        'temperature': (20, 30), 'humidity': (40, 60), 'ph': (6.0, 8.0),
        'rainfall': (400, 650), 'soil_types': ['black soil', 'red soil'],
        'priority': 'high', 'yield': (8, 14)
    },
    'pigeonpeas': {
        'N': (25, 40), 'P': (30, 45), 'K': (25, 40),
        'temperature': (22, 35), 'humidity': (45, 70), 'ph': (6.5, 8.0),
        'rainfall': (600, 900), 'soil_types': ['black soil', 'red soil'],
        'priority': 'high', 'yield': (6, 12)
    },
    'greengram': {
        'N': (15, 30), 'P': (20, 35), 'K': (20, 30),
        'temperature': (25, 35), 'humidity': (50, 70), 'ph': (6.5, 7.5),
        'rainfall': (500, 800), 'soil_types': ['black soil', 'alluvial soil'],
        'priority': 'medium', 'yield': (5, 10)
    },
    'blackgram': {
        'N': (15, 30), 'P': (20, 35), 'K': (15, 30),
        'temperature': (25, 35), 'humidity': (50, 70), 'ph': (6.0, 7.5),
        'rainfall': (500, 800), 'soil_types': ['black soil', 'red soil'],
        'priority': 'medium', 'yield': (4, 9)
    },
    'lentil': {
        'N': (15, 25), 'P': (25, 35), 'K': (20, 30),
        'temperature': (18, 28), 'humidity': (45, 65), 'ph': (6.0, 7.5),
        'rainfall': (400, 600), 'soil_types': ['black soil', 'alluvial soil'],
        'priority': 'low', 'yield': (5, 10)
    },
    
    # CASH CROPS
    'cotton': {
        'N': (60, 90), 'P': (35, 55), 'K': (40, 60),
        'temperature': (24, 35), 'humidity': (50, 70), 'ph': (6.0, 8.0),
        'rainfall': (500, 1000), 'soil_types': ['black soil', 'red soil'],
        'priority': 'high', 'yield': (8, 15)  # quintals lint/acre
    },
    'sugarcane': {
        'N': (100, 140), 'P': (50, 70), 'K': (60, 90),
        'temperature': (25, 35), 'humidity': (60, 85), 'ph': (6.5, 7.5),
        'rainfall': (1200, 2000), 'soil_types': ['black soil', 'alluvial soil'],
        'priority': 'low', 'yield': (250, 400)  # quintals/acre (needs irrigation)
    },
    'sunflower': {
        'N': (50, 70), 'P': (30, 50), 'K': (35, 55),
        'temperature': (20, 30), 'humidity': (40, 60), 'ph': (6.5, 8.0),
        'rainfall': (500, 800), 'soil_types': ['black soil', 'red soil', 'alluvial soil'],
        'priority': 'high', 'yield': (6, 12)
    },
    'groundnut': {
        'N': (20, 40), 'P': (25, 45), 'K': (30, 50),
        'temperature': (25, 33), 'humidity': (50, 70), 'ph': (6.0, 7.5),
        'rainfall': (500, 900), 'soil_types': ['red soil', 'alluvial soil'],
        'priority': 'medium', 'yield': (8, 15)
    },
    'safflower': {
        'N': (40, 60), 'P': (25, 40), 'K': (30, 45),
        'temperature': (15, 25), 'humidity': (35, 55), 'ph': (6.5, 8.0),
        'rainfall': (400, 650), 'soil_types': ['black soil', 'red soil'],
        'priority': 'medium', 'yield': (5, 10)
    },
    
    # HORTICULTURE
    'onion': {
        'N': (80, 110), 'P': (40, 60), 'K': (50, 70),
        'temperature': (18, 28), 'humidity': (55, 75), 'ph': (6.0, 7.5),
        'rainfall': (600, 1000), 'soil_types': ['black soil', 'alluvial soil', 'red soil'],
        'priority': 'high', 'yield': (80, 150)  # quintals/acre
    },
    'tomato': {
        'N': (90, 120), 'P': (45, 65), 'K': (55, 75),
        'temperature': (20, 30), 'humidity': (60, 80), 'ph': (6.0, 7.0),
        'rainfall': (600, 1000), 'soil_types': ['red soil', 'alluvial soil'],
        'priority': 'medium', 'yield': (100, 200)
    },
    'chilli': {
        'N': (70, 100), 'P': (35, 55), 'K': (45, 65),
        'temperature': (22, 32), 'humidity': (55, 75), 'ph': (6.0, 7.5),
        'rainfall': (600, 1000), 'soil_types': ['red soil', 'black soil'],
        'priority': 'high', 'yield': (25, 45)
    },
    'pomegranate': {
        'N': (80, 110), 'P': (50, 70), 'K': (60, 90),
        'temperature': (25, 35), 'humidity': (40, 60), 'ph': (6.5, 7.5),
        'rainfall': (500, 800), 'soil_types': ['red soil', 'black soil'],
        'priority': 'medium', 'yield': (40, 80)
    },
    'grapes': {
        'N': (90, 120), 'P': (50, 70), 'K': (70, 100),
        'temperature': (20, 30), 'humidity': (50, 70), 'ph': (6.5, 7.5),
        'rainfall': (600, 900), 'soil_types': ['black soil', 'red soil'],
        'priority': 'low', 'yield': (60, 120)
    },
    
    # OILSEEDS
    'soybean': {
        'N': (30, 50), 'P': (30, 50), 'K': (25, 45),
        'temperature': (22, 30), 'humidity': (60, 80), 'ph': (6.0, 7.5),
        'rainfall': (600, 1000), 'soil_types': ['black soil', 'alluvial soil'],
        'priority': 'medium', 'yield': (8, 15)
    }
}

def generate_realistic_sample(crop_name, crop_params, suitable=True):
    """Generate a realistic crop sample with natural variation"""
    
    if suitable:
        # For suitable crops, generate within optimal range with some variation
        sample = {
            'N': np.random.uniform(crop_params['N'][0], crop_params['N'][1]),
            'P': np.random.uniform(crop_params['P'][0], crop_params['P'][1]),
            'K': np.random.uniform(crop_params['K'][0], crop_params['K'][1]),
            'temperature': np.random.uniform(crop_params['temperature'][0], crop_params['temperature'][1]),
            'humidity': np.random.uniform(crop_params['humidity'][0], crop_params['humidity'][1]),
            'ph': np.random.uniform(crop_params['ph'][0], crop_params['ph'][1]),
            'rainfall': np.random.uniform(crop_params['rainfall'][0], crop_params['rainfall'][1]),
            'label': crop_name,
            'soil_type': np.random.choice(crop_params['soil_types'])
        }
    else:
        # For unsuitable crops, generate outside optimal range
        sample = {
            'N': np.random.uniform(0, 140),
            'P': np.random.uniform(0, 80),
            'K': np.random.uniform(0, 100),
            'temperature': np.random.uniform(10, 45),
            'humidity': np.random.uniform(20, 95),
            'ph': np.random.uniform(4.5, 9.5),
            'rainfall': np.random.uniform(200, 2500),
            'label': crop_name,
            'soil_type': np.random.choice(SOIL_TYPES)
        }
    
    return sample

def generate_north_karnataka_dataset(samples_per_crop=700):
    """
    Generate comprehensive North Karnataka dataset
    
    Args:
        samples_per_crop: Number of samples to generate per crop (default: 700)
    
    Returns:
        DataFrame with generated samples
    """
    
    print("🌾 Generating North Karnataka Crop Dataset...")
    print(f"Total crops: {len(NORTH_KARNATAKA_CROPS)}")
    print(f"Samples per crop: {samples_per_crop}")
    print(f"Total samples: {len(NORTH_KARNATAKA_CROPS) * samples_per_crop}")
    
    all_samples = []
    
    for crop_name, crop_params in NORTH_KARNATAKA_CROPS.items():
        print(f"  Generating samples for {crop_name}...")
        
        # Generate 80% suitable samples and 20% unsuitable
        suitable_count = int(samples_per_crop * 0.8)
        unsuitable_count = samples_per_crop - suitable_count
        
        # Suitable samples
        for _ in range(suitable_count):
            sample = generate_realistic_sample(crop_name, crop_params, suitable=True)
            all_samples.append(sample)
        
        # Unsuitable samples (for model to learn what NOT to recommend)
        for _ in range(unsuitable_count):
            sample = generate_realistic_sample(crop_name, crop_params, suitable=False)
            all_samples.append(sample)
    
    # Create DataFrame
    df = pd.DataFrame(all_samples)
    
    # Round numerical values for realism
    df['N'] = df['N'].round(1)
    df['P'] = df['P'].round(1)
    df['K'] = df['K'].round(1)
    df['temperature'] = df['temperature'].round(2)
    df['humidity'] = df['humidity'].round(2)
    df['ph'] = df['ph'].round(2)
    df['rainfall'] = df['rainfall'].round(1)
    
    # Shuffle the dataset
    df = df.sample(frac=1).reset_index(drop=True)
    
    print("\n✅ Dataset generation complete!")
    print(f"Total samples: {len(df)}")
    print(f"\nCrop distribution:")
    print(df['label'].value_counts().sort_index())
    print(f"\nSoil type distribution:")
    print(df['soil_type'].value_counts())
    
    return df

if __name__ == "__main__":
    # Generate dataset
    df = generate_north_karnataka_dataset(samples_per_crop=700)
    
    # Save to CSV
    output_path = 'data/north_karnataka_crops.csv'
    df.to_csv(output_path, index=False)
    print(f"\n📁 Dataset saved to: {output_path}")
    
    # Display statistics
    print("\n📊 Dataset Statistics:")
    print(f"Shape: {df.shape}")
    print(f"\nNumeric columns summary:")
    print(df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].describe())
    
    # Create a backup of old dataset
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f'data/backup/crop_recommendation_with_soil_{timestamp}.csv'
    
    print(f"\n💾 Creating backup of old dataset: {backup_path}")
    try:
        shutil.copy('data/crop_recommendation_with_soil.csv', backup_path)
        print("✅ Backup created successfully!")
    except Exception as e:
        print(f"⚠️ Could not create backup: {e}")
    
    print("\n🎯 Next Steps:")
    print("1. Review the generated dataset: data/north_karnataka_crops.csv")
    print("2. Retrain models: python app/models/train_model.py")
    print("3. Test predictions with real farmer cases")
    print("4. Collect feedback and refine crop parameters")
