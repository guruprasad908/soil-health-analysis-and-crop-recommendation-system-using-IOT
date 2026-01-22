import sys
import os
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.regional_crops import REGIONAL_CROPS, DEFAULT_NORTH_KARNATAKA, normalize

def extract_data():
    print("Identifying suitable crops for North Karnataka...")
    
    suitable_crops = set()
    
    # Add crops from all defined districts
    for district_data in REGIONAL_CROPS.values():
        for crop in district_data.get('suitable_crops', []):
            suitable_crops.add(normalize(crop))
            
    # Add crops from default rules
    for crop in DEFAULT_NORTH_KARNATAKA.get('suitable_crops', []):
        suitable_crops.add(normalize(crop))
        
    print(f"Found {len(suitable_crops)} unique suitable crops.")
    print(f"Crops: {', '.join(sorted(suitable_crops))}")
    
    print("\nLoading dataset...")
    try:
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/crop_recommendation_with_soil.csv'))
    except FileNotFoundError:
        print("Error: Dataset not found.")
        return

    print(f"Original dataset size: {len(df)} rows")
    
    # Filter
    # We normalize the dataframe label for comparison
    mask = df['label'].apply(normalize).isin(suitable_crops)
    filtered_df = df[mask]
    
    print(f"Filtered dataset size: {len(filtered_df)} rows")
    
    output_path = os.path.join(os.path.dirname(__file__), '../north_karnataka_suitable_crops.csv')
    filtered_df.to_csv(output_path, index=False)
    
    print("-" * 60)
    print(f"Data extracted to: {output_path}")
    print("-" * 60)
    print("Sample of extracted data:")
    print(filtered_df.head().to_string())

if __name__ == "__main__":
    extract_data()
