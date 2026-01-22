import sys
import os
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.utils.pdf_generator import generate_pdf

# Mock data
data = {
    "farmer_name": "Ramesh Kumar",
    "phone": "9876543210",
    "location": "Haveri, Karnataka",
    "land_size": 19.8,
    "N": 80,
    "P": 50,
    "K": 50,
    "ph": 6.5,
    "temperature": 28,
    "humidity": 65,
    "rainfall": 600,
    "soil_type": "Black Soil",
    "predicted_crop": "Cotton",
    "confidence": 92.5,
    "model_used": "Stacking Classifier",
    "soil_health": {
        "overall_score": 85.0,
        "category": "Good",
        "breakdown": {
            "nutrient_balance": 80,
            "physical_properties": 90,
            "biological_activity": 85
        }
    },
    "soil_treatment": [
        "Soil pH (6.5) is within optimal range (5.8-8.0) for cotton.",
        "Nitrogen (80.0 mg/kg) is within optimal range for cotton.",
        "High clay content, retains moisture well. Ideal for cotton, wheat, and pulses."
    ],
    "fertilizer_estimate": "FARM DETAILS\nFERTILIZER APPLICATION SCHEDULE\nNITROGEN (N): 396.0 kg total (20.0 kg/acre)\nApplication Method:\n• Basal (50%): 198.0 kg at sowing\n• First Top Dressing (25%): 99.0 kg at tillering stage\nORGANIC & BIO-FERTILIZER ALTERNATIVES\nFarm Yard Manure (FYM): 99-198 tons\nNote: Apply fertilizers based on soil test results.",
    "market_recommendation": {
        "current_price_range": {"min": 2000, "max": 3500, "average": 2750},
        "best_market": {"name": "Local Market", "state": "Your State", "price": 2750, "unit": "₹/Quintal"},
        "recommendation": "Market data integration is available in the system. In a production environment, this would show real-time market prices."
    }
}

try:
    output_file = generate_pdf(data, filename="test_bilingual_report.pdf", include_images=True)
    print(f"Success! Report generated at: {output_file}")
except Exception as e:
    print(f"Error generating PDF: {e}")
    import traceback
    traceback.print_exc()
