import sys
import os
import pandas as pd
import numpy as np

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.regional_crops import get_region_analysis, detect_district_from_location

def generate_demo_report():
    print("Loading dataset...")
    try:
        # Load the dataset
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/crop_recommendation_with_soil.csv'))
    except FileNotFoundError:
        print("Error: Dataset not found at ../data/crop_recommendation_with_soil.csv")
        return

    # Get unique crops and their typical characteristics (average rainfall, most common soil)
    print("Analyzing crop characteristics from data...")
    crop_stats = []
    
    for crop in df['label'].unique():
        crop_data = df[df['label'] == crop]
        avg_rainfall = crop_data['rainfall'].mean()
        
        # Get most common soil type
        soil_type = crop_data['soil_type'].mode().iloc[0] if not crop_data['soil_type'].empty else "unknown"
        
        crop_stats.append({
            'crop': crop,
            'rainfall': avg_rainfall,
            'soil_type': soil_type
        })

    # Define target districts in North Karnataka
    districts = [
        'vijayapura', 'belagavi', 'bagalkot', 'haveri', 'gadag', 
        'raichur', 'koppal', 'kalaburagi', 'bidar', 'ballari'
    ]

    results = []
    print(f"Testing {len(crop_stats)} crops against {len(districts)} districts...")

    for district in districts:
        # Detect district name properly (simulating user input)
        # We use the district key itself as input to be safe, or a formatted name
        location_input = district.capitalize()
        
        for stat in crop_stats:
            crop = stat['crop']
            
            # Prepare soil data for the analysis function
            soil_data = {
                'rainfall': stat['rainfall'],
                'soil_type': stat['soil_type']
            }
            
            # Run the analysis
            analysis = get_region_analysis(location_input, crop, soil_data)
            
            # Determine the final status and reason
            status = "Allowed"
            reason = "Suitable"
            
            if analysis['is_unsuitable']:
                status = "Blocked"
                reason = "Explicitly Unsuitable (Crop not grown in region)"
            elif not analysis['rainfall_adequate']:
                status = "Warning"
                reason = f"Rainfall Mismatch (Needs {analysis['rainfall_range']}mm, Avg {stat['rainfall']:.1f}mm)"
            elif not analysis['soil_suitable']:
                status = "Warning"
                reason = f"Soil Mismatch (Needs {analysis['soil_type']}, Got {stat['soil_type']})"
            
            # Add to results
            results.append({
                'District': analysis['region'], # Use the pretty name returned by analysis
                'Crop': crop,
                'Avg Rainfall (mm)': f"{stat['rainfall']:.1f}",
                'Typical Soil': stat['soil_type'],
                'Status': status,
                'Reason': reason
            })

    # Create DataFrame and save
    results_df = pd.DataFrame(results)
    output_file = os.path.join(os.path.dirname(__file__), '../regional_filtering_demo.csv')
    results_df.to_csv(output_file, index=False)
    
    print("-" * 60)
    print(f"Demo Report Generated: {output_file}")
    print("-" * 60)
    print(f"Total Scenarios Tested: {len(results)}")
    print("Sample Rows:")
    print(results_df.head(10).to_string())
    print("-" * 60)

if __name__ == "__main__":
    generate_demo_report()
