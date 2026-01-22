import sys
import os
import csv
import pandas as pd

# Add the project root to the python path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.regional_crops import filter_crops_by_region, detect_district_from_location

def run_tests():
    # Define test cases
    # Format: (Location String, List of Crops to Test)
    test_cases = [
        ("Vijayapura", ["Coffee", "Jowar", "Bajra", "Rice", "Apple"]),
        ("Bijapur", ["Maize", "Tea", "Pomegranate"]),
        ("Tonsyal, Vijayapura", ["Sunflower", "Rubber"]),
        ("Belagavi", ["Rice", "Coffee", "Sugarcane"]),
        ("Gokak", ["Maize", "Coconut"]),
        ("Bagalkot", ["Jowar", "Tea"]),
        ("Badami", ["Cotton", "Cardamom"]),
        ("Haveri", ["Rice", "Rubber"]),
        ("Hirekerur", ["Chilli", "Coffee"]),
        ("Gadag", ["Jowar", "Rice"]), # Rice is unsuitable in Gadag
        ("Raichur", ["Rice", "Coffee"]),
        ("Koppal", ["Maize", "Apple"]),
        ("Unknown Location", ["Rice", "Coffee"]), # Should use default North Karnataka rules
        ("Bangalore", ["Rice", "Coffee"]) # Should use default North Karnataka rules (as it defaults to that if not found)
    ]

    results = []

    print("Running Regional Rule Tests...")
    print("-" * 60)

    for location, crops in test_cases:
        # Detect district for reporting
        detected_district = detect_district_from_location(location)
        
        # Run the filter logic
        filtered_results = filter_crops_by_region(crops, location)
        
        # Process results
        # filter_crops_by_region returns a list of dicts. 
        # If a crop is unsuitable, it might be filtered out or marked as unsuitable depending on implementation.
        # The current implementation returns: {"crop": ..., "suitable": bool, "region_verified": True}
        # But wait, the implementation says: "Remove explicitly unsuitable crops"
        # So if it's in 'unsuitable_crops', it's removed from the returned list?
        # Let's check the code again.
        # Code says: 
        # if crop_match(c_norm, unsuitable): continue
        # So explicitly unsuitable crops are REMOVED from the list.
        # However, if ALL are removed, it returns top 5 suitable crops.
        
        # To properly test "Is Suitable", we should check if the input crop is present in the output
        # and if it is marked as suitable.
        
        # Let's map the output for easy lookup
        output_map = {res['crop']: res for res in filtered_results}
        
        for crop in crops:
            is_present = False
            is_suitable = False
            note = ""
            
            # Check if this specific crop is in the output
            # We need to handle potential case differences or if the output uses the original name
            # The code preserves the original name.
            
            if crop in output_map:
                is_present = True
                is_suitable = output_map[crop]['suitable']
                note = "Passed filter"
            else:
                is_present = False
                is_suitable = False
                note = "Filtered out (Unsuitable)"
                
            # Special case: if the input list was completely replaced by fallback crops
            # We can detect this if none of the input crops are in the output
            # But here we are iterating per crop.
            
            results.append({
                "Input Location": location,
                "Detected District": detected_district,
                "Input Crop": crop,
                "Is Suitable": "Yes" if is_suitable else "No",
                "Outcome": note
            })

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(results)
    output_file = "regional_rules_test_results.csv"
    df.to_csv(output_file, index=False)
    
    print(f"\nTest completed. Results saved to {output_file}")
    print("-" * 60)
    print(df.to_string())

if __name__ == "__main__":
    run_tests()
