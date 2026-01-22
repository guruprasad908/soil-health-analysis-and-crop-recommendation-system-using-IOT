from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tempfile
import os
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Kannada Font
# Tunga is often better for PDF embedding than Nirmala UI
try:
    pdfmetrics.registerFont(TTFont('Kannada', 'C:\\Windows\\Fonts\\Tunga.ttf'))
    KANNADA_FONT = 'Kannada'
except:
    try:
        pdfmetrics.registerFont(TTFont('Kannada', 'C:\\Windows\\Fonts\\Nirmala.ttf'))
        KANNADA_FONT = 'Kannada'
    except:
        print("⚠ Warning: Kannada fonts (Tunga/Nirmala) not found. Kannada text may not render correctly.")
        KANNADA_FONT = 'Helvetica' # Fallback to standard font

# English to Kannada Translations
TRANSLATIONS = {
    "Soil Health & Crop Recommendation Report": "ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಮತ್ತು ಬೆಳೆ ಶಿಫಾರಸು ವರದಿ",
    "Report Date": "ವರದಿ ದಿನಾಂಕ",
    "Farmer Information": "ರೈತರ ಮಾಹಿತಿ",
    "Name": "ಹೆಸರು",
    "Phone": "ದೂರವಾಣಿ",
    "Location": "ಸ್ಥಳ",
    "Land Size": "ಜಮೀನು ವಿಸ್ತೀರ್ಣ",
    "acres": "ಎಕರೆ",
    "Soil Health Assessment": "ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಮೌಲ್ಯಮಾಪನ",
    "Overall Soil Health Score": "ಒಟ್ಟಾರೆ ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಅಂಕ",
    "Component": "ಘಟಕ",
    "Score": "ಅಂಕ",
    "Points": "ಅಂಕಗಳು",
    "Weather Suitability for": "ಹವಾಮಾನ ಸೂಕ್ತತೆ",
    "Overall Suitability Score": "ಒಟ್ಟಾರೆ ಸೂಕ್ತತೆ ಅಂಕ",
    "Recommended Crop": "ಶಿಫಾರಸು ಮಾಡಲಾದ ಬೆಳೆ",
    "Predicted Crop": "ಶಿಫಾರಸು ಬೆಳೆ",
    "Confidence Level": "ನಂಬಿಕೆ ಮಟ್ಟ",
    "Rainfall Analysis": "ಮಳೆ ವಿಶ್ಲೇಷಣೆ",
    "Status": "ಸ್ಥಿತಿ",
    "Sufficient": "ಸಾಕಷ್ಟು",
    "Deficient": "ಕೊರತೆ",
    "Excessive": "ಅತಿಯಾದ",
    "Soil Treatment Recommendations": "ಮಣ್ಣಿನ ಚಿಕಿತ್ಸೆ ಶಿಫಾರಸುಗಳು",
    "Fertilizer Recommendations": "ಗೊಬ್ಬರ ಶಿಫಾರಸುಗಳು",
    "Market Price Trends": "ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ಪ್ರವೃತ್ತಿಗಳು",
    "Mandi": "ಮಂಡಿ",
    "Price": "ಬೆಲೆ",
    "Warnings & Observations": "ಎಚ್ಚರಿಕೆಗಳು ಮತ್ತು ಅವಲೋಕನಗಳು",
    "Nitrogen": "ಸಾರಜನಕ",
    "Phosphorus": "ರಂಜಕ",
    "Potassium": "ಪೊಟ್ಯಾಸಿಯಮ್",
    "Temperature": "ತಾಪಮಾನ",
    "Humidity": "ತೇವಾಂಶ",
    "Rainfall": "ಮಳೆ",
    "Soil Type": "ಮಣ್ಣಿನ ಪ್ರಕಾರ",
    "Soil type": "ಮಣ್ಣಿನ ಪ್ರಕಾರ", # Lowercase handling
    "Parameter": "ಪರತಂತ್ರ",
    "Value": "ಮೌಲ್ಯ",
    "Unit": "ಘಟಕ",
    "Excellent": "ಅತ್ಯುತ್ತಮ",
    "Good": "ಉತ್ತಮ",
    "Moderate": "ಮಧ್ಯಮ",
    "Poor": "ಕಳಪೆ",
    "Generated": "ರಚಿಸಲಾಗಿದೆ",
    "Page": "ಪುಟ",
    "Range": "ವ್ಯಾಪ್ತಿ",
    "Average": "ಸರಾಸರಿ",
    "Best Market": "ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ",
    "Market Advice": "ಮಾರುಕಟ್ಟೆ ಸಲಹೆ",
    "Action Required": "ಅಗತ್ಯ ಕ್ರಮ",
    "Positive Indicators": "ಸಕಾರಾತ್ಮಕ ಸೂಚಕಗಳು",
    "Crop-Specific Tips for": "ಬೆಳೆ ನಿರ್ದಿಷ್ಟ ಸಲಹೆಗಳು",
    "Additional Notes & Disclaimer": "ಹೆಚ್ಚುವರಿ ಟಿಪ್ಪಣಿಗಳು ಮತ್ತು ಹಕ್ಕು ನಿರಾಕರಣೆ",
    # Crops
    "Rice": "ಭತ್ತ",
    "Maize": "ಜೋಳ",
    "Chickpea": "ಕಡಲೆ",
    "Kidneybeans": "ಹುರುಳಿ",
    "Pigeonpeas": "ತೊಗರಿ",
    "Mothbeans": "ಮಡಿಕೆ ಕಾಳು",
    "Mungbean": "ಹೆಸರು ಕಾಳು",
    "Blackgram": "ಉದ್ದು",
    "Lentil": "ಮಸೂರ",
    "Pomegranate": "ದಾಳಿಂಬೆ",
    "Banana": "ಬಾಳೆ",
    "Mango": "ಮಾವಿನ ಹಣ್ಣು",
    "Grapes": "ದ್ರಾಕ್ಷಿ",
    "Watermelon": "ಕಲ್ಲಂಗಡಿ",
    "Muskmelon": "ಕರಬೂಜ",
    "Apple": "ಸೇಬು",
    "Orange": "ಕಿತ್ತಳೆ",
    "Papaya": "ಪಪ್ಪಾಯಿ",
    "Coconut": "ತೆಂಗಿನಕಾಯಿ",
    "Cotton": "ಹತ್ತಿ",
    "Jute": "ಸೆಣಬು",
    "Coffee": "ಕಾಫಿ",
    # Dynamic content translations
    "Rainfall below optimal": "ಮಳೆ ಕೊರತೆ",
    "Increase irrigation": "ನೀರಾವರಿ ಹೆಚ್ಚಿಸಿ",
    "Rainfall excessive": "ಅತಿಯಾದ ಮಳೆ",
    "Ensure proper drainage": "ಸರಿಯಾದ ಒಳಚರಂಡಿ ವ್ಯವಸ್ಥೆ ಮಾಡಿ",
    "Temperature high": "ಹೆಚ್ಚಿನ ತಾಪಮಾನ",
    "Provide shade or mulching": "ನೆರಳು ಅಥವಾ ಮಲ್ಚಿಂಗ್ ಒದಗಿಸಿ",
    "Temperature low": "ಕಡಿಮೆ ತಾಪಮಾನ",
    "Consider protective covering": "ರಕ್ಷಣಾತ್ಮಕ ಹೊದಿಕೆಯನ್ನು ಪರಿಗಣಿಸಿ",
    "Soil acidic": "ಆಮ್ಲೀಯ ಮಣ್ಣು",
    "Add lime to raise pH": "pH ಹೆಚ್ಚಿಸಲು ಸುಣ್ಣ ಸೇರಿಸಿ",
    "Soil alkaline": "ಕ್ಷಾರೀಯ ಮಣ್ಣು",
    "Add gypsum to lower pH": "pH ಕಡಿಮೆ ಮಾಡಲು ಜಿಪ್ಸಮ್ ಸೇರಿಸಿ",
    "pH optimal": "pH ಉತ್ತಮವಾಗಿದೆ",
    "Nitrogen level optimal": "ಸಾರಜನಕ ಮಟ್ಟ ಉತ್ತಮವಾಗಿದೆ",
    "Phosphorus level optimal": "ರಂಜಕ ಮಟ್ಟ ಉತ್ತಮವಾಗಿದೆ",
    "Potassium level optimal": "ಪೊಟ್ಯಾಸಿಯಮ್ ಮಟ್ಟ ಉತ್ತಮವಾಗಿದೆ",
    "level optimal": "ಮಟ್ಟ ಉತ್ತಮವಾಗಿದೆ",
    "is ideal for": "ಗೆ ಸೂಕ್ತವಾಗಿದೆ",
    "is below requirement": "ಅಗತ್ಯಕ್ಕಿಂತ ಕಡಿಮೆಯಾಗಿದೆ",
    "irrigation strongly recommended": "ನೀರಾವರಿ ಬಲವಾಗಿ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ",
    "Black Soil": "ಕಪ್ಪು ಮಣ್ಣು",
    "Red Soil": "ಕೆಂಪು ಮಣ್ಣು",
    "Clay Soil": "ಜೇಡಿ ಮಣ್ಣು",
    "Sandy Soil": "ಮರಳು ಮಣ್ಣು",
    "Loamy Soil": "ಲೋಮಿ ಮಣ್ಣು",
    "Alluvial Soil": "ಮೆಕ್ಕಲು ಮಣ್ಣು",
    # Fertilizer & Soil Analysis Terms
    "Soil pH": "ಮಣ್ಣಿನ pH",
    "is within optimal range": "ಸೂಕ್ತ ವ್ಯಾಪ್ತಿಯಲ್ಲಿದೆ",
    "High clay content": "ಹೆಚ್ಚಿನ ಜೇಡಿ ಮಣ್ಣಿನ ಅಂಶ",
    "retains moisture well": "ತೇವಾಂಶವನ್ನು ಚೆನ್ನಾಗಿ ಹಿಡಿದಿಟ್ಟುಕೊಳ್ಳುತ್ತದೆ",
    "Ideal for": "ಗೆ ಸೂಕ್ತವಾಗಿದೆ",
    "FARM DETAILS": "ಜಮೀನಿನ ವಿವರಗಳು",
    "Current Soil NPK": "ಪ್ರಸ್ತುತ ಮಣ್ಣಿನ NPK",
    "Optimal NPK for": "ಗೆ ಸೂಕ್ತವಾದ NPK",
    "FERTILIZER APPLICATION SCHEDULE": "ಗೊಬ್ಬರ ಹಾಕುವ ವೇಳಾಪಟ್ಟಿ",
    "NITROGEN (N)": "ಸಾರಜನಕ (N)",
    "Application Method": "ಅನ್ವಯಿಸುವ ವಿಧಾನ",
    "Basal": "ಮೂಲ",
    "Top Dressing": "ಮೇಲ್ಗೊಬ್ಬರ",
    "at sowing": "ಬಿತ್ತನೆ ಸಮಯದಲ್ಲಿ",
    "at tillering stage": "ಮರಿಗಳು ಒಡೆಯುವ ಹಂತದಲ್ಲಿ",
    "at flowering stage": "ಹೂ ಬಿಡುವ ಹಂತದಲ್ಲಿ",
    "ORGANIC & BIO-FERTILIZER ALTERNATIVES": "ಸಾವಯವ ಮತ್ತು ಜೈವಿಕ ಗೊಬ್ಬರ ಪರ್ಯಾಯಗಳು",
    "Farm Yard Manure (FYM)": "ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ",
    "Compost": "ಕಾಂಪೋಸ್ಟ್",
    "Green Manure": "ಹಸಿರೆಲೆ ಗೊಬ್ಬರ",
    "Bio-Fertilizers": "ಜೈವಿಕ ಗೊಬ್ಬರಗಳು",
    "Benefits": "ಪ್ರಯಜನಗಳು",
    "Natural nitrogen fixation": "ನೈಸರ್ಗಿಕ ಸಾರಜನಕ ಸ್ಥಿರೀಕರಣ",
    "Enhances P uptake": "ರಂಜಕ ಹೀರಿಕೊಳ್ಳುವಿಕೆಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ",
    "Apply fertilizers based on": "ಮಣ್ಣಿನ ಪರೀಕ್ಷಾ ಫಲಿತಾಂಶಗಳ ಆಧಾರದ ಮೇಲೆ ಗೊಬ್ಬರ ಹಾಕಿ",
    "Avoid waterlogging": "ನೀರು ನಿಲ್ಲುವುದನ್ನು ತಡೆಯಿರಿ",
    "monitor for pests": "ಕೀಟಗಳಿಗಾಗಿ ಗಮನವಿಡಿ",
    "Requires warm climate": "ಬೆಚ್ಚಗಿನ ಹವಾಮಾನ ಅಗತ್ಯ",
    "Market data integration is available": "ಮಾರುಕಟ್ಟೆ ಡೇಟಾ ಏಕೀಕರಣ ಲಭ್ಯವಿದೆ",
    "In a production environment": "ಉತ್ಪಾದನಾ ಪರಿಸರದಲ್ಲಿ",
    "this would show real-time market prices": "ಇದು ನೈಜ ಸಮಯದ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳನ್ನು ತೋರಿಸುತ್ತದೆ",
    "Local Market": "ಸ್ಥಳೀಯ ಮಾರುಕಟ್ಟೆ",
    "Your State": "ನಿಮ್ಮ ರಾಜ್ಯ"
}

def clean_text(text, lang):
    """Clean text based on language. Removes emojis to prevent rendering issues in both English (Helvetica) and Kannada."""
    # Remove common emojis and symbols that might break font
    # Also remove checkmarks if they cause issues
    cleaned = text.replace("📊", "").replace("🌱", "").replace("📦", "").replace("⚠️", "").replace("🌿", "").replace("📝", "").replace("🔹", "").replace("🔸", "").replace("✅", "").replace("✓", "").replace("⚠", "").replace("■", "").replace("🌤️", "").replace("🌾", "").strip()
    return cleaned

# Comprehensive crop-specific tips for all crops
CROP_TIPS = {
    "rice": "Ensure consistent water supply and transplant in puddled field. Maintain 5-7 cm water depth.",
    "wheat": "Sow seeds at 4-5 cm depth and avoid over-irrigation. Requires well-drained soil.",
    "maize": "Plant in well-drained soil and apply nitrogen in splits. Maintain proper spacing.",
    "cotton": "Avoid waterlogging; monitor for pests like bollworms. Requires warm climate.",
    "sugarcane": "Requires high water and rich organic matter in soil. Plant in rows with proper spacing.",
    "coconut": "Requires high humidity and well-drained soil. Plant in pits with organic matter.",
    "apple": "Requires cold winters for dormancy. Prune regularly and maintain soil pH 6.0-7.0.",
    "banana": "Requires high humidity and consistent moisture. Plant in pits with organic matter.",
    "blackgram": "Leguminous crop, fixes nitrogen. Requires well-drained soil and moderate rainfall.",
    "chickpea": "Drought-tolerant legume. Requires well-drained soil and cool climate during flowering.",
    "coffee": "Requires shade and well-drained acidic soil. Prune regularly for better yield.",
    "grapes": "Requires trellis support and well-drained soil. Prune during dormancy period.",
    "jute": "Requires high humidity and consistent moisture. Harvest before flowering for best fiber.",
    "kidneybeans": "Leguminous crop, fixes nitrogen. Requires moderate temperature and well-drained soil.",
    "lentil": "Drought-tolerant legume. Requires cool climate and well-drained soil.",
    "mango": "Requires deep, well-drained soil. Prune after harvest and maintain proper spacing.",
    "mothbeans": "Drought-tolerant legume. Requires well-drained soil and moderate temperature.",
    "mungbean": "Short-duration legume. Requires well-drained soil and moderate rainfall.",
    "muskmelon": "Requires warm climate and well-drained soil. Provide support for vines.",
    "orange": "Requires well-drained soil and moderate temperature. Prune regularly and control pests.",
    "papaya": "Requires well-drained soil and warm climate. Plant both male and female trees.",
    "pigeonpeas": "Drought-tolerant legume. Requires well-drained soil and warm climate.",
    "pomegranate": "Requires well-drained soil and warm climate. Prune for better fruit quality.",
    "watermelon": "Requires warm climate and well-drained soil. Provide adequate spacing for vines.",
    # North Karnataka crops
    "jowar": "Drought-resistant millet. Requires well-drained black soil and moderate rainfall.",
    "bajra": "Pearl millet, highly drought-tolerant. Plant in sandy loam soil with good drainage.",
    "ragi": "Finger millet, nutritious crop. Requires moderate rainfall and well-drained soil.",
    "greengram": "Short-duration legume. Requires well-drained soil and moderate temperature.",
    "sunflower": "Requires full sunlight and well-drained soil. Monitor for pests and diseases.",
    "groundnut": "Leguminous oilseed crop. Requires well-drained sandy loam soil.",
    "safflower": "Oilseed crop suitable for dry conditions. Requires well-drained soil.",
    "onion": "Requires well-drained soil and moderate irrigation. Plant in rows with proper spacing.",
    "tomato": "Requires well-drained soil and regular irrigation. Stake plants for support.",
    "chilli": "Requires well-drained soil and moderate irrigation. Monitor for pests and diseases.",
    "soybean": "Leguminous crop. Requires well-drained soil and moderate rainfall."
}

# Kannada Crop Tips
CROP_TIPS_KN = {
    "rice": "ನಿರಂತರ ನೀರು ಸರಬರಾಜು ಮತ್ತು ನಾಟಿ ಮಾಡಿದ ಗದ್ದೆಯಲ್ಲಿ ಬೆಳೆಯಿರಿ. 5-7 ಸೆಂ.ಮೀ ನೀರಿನ ಮಟ್ಟವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ.",
    "wheat": "4-5 ಸೆಂ.ಮೀ ಆಳದಲ್ಲಿ ಬೀಜಗಳನ್ನು ಬಿತ್ತಿ ಮತ್ತು ಅತಿಯಾದ ನೀರಾವರಿಯನ್ನು ತಪ್ಪಿಸಿ. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ.",
    "maize": "ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆಯಿರಿ ಮತ್ತು ಸಾರಜನಕವನ್ನು ಕಂತುಗಳಲ್ಲಿ ನೀಡಿ. ಸರಿಯಾದ ಅಂತರವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ.",
    "cotton": "ನೀರು ನಿಲ್ಲುವುದನ್ನು ತಡೆಯಿರಿ; ಬೊಳ್ಳು ಹುಳುಗಳಂತಹ ಕೀಟಗಳಿಗಾಗಿ ಗಮನವಿಡಿ. ಬೆಚ್ಚಗಿನ ಹವಾಮಾನ ಅಗತ್ಯ.",
    "sugarcane": "ಹೆಚ್ಚಿನ ನೀರು ಮತ್ತು ಮಣ್ಣಿನಲ್ಲಿ ಸಮೃದ್ಧ ಸಾವಯವ ಪದಾರ್ಥಗಳ ಅಗತ್ಯವಿದೆ. ಸಾಲುಗಳಲ್ಲಿ ಸರಿಯಾದ ಅಂತರದಲ್ಲಿ ಬೆಳೆಯಿರಿ.",
    "coconut": "ಹೆಚ್ಚಿನ ತೇವಾಂಶ ಮತ್ತು ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ. ಸಾವಯವ ಗೊಬ್ಬರದೊಂದಿಗೆ ಗುಂಡಿಗಳಲ್ಲಿ ಬೆಳೆಯಿರಿ.",
    "apple": "ಸುಪ್ತಾವಸ್ಥೆಗೆ ಶೀತ ಚಳಿಗಾಲದ ಅಗತ್ಯವಿದೆ. ನಿಯಮಿತವಾಗಿ ಕತ್ತರಿಸಿ ಮತ್ತು ಮಣ್ಣಿನ pH 6.0-7.0 ಕಾಪಾಡಿಕೊಳ್ಳಿ.",
    "banana": "ಹೆಚ್ಚಿನ ತೇವಾಂಶ ಮತ್ತು ಸ್ಥಿರ ತೇವಾಂಶ ಅಗತ್ಯ. ಸಾವಯವ ಗೊಬ್ಬರದೊಂದಿಗೆ ಗುಂಡಿಗಳಲ್ಲಿ ಬೆಳೆಯಿರಿ.",
    "blackgram": "ದ್ವಿದಳ ಧಾನ್ಯ ಬೆಳೆ, ಸಾರಜನಕವನ್ನು ಸ್ಥಿರೀಕರಿಸುತ್ತದೆ. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಮಧ್ಯಮ ಮಳೆ ಅಗತ್ಯ.",
    "chickpea": "ಬರ ಸಹಿಷ್ಣು ದ್ವಿದಳ ಧಾನ್ಯ. ಹೂ ಬಿಡುವ ಸಮಯದಲ್ಲಿ ತಂಪಾದ ಹವಾಮಾನ ಮತ್ತು ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ.",
    "coffee": "ನೆರಳು ಮತ್ತು ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಆಮ್ಲೀಯ ಮಣ್ಣು ಅಗತ್ಯ. ಉತ್ತಮ ಇಳುವರಿಗಾಗಿ ನಿಯಮಿತವಾಗಿ ಕತ್ತರಿಸಿ.",
    "grapes": "ಚಪ್ಪರದ ಬೆಂಬಲ ಮತ್ತು ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ. ಸುಪ್ತಾವಸ್ಥೆಯ ಅವಧಿಯಲ್ಲಿ ಕತ್ತರಿಸಿ.",
    "jute": "ಹೆಚ್ಚಿನ ತೇವಾಂಶ ಮತ್ತು ಸ್ಥಿರ ತೇವಾಂಶ ಅಗತ್ಯ. ಉತ್ತಮ ನಾರಿಗಾಗಿ ಹೂ ಬಿಡುವ ಮೊದಲು ಕೊಯ್ಲು ಮಾಡಿ.",
    "kidneybeans": "ದ್ವಿದಳ ಧಾನ್ಯ ಬೆಳೆ, ಸಾರಜನಕವನ್ನು ಸ್ಥಿರೀಕರಿಸುತ್ತದೆ. ಮಧ್ಯಮ ತಾಪಮಾನ ಮತ್ತು ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ.",
    "lentil": "ಬರ ಸಹಿಷ್ಣು ದ್ವಿದಳ ಧಾನ್ಯ. ತಂಪಾದ ಹವಾಮಾನ ಮತ್ತು ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ.",
    "mango": "ಆಳವಾದ, ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ. ಕೊಯ್ಲಿನ ನಂತರ ಕತ್ತರಿಸಿ ಮತ್ತು ಸರಿಯಾದ ಅಂತರವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ.",
    "mothbeans": "ಬರ ಸಹಿಷ್ಣು ದ್ವಿದಳ ಧಾನ್ಯ. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಮಧ್ಯಮ ತಾಪಮಾನ ಅಗತ್ಯ.",
    "mungbean": "ಅಲ್ಪಾವಧಿಯ ದ್ವಿದಳ ಧಾನ್ಯ. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಮಧ್ಯಮ ಮಳೆ ಅಗತ್ಯ.",
    "muskmelon": "ಬೆಚ್ಚಗಿನ ಹವಾಮಾನ ಮತ್ತು ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ. ಬಳ್ಳಿಗಳಿಗೆ ಬೆಂಬಲ ನೀಡಿ.",
    "orange": "ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಮಧ್ಯಮ ತಾಪಮಾನ ಅಗತ್ಯ. ನಿಯಮಿತವಾಗಿ ಕತ್ತರಿಸಿ ಮತ್ತು ಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸಿ.",
    "papaya": "ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಬೆಚ್ಚಗಿನ ಹವಾಮಾನ ಅಗತ್ಯ. ಗಂಡು ಮತ್ತು ಹೆಣ್ಣು ಮರಗಳನ್ನು ಬೆಳೆಯಿರಿ.",
    "pigeonpeas": "ಬರ ಸಹಿಷ್ಣು ದ್ವಿದಳ ಧಾನ್ಯ. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಬೆಚ್ಚಗಿನ ಹವಾಮಾನ ಅಗತ್ಯ.",
    "pomegranate": "ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಬೆಚ್ಚಗಿನ ಹವಾಮಾನ ಅಗತ್ಯ. ಉತ್ತಮ ಹಣ್ಣಿನ ಗುಣಮಟ್ಟಕ್ಕಾಗಿ ಕತ್ತರಿಸಿ.",
    "watermelon": "ಬೆಚ್ಚಗಿನ ಹವಾಮಾನ ಮತ್ತು ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ. ಬಳ್ಳಿಗಳಿಗೆ ಸಾಕಷ್ಟು ಅಂತರವನ್ನು ಒದಗಿಸಿ.",
    # North Karnataka crops
    "jowar": "ಬರ ನಿರೋಧಕ ಸಿರಿಧಾನ್ಯ. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಕಪ್ಪು ಮಣ್ಣು ಮತ್ತು ಮಧ್ಯಮ ಮಳೆ ಅಗತ್ಯ.",
    "bajra": "ಸಜ್ಜೆ, ಹೆಚ್ಚು ಬರ ಸಹಿಷ್ಣು. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮರಳು ಮಿಶ್ರಿತ ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆಯಿರಿ.",
    "ragi": "ರಾಗಿ, ಪೌಷ್ಟಿಕ ಬೆಳೆ. ಮಧ್ಯಮ ಮಳೆ ಮತ್ತು ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ.",
    "greengram": "ಅಲ್ಪಾವಧಿಯ ದ್ವಿದಳ ಧಾನ್ಯ. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಮಧ್ಯಮ ತಾಪಮಾನ ಅಗತ್ಯ.",
    "sunflower": "ಪೂರ್ಣ ಸೂರ್ಯನ ಬೆಳಕು ಮತ್ತು ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ. ಕೀಟಗಳು ಮತ್ತು ರೋಗಗಳಿಗಾಗಿ ಗಮನವಿಡಿ.",
    "groundnut": "ದ್ವಿದಳ ಧಾನ್ಯದ ಎಣ್ಣೆಕಾಳು ಬೆಳೆ. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮರಳು ಮಿಶ್ರಿತ ಮಣ್ಣು ಅಗತ್ಯ.",
    "safflower": "ಒಣ ಪರಿಸ್ಥಿತಿಗಳಿಗೆ ಸೂಕ್ತವಾದ ಎಣ್ಣೆಕಾಳು ಬೆಳೆ. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಅಗತ್ಯ.",
    "onion": "ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಮಧ್ಯಮ ನೀರಾವರಿ ಅಗತ್ಯ. ಸಾಲುಗಳಲ್ಲಿ ಸರಿಯಾದ ಅಂತರದಲ್ಲಿ ಬೆಳೆಯಿರಿ.",
    "tomato": "ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ನಿಯಮಿತ ನೀರಾವರಿ ಅಗತ್ಯ. ಸಸ್ಯಗಳಿಗೆ ಬೆಂಬಲ ನೀಡಿ.",
    "chilli": "ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಮಧ್ಯಮ ನೀರಾವರಿ ಅಗತ್ಯ. ಕೀಟಗಳು ಮತ್ತು ರೋಗಗಳಿಗಾಗಿ ಗಮನವಿಡಿ.",
    "soybean": "ದ್ವಿದಳ ಧಾನ್ಯ ಬೆಳೆ. ಉತ್ತಮ ಒಳಚರಂಡಿ ಇರುವ ಮಣ್ಣು ಮತ್ತು ಮಧ್ಯಮ ಮಳೆ ಅಗತ್ಯ."
}

# Kannada Notes
NOTES_KN = [
    "ಈ ಶಿಫಾರಸುಗಳು ಸಮಗ್ರ ಮಣ್ಣಿನ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಸುಧಾರಿತ ML ಮುನ್ಸೂಚನೆಗಳನ್ನು ಆಧರಿಸಿವೆ.",
    "ಸ್ಥಳೀಯ ಪರಿಸ್ಥಿತಿಗಳು, ಹವಾಮಾನ ಮಾದರಿಗಳು ಮತ್ತು ಕೃಷಿ ಪದ್ಧತಿಗಳ ಆಧಾರದ ಮೇಲೆ ನೈಜ ಫಲಿತಾಂಶಗಳು ಬದಲಾಗಬಹುದು.",
    "ಪ್ರಮುಖ ಕೃಷಿ ನಿರ್ಧಾರಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುವ ಮೊದಲು ಸ್ಥಳೀಯ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    "ಬೆಳೆ ನಿರ್ವಹಣೆಗಾಗಿ ನಿಯಮಿತ ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ (ಪ್ರತಿ 2-3 ವರ್ಷಗಳಿಗೊಮ್ಮೆ) ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ.",
    "ದೀರ್ಘಕಾಲೀನ ಮಣ್ಣಿನ ಆರೋಗ್ಯಕ್ಕಾಗಿ ಬೆಳೆ ಬದಲಾವಣೆ ಮತ್ತು ಸಾವಯವ ಕೃಷಿ ಪದ್ಧತಿಗಳನ್ನು ಪರಿಗಣಿಸಿ.",
    "ಹವಾಮಾನ ಮುನ್ಸೂಚನೆಗಳನ್ನು ಗಮನಿಸಿ ಮತ್ತು ಅದಕ್ಕೆ ಅನುಗುಣವಾಗಿ ನೀರಾವರಿ ವೇಳಾಪಟ್ಟಿಗಳನ್ನು ಹೊಂದಿಸಿ."
]

def translate_dynamic_text(text, translations):
    """
    Translate dynamic text by replacing known phrases.
    This is a simple keyword-based translation for generated sentences.
    """
    if not text:
        return text
        
    translated = text
    # Sort translations by length (descending) to match longest phrases first
    sorted_phrases = sorted(translations.keys(), key=len, reverse=True)
    
    for phrase in sorted_phrases:
        if phrase in translated:
            translated = translated.replace(phrase, translations[phrase])
            
    return translated


# Crop rainfall requirements (min, max) in mm
CROP_RAINFALL_REQ = {
    'rice': (1000, 2000), 'wheat': (400, 800), 'maize': (500, 800),
    'cotton': (500, 1000), 'sugarcane': (1500, 2500), 'coconut': (1000, 2000),
    'apple': (600, 1200), 'banana': (1000, 2500), 'blackgram': (400, 600),
    'chickpea': (400, 600), 'coffee': (1500, 2500), 'grapes': (500, 800),
    'jute': (1000, 2000), 'kidneybeans': (400, 600), 'lentil': (400, 600),
    'mango': (800, 1500), 'mothbeans': (400, 600), 'mungbean': (400, 600),
    'muskmelon': (400, 600), 'orange': (800, 1500), 'papaya': (1000, 2000),
    'pigeonpeas': (600, 1000), 'pomegranate': (500, 800), 'watermelon': (400, 600),
    'jowar': (450, 750), 'bajra': (400, 650), 'ragi': (500, 900),
    'greengram': (400, 600), 'sunflower': (500, 750), 'groundnut': (500, 800),
    'safflower': (400, 650), 'onion': (500, 700), 'tomato': (600, 900),
    'chilli': (600, 900), 'soybean': (600, 1000)
}

# Color scheme
PRIMARY_COLOR = colors.HexColor('#2c5530')  # Dark green
SECONDARY_COLOR = colors.HexColor('#4a7c59')  # Medium green
ACCENT_COLOR = colors.HexColor('#6b9f78')  # Light green
WARNING_COLOR = colors.HexColor('#d4a574')  # Orange
SUCCESS_COLOR = colors.HexColor('#2ecc71')  # Green
DANGER_COLOR = colors.HexColor('#e74c3c')  # Red

def format_number(value, decimals=1, is_integer=False):
    """Format number with thousand separators"""
    if value is None:
        return "N/A"
    if is_integer:
        return f"{int(value):,}"
    return f"{float(value):,.{decimals}f}"

def create_npk_chart(data, include_images=True):
    """Create a professional NPK bar chart with ideal ranges"""
    if not include_images:
        return None
    try:
        fig, ax = plt.subplots(figsize=(6, 4))
        nutrients = ['Nitrogen\n(N)', 'Phosphorus\n(P)', 'Potassium\n(K)']
        values = [data.get('N', 0), data.get('P', 0), data.get('K', 0)]
        
        # Ideal ranges for visualization
        ideal_ranges = [
            (40, 120),  # N
            (20, 60),   # P
            (20, 100)   # K
        ]
        
        x_pos = [0, 1, 2]
        
        # Create bars for current values
        bars = ax.bar(x_pos, values, width=0.4, label='Current', 
                     color=['#3498db', '#e67e22', '#9b59b6'], 
                     edgecolor='white', linewidth=2, alpha=0.9)
        
        # Add ideal range zones (shaded rectangles)
        for i, (low, high) in enumerate(ideal_ranges):
            # Green zone (ideal)
            ax.add_patch(patches.Rectangle((i-0.4, low), 0.8, high-low, 
                                          fill=True, alpha=0.15, color='green', 
                                          linewidth=0))
            
            # Add range text
            ax.text(i, high + 5, f'Ideal: {low}-{high}', 
                   ha='center', va='bottom', fontsize=7, style='italic')
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(nutrients, fontsize=9)
        ax.set_title('Soil NPK Levels vs Ideal Ranges', fontsize=12, fontweight='bold', pad=15)
        ax.set_ylabel('mg/kg', fontsize=10, fontweight='bold')
        ax.set_ylim(0, max(max(values) * 1.4, max([r[1] for r in ideal_ranges]) * 1.2))
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                   f'{value:.1f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
        ax.legend(loc='upper right', fontsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        tmpfile_path = tmpfile.name
        tmpfile.close()
        
        plt.savefig(tmpfile_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        return tmpfile_path
    except Exception as e:
        print(f"Error creating NPK chart: {e}")
        return None

def create_soil_health_chart(soil_health, include_images=True):
    """Create a soil health breakdown chart"""
    if not include_images or not soil_health or not soil_health.get('breakdown'):
        return None
    try:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        breakdown = soil_health['breakdown']
        components = [k.replace('_', ' ').title() for k in breakdown.keys()]
        scores = list(breakdown.values())
        
        colors_pie = ['#2ecc71', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']
        bars = ax.barh(components, scores, color=colors_pie[:len(components)], edgecolor='white', linewidth=1.5, alpha=0.9)
        ax.set_title('Soil Health Component Scores', fontsize=12, fontweight='bold')
        ax.title.set_position([0.5, 1.05])
        ax.set_xlabel('Score (points)', fontsize=10, fontweight='bold')
        ax.set_xlim(0, max(scores) * 1.2 if scores else 50)
        
        # Add value labels
        for bar, score in zip(bars, scores):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{score:.1f}',
                   ha='left', va='center', fontsize=9, fontweight='bold')
        
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        
        # Create temp file
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        tmpfile_path = tmpfile.name
        tmpfile.close()
        
        plt.savefig(tmpfile_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        return tmpfile_path
    except Exception as e:
        print(f"Error creating soil health chart: {e}")
        return None

def create_rainfall_chart(data, predicted_crop, include_images=True):
    """Create rainfall vs crop suitability chart with sufficiency status"""
    if not include_images:
        return None
    try:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        rainfall = data.get('rainfall', 0)
        
        crop_lower = predicted_crop.lower()
        if crop_lower in CROP_RAINFALL_REQ:
            min_req, max_req = CROP_RAINFALL_REQ[crop_lower]
            avg_req = (min_req + max_req) / 2
            
            # Determine sufficiency status
            if rainfall < min_req:
                status = 'Deficient'
                status_color = '#e74c3c'
                diff = min_req - rainfall
            elif rainfall > max_req:
                status = 'Excessive'
                status_color = '#f39c12'
                diff = rainfall - max_req
            else:
                status = 'Sufficient'
                status_color = '#2ecc71'
                diff = 0
            
            categories = ['Current\nRainfall', 'Minimum\nRequired', 'Optimal\nRange', 'Maximum\nRequired']
            values = [rainfall, min_req, avg_req, max_req]
            colors_bars = [status_color, '#95a5a6', '#3498db', '#95a5a6']
            
            bars = ax.bar(categories, values, color=colors_bars, alpha=0.8, edgecolor='white', linewidth=1.5)
            
            # Add value labels
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 20,
                       f'{value:.0f} mm',
                       ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            ax.set_title(f'Rainfall Analysis for {predicted_crop.title()}', 
                        fontsize=12, fontweight='bold')
            ax.set_ylabel('Rainfall (mm)', fontsize=10, fontweight='bold')
            
            # Add status text
            ax.text(0.5, 0.95, f'Status: {status}', 
                   transform=ax.transAxes, ha='center', va='top',
                   fontsize=10, fontweight='bold', color=status_color,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor=status_color, linewidth=2))
            
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        else:
            # Fallback if crop not in requirements
            ax.text(0.5, 0.5, f'Rainfall data for {predicted_crop} not available',
                   ha='center', va='center', transform=ax.transAxes, fontsize=10)
        
        plt.tight_layout()
        
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        tmpfile_path = tmpfile.name
        tmpfile.close()
        
        plt.savefig(tmpfile_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        return tmpfile_path
    except Exception as e:
        print(f"Error creating rainfall chart: {e}")
        return None

def create_health_indicator(score, category):
    """Create a small color indicator for soil health"""
    try:
        fig, ax = plt.subplots(figsize=(1, 1))
        ax.axis('off')
        
        # Color based on score - using hex colors directly for matplotlib compatibility
        if score >= 80:
            color = '#2ecc71'  # Green
        elif score >= 60:
            color = '#d4a574'  # Orange
        else:
            color = '#e74c3c'  # Red
        
        # Draw circle
        circle = patches.Circle((0.5, 0.5), 0.4, color=color, alpha=0.8)
        ax.add_patch(circle)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        tmpfile_path = tmpfile.name
        tmpfile.close()
        
        plt.savefig(tmpfile_path, dpi=100, bbox_inches='tight', facecolor='white', transparent=True)
        plt.close()
        return tmpfile_path
    except Exception as e:
        print(f"Error creating health indicator: {e}")
        return None

def calculate_weather_suitability(data, predicted_crop):
    """Calculate weather suitability score and interpretation"""
    crop_lower = predicted_crop.lower()
    
    # Optimal temperature ranges for crops (°C)
    temp_ranges = {
        'rice': (20, 35), 'wheat': (10, 25), 'maize': (18, 32), 'cotton': (21, 35),
        'sugarcane': (20, 35), 'jowar': (25, 32), 'bajra': (26, 35), 'ragi': (20, 30),
        'sunflower': (20, 30), 'chilli': (20, 30), 'tomato': (18, 27), 'onion': (13, 25),
        'soybean': (20, 30), 'groundnut': (22, 30), 'safflower': (15, 25),
        # Add defaults for others
    }
    
    # Optimal humidity ranges (%)
    humidity_ranges = {
        'rice': (70, 90), 'wheat': (50, 70), 'cotton': (50, 70), 'jowar': (45, 65),
        'bajra': (40, 60), 'chilli': (50, 70), 'tomato': (60, 80), 'onion': (60, 70),
        # Defaults
    }
    
    temp = data.get('temperature', 25)
    humidity = data.get('humidity', 60)
    rainfall = data.get('rainfall', 500)
    
    # Get optimal ranges
    temp_opt = temp_ranges.get(crop_lower, (15, 35))
    hum_opt = humidity_ranges.get(crop_lower, (50, 80))
    rain_opt = CROP_RAINFALL_REQ.get(crop_lower, (400, 1000))
    
    # Score calculations (0-10 scale)
    scores = {}
    interpretations = {}
    
    # Temperature score
    if temp_opt[0] <= temp <= temp_opt[1]:
        scores['temperature'] = 10
        interpretations['temperature'] = f"✓ Temperature {temp:.1f}°C is ideal for {predicted_crop}"
    elif temp < temp_opt[0]:
        diff = temp_opt[0] - temp
        scores['temperature'] = max(0, 10 - diff * 0.5)
        interpretations['temperature'] = f"⚠ Temperature {temp:.1f}°C is below optimal range ({temp_opt[0]}-{temp_opt[1]}°C); crop growth may be slower"
    else:
        diff = temp - temp_opt[1]
        scores['temperature'] = max(0, 10 - diff * 0.5)
        interpretations['temperature'] = f"⚠ Temperature {temp:.1f}°C is above optimal range ({temp_opt[0]}-{temp_opt[1]}°C); heat stress may occur"
    
    # Humidity score
    if hum_opt[0] <= humidity <= hum_opt[1]:
        scores['humidity'] = 10
        interpretations['humidity'] = f"✓ Humidity {humidity:.1f}% is ideal for {predicted_crop} — reduces disease risk"
    elif humidity < hum_opt[0]:
        diff = hum_opt[0] - humidity
        scores['humidity'] = max(0, 10 - diff * 0.2)
        interpretations['humidity'] = f"⚠ Humidity {humidity:.1f}% is lower than ideal ({hum_opt[0]}-{hum_opt[1]}%); increase irrigation"
    else:
        diff = humidity - hum_opt[1]
        scores['humidity'] = max(0, 10 - diff * 0.2)
        interpretations['humidity'] = f"⚠ Humidity {humidity:.1f}% is high ({hum_opt[0]}-{hum_opt[1]}% ideal); fungal disease risk increased"
    
    # Rainfall score
    if rain_opt[0] <= rainfall <= rain_opt[1]:
        scores['rainfall'] = 10
        interpretations['rainfall'] = f"✓ Rainfall {rainfall:.0f} mm is sufficient for {predicted_crop}"
    elif rainfall < rain_opt[0]:
        diff_pct = ((rain_opt[0] - rainfall) / rain_opt[0]) * 100
        scores['rainfall'] = max(0, 10 - diff_pct * 0.1)
        interpretations['rainfall'] = f"⚠ Rainfall {rainfall:.0f} mm is below requirement ({rain_opt[0]}-{rain_opt[1]} mm); irrigation strongly recommended"
    else:
        diff_pct = ((rainfall - rain_opt[1]) / rain_opt[1]) * 100
        scores['rainfall'] = max(0, 10 - diff_pct * 0.1)
        interpretations['rainfall'] = f"⚠ Rainfall {rainfall:.0f} mm is excessive ({rain_opt[0]}-{rain_opt[1]} mm ideal); ensure proper drainage"
    
    # Overall suitability score
    overall_score = (scores['temperature'] + scores['humidity'] + scores['rainfall']) / 3
    
    # Traffic light remark
    if overall_score >= 8.5:
        remark = "🟢 Excellent"
        remark_text = "Weather conditions are excellent for this crop"
    elif overall_score >= 7:
        remark = "🟢 Good"
        remark_text = "Weather conditions are good for this crop"
    elif overall_score >= 5:
        remark = "🟡 Moderate"
        remark_text = "Weather conditions are moderate; some management needed"
    else:
        remark = "🔴 Poor"
        remark_text = "Weather conditions are challenging; consider alternatives"
    
    return {
        'overall_score': overall_score,
        'scores': scores,
        'interpretations': interpretations,
        'remark': remark,
        'remark_text': remark_text
    }

def generate_warnings_observations(data, predicted_crop):
    """Generate warnings and observations based on soil and weather data"""
    warnings = []
    observations = []
    
    # NPK warnings
    if data.get('N', 0) < 40:
        warnings.append("⚠ Nitrogen low → Apply compost or urea")
    elif data.get('N', 0) > 120:
        warnings.append("⚠ Nitrogen excessive → Reduce nitrogen application")
    else:
        observations.append("✓ Nitrogen level optimal")
    
    if data.get('P', 0) < 20:
        warnings.append("⚠ Phosphorus low → Apply rock phosphate or bone meal")
    elif data.get('P', 0) > 60:
        warnings.append("⚠ Phosphorus excessive → May interfere with micronutrients")
    else:
        observations.append("✓ Phosphorus level optimal")
    
    if data.get('K', 0) < 20:
        warnings.append("⚠ Potassium low → Apply potash or wood ash")
    elif data.get('K', 0) > 100:
        warnings.append("⚠ Potassium excessive → May cause magnesium deficiency")
    else:
        observations.append("✓ Potassium level optimal")
    
    # pH warnings
    ph = data.get('ph', 7)
    if ph < 6.0:
        warnings.append(f"⚠ Soil acidic (pH {ph:.1f}) → Add lime to raise pH")
    elif ph > 8.0:
        warnings.append(f"⚠ Soil alkaline (pH {ph:.1f}) → Add gypsum to lower pH")
    else:
        observations.append(f"✓ pH optimal ({ph:.1f})")
    
    # Weather warnings
    crop_lower = predicted_crop.lower()
    rainfall = data.get('rainfall', 0)
    if crop_lower in CROP_RAINFALL_REQ:
        min_req, max_req = CROP_RAINFALL_REQ[crop_lower]
        if rainfall < min_req:
            warnings.append(f"⚠ Rainfall below optimal → Increase irrigation")
        elif rainfall > max_req:
            warnings.append(f"⚠ Rainfall excessive → Ensure proper drainage")
    
    temp = data.get('temperature', 25)
    if temp > 35:
        warnings.append("⚠ Temperature high → Provide shade or mulching")
    elif temp < 15:
        warnings.append("⚠ Temperature low → Consider protective covering")
    
    # Soil type suitability
    soil_type = str(data.get('soil_type', '')).lower()
    if soil_type:
        observations.append(f"✓ Soil type: {soil_type.title()}")
    
    return {'warnings': warnings, 'observations': observations}

def add_header_footer(canvas, doc):
    """Draw header and footer on each page"""
    canvas.saveState()
    
    # Header - Branding
    canvas.setFont("Helvetica-Bold", 14)
    canvas.setFillColor(PRIMARY_COLOR)
    canvas.drawString(2*cm, A4[1] - 1.5*cm, "Soil Health & Crop Recommendation System")
    
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(2*cm, A4[1] - 2*cm, "🌾 Powered by ML + IoT + Weather Intelligence")
    
    # Footer with page numbers
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor('#666666'))
    
    page_num = canvas.getPageNumber()
    footer_text = f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} | Page {page_num}"
    
    footer_width = canvas.stringWidth(footer_text, "Helvetica", 8)
    canvas.drawString((A4[0] - footer_width) / 2, 1*cm, footer_text)
    
    # Line separators
    canvas.setStrokeColor(PRIMARY_COLOR)
    canvas.setLineWidth(2)
    canvas.line(2*cm, A4[1] - 2.3*cm, A4[0] - 2*cm, A4[1] - 2.3*cm)
    
    canvas.setStrokeColor(colors.HexColor('#cccccc'))
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.5*cm, A4[0] - 2*cm, 1.5*cm)
    
    canvas.restoreState()

def t(text, lang):
    """Translate text if language is Kannada, otherwise return English"""
    if lang == 'en':
        return text
    return TRANSLATIONS.get(text, text)

def _generate_report_content(data, story, styles, temp_files, lang='en'):
    """Generate the content for a single language section"""
    
    # Determine font based on language
    font_name = KANNADA_FONT if lang == 'kn' else 'Helvetica'
    bold_font = KANNADA_FONT if lang == 'kn' else 'Helvetica-Bold'
    
    # Custom styles with colored backgrounds
    title_style = ParagraphStyle(
        f'CustomTitle_{lang}',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=PRIMARY_COLOR,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName=bold_font
    )
    
    # Blue heading for soil analysis
    heading_blue_style = ParagraphStyle(
        f'HeadingBlue_{lang}',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.white,
        spaceAfter=12,
        spaceBefore=15,
        fontName=bold_font,
        backColor=colors.HexColor('#3498db'),
        borderPadding=8,
        leftIndent=8
    )
    
    # Green heading for recommendations
    heading_green_style = ParagraphStyle(
        f'HeadingGreen_{lang}',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.white,
        spaceAfter=12,
        spaceBefore=15,
        fontName=bold_font,
        backColor=PRIMARY_COLOR,
        borderPadding=8,
        leftIndent=8
    )
    
    # Orange heading for market/warnings
    heading_orange_style = ParagraphStyle(
        f'HeadingOrange_{lang}',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.white,
        spaceAfter=12,
        spaceBefore=15,
        fontName=bold_font,
        backColor=colors.HexColor('#f39c12'),
        borderPadding=8,
        leftIndent=8
    )
    
    subheading_style = ParagraphStyle(
        f'CustomSubHeading_{lang}',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=SECONDARY_COLOR,
        spaceAfter=8,
        fontName=bold_font
    )
    
    normal_style = ParagraphStyle(
        f'CustomNormal_{lang}',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        alignment=TA_LEFT,
        leading=12,
        fontName=font_name
    )
    
    bullet_style = ParagraphStyle(
        f'BulletStyle_{lang}',
        parent=normal_style,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=4,
        fontName=font_name
    )
    
    # Title
    title = Paragraph(t("Soil Health & Crop Recommendation Report", lang), title_style)
    story.append(title)
    story.append(Spacer(1, 0.3*cm))
    
    # Date
    date_str = datetime.utcnow().strftime('%B %d, %Y')
    date_text = f"{t('Report Date', lang)}: {date_str}"
    date_para = Paragraph(date_text, normal_style)
    story.append(date_para)
    story.append(Spacer(1, 0.5*cm))
    
    # Farmer Information Table
    farmer_data = [
        [t('Farmer Information', lang), ''],
        [f"{t('Name', lang)}:", Paragraph(str(data.get('farmer_name', 'N/A')), normal_style)],
        [f"{t('Phone', lang)}:", str(data.get('phone', 'N/A'))],
        [f"{t('Location', lang)}:", Paragraph(str(data.get('location', 'N/A')), normal_style)],
        [f"{t('Land Size', lang)}:", f"{format_number(data.get('land_size', 0), decimals=2)} {t('acres', lang)}"]
    ]
    
    farmer_table = Table(farmer_data, colWidths=[5*cm, 12*cm])
    farmer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), bold_font),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    story.append(KeepTogether(farmer_table))
    story.append(Spacer(1, 0.5*cm))
    
    # Soil & Weather Data Table
    soil_data = [
        [t('Parameter', lang), t('Value', lang), t('Unit', lang)],
        [t('Nitrogen', lang) + ' (N)', format_number(data.get('N', 0), decimals=1), 'mg/kg'],
        [t('Phosphorus', lang) + ' (P)', format_number(data.get('P', 0), decimals=1), 'mg/kg'],
        [t('Potassium', lang) + ' (K)', format_number(data.get('K', 0), decimals=1), 'mg/kg'],
        ['pH', format_number(data.get('ph', 0), decimals=2), ''],
        [t('Temperature', lang), format_number(data.get('temperature', 0), decimals=1), '°C'],
        [t('Humidity', lang), format_number(data.get('humidity', 0), decimals=1), '%'],
        [t('Rainfall', lang), format_number(data.get('rainfall', 0), decimals=1), 'mm'],
        [t('Soil Type', lang), t(str(data.get('soil_type', 'N/A')).title(), lang), '']
    ]
    
    soil_table = Table(soil_data, colWidths=[6*cm, 5.5*cm, 5.5*cm])
    soil_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (2, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), bold_font),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e8f5e9')),
        ('BACKGROUND', (1, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#c8e6c9')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    story.append(KeepTogether(soil_table))
    story.append(Spacer(1, 0.5*cm))
    
    # Soil Health Score Section
    if data.get('soil_health'):
        soil_health = data['soil_health']
        health_heading = Paragraph(clean_text(f"📊 {t('Soil Health Assessment', lang)}", lang), heading_blue_style)
        story.append(health_heading)
        
        score = soil_health.get('overall_score', 0)
        category = soil_health.get('category', 'Unknown')
        
        # Translate category
        category_trans = t(category, lang)
        
        # Create health indicator (only for English to avoid dups, or reuse)
        # We reuse the same image path if passed in temp_files
        indicator_path = create_health_indicator(score, category) 
        if indicator_path:
            temp_files.append(indicator_path)
        
        # Overall Score Display
        score_data = [
            [t('Overall Soil Health Score', lang), f'{score:.1f}/100', category_trans]
        ]
        
        if indicator_path:
            try:
                indicator_img = Image(indicator_path, width=0.8*cm, height=0.8*cm)
                score_data[0].append(indicator_img)
            except:
                pass
        
        health_table = Table(score_data, colWidths=[6.5*cm, 4.5*cm, 4*cm, 2*cm])
        health_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), ACCENT_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (2, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), bold_font),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(health_table)
        story.append(Spacer(1, 0.3*cm))
        
        # Component Breakdown
        if soil_health.get('breakdown'):
            breakdown_data = [[t('Component', lang), t('Score', lang), t('Points', lang)]]
            for component, score_val in soil_health['breakdown'].items():
                comp_name = component.replace('_', ' ').title()
                # Simple translation for components if needed, or keep English
                breakdown_data.append([comp_name, f"{score_val:.1f}", t('Points', lang)])
            
            breakdown_table = Table(breakdown_data, colWidths=[8*cm, 4.5*cm, 4.5*cm])
            breakdown_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), SECONDARY_COLOR),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 1), (2, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), bold_font),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('FONTNAME', (0, 1), (-1, -1), font_name),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f7f2')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#a5d6a7')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ]))
            story.append(breakdown_table)
        
        # Soil Health Chart
        health_chart_path = create_soil_health_chart(soil_health, True)
        if health_chart_path:
            temp_files.append(health_chart_path)
            try:
                story.append(Spacer(1, 0.3*cm))
                chart_img = Image(health_chart_path, width=15*cm, height=8.75*cm)
                story.append(chart_img)
            except Exception as e:
                story.append(Paragraph(f"Note: Soil health chart could not be displayed. Error: {str(e)}", normal_style))
        
        story.append(Spacer(1, 0.5*cm))
    
    # Weather Suitability Analysis Section
    predicted_crop = data.get('predicted_crop', 'N/A')
    if predicted_crop and predicted_crop != 'N/A':
        weather_suit = calculate_weather_suitability(data, predicted_crop)
        
        weather_heading = Paragraph(clean_text(f"🌤️ {t('Weather Suitability for', lang)} {predicted_crop.title()}", lang), heading_orange_style)
        story.append(weather_heading)
        
        # Overall suitability score
        remark_trans = t(weather_suit['remark'].split(' ')[1], lang) # Extract text part
        suit_para = Paragraph(
            f"<b>{t('Overall Suitability Score', lang)}:</b> {weather_suit['overall_score']:.1f}/10 &nbsp;&nbsp; {weather_suit['remark'][0]} {remark_trans}",
            normal_style
        )
        story.append(suit_para)
        story.append(Spacer(1, 0.2*cm))
        
        # Interpretations
        for key, interpretation in weather_suit['interpretations'].items():
            clean_interp = clean_text(interpretation, lang)
            # Try to translate known phrases in interpretation ONLY if language is Kannada
            if lang == 'kn':
                for en_phrase, kn_phrase in TRANSLATIONS.items():
                    if en_phrase in clean_interp:
                        clean_interp = clean_interp.replace(en_phrase, kn_phrase)
            
            interp_para = Paragraph(f"• {clean_interp}", bullet_style)
            story.append(interp_para)
        
        story.append(Spacer(1, 0.5*cm))
    
    # Recommended Crop Section
    crop_heading = Paragraph(clean_text(f"🌾 {t('Recommended Crop', lang)}", lang), heading_green_style)
    story.append(crop_heading)
    
    confidence = data.get('confidence', 0)
    
    crop_data = [
        [t('Predicted Crop', lang), f'{predicted_crop.title()}'],
        [t('Confidence Level', lang), f'{confidence:.1f}%']
    ]
    
    crop_table = Table(crop_data, colWidths=[5*cm, 12*cm])
    crop_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#e8f5e9')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), bold_font),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('FONTNAME', (1, 0), (1, -1), font_name),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1.5, PRIMARY_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(KeepTogether(crop_table))
    story.append(Spacer(1, 0.3*cm))
    
    # NPK Chart
    npk_chart_path = create_npk_chart(data, True)
    if npk_chart_path:
        temp_files.append(npk_chart_path)
        chart_heading = Paragraph("Soil NPK Levels Visualization", subheading_style)
        story.append(chart_heading)
        try:
            chart_img = Image(npk_chart_path, width=15*cm, height=10*cm)
            story.append(chart_img)
        except Exception as e:
            story.append(Paragraph(f"Note: NPK chart could not be displayed. Error: {str(e)}", normal_style))
        story.append(Spacer(1, 0.3*cm))
    
    # Rainfall Chart
    rainfall_chart_path = create_rainfall_chart(data, predicted_crop, True)
    if rainfall_chart_path:
        temp_files.append(rainfall_chart_path)
        rainfall_heading = Paragraph(t("Rainfall Analysis", lang), subheading_style)
        story.append(rainfall_heading)
        if rainfall_chart_path:
            try:
                chart_img = Image(rainfall_chart_path, width=15*cm, height=8.75*cm)
                story.append(chart_img)
            except Exception as e:
                story.append(Paragraph(f"Note: Rainfall chart could not be displayed. Error: {str(e)}", normal_style))
        story.append(Spacer(1, 0.5*cm))
    
    # Warnings & Observations Section
    warn_obs = generate_warnings_observations(data, predicted_crop)
    if warn_obs['warnings'] or warn_obs['observations']:
        warnings_heading = Paragraph(clean_text(f"⚠️ {t('Warnings & Observations', lang)}", lang), heading_orange_style)
        story.append(warnings_heading)
        
        # Warnings
        if warn_obs['warnings']:
            warning_para = Paragraph(f"<b>{t('Action Required', lang)}:</b>", normal_style)
            story.append(warning_para)
            for warning in warn_obs['warnings']:
                clean_warning = clean_text(warning, lang)
                # Try to translate known phrases ONLY if language is Kannada
                if lang == 'kn':
                    for en_phrase, kn_phrase in TRANSLATIONS.items():
                        if en_phrase in clean_warning:
                            clean_warning = clean_warning.replace(en_phrase, kn_phrase)
                
                warning_bullet = Paragraph(f"{clean_warning}", bullet_style)
                story.append(warning_bullet)
            story.append(Spacer(1, 0.2*cm))
        
        # Observations
        if warn_obs['observations']:
            obs_para = Paragraph(f"<b>{t('Positive Indicators', lang)}:</b>", normal_style)
            story.append(obs_para)
            for obs in warn_obs['observations']:
                clean_obs = clean_text(obs, lang)
                # Try to translate known phrases ONLY if language is Kannada
                if lang == 'kn':
                    for en_phrase, kn_phrase in TRANSLATIONS.items():
                        if en_phrase in clean_obs:
                            clean_obs = clean_obs.replace(en_phrase, kn_phrase)
                
                obs_bullet = Paragraph(f"{clean_obs}", bullet_style)
                story.append(obs_bullet)
        
        story.append(Spacer(1, 0.5*cm))
    
    # Market Price Information
    market_recommendation = data.get("market_recommendation")
    if market_recommendation:
        market_heading = Paragraph(clean_text(f"📊 {t('Market Price Trends', lang)}", lang), heading_orange_style)
        story.append(market_heading)
        
        if market_recommendation.get("current_price_range"):
            price_range = market_recommendation["current_price_range"]
            price_data = [
                [t('Price', lang) + ' ' + t('Range', lang), f'{price_range["min"]} - {price_range["max"]} ₹/Quintal'],
                [t('Average', lang) + ' ' + t('Price', lang), f'{price_range["average"]} ₹/Quintal']
            ]
            
            price_table = Table(price_data, colWidths=[5*cm, 12*cm])
            price_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), SECONDARY_COLOR),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), bold_font),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('FONTNAME', (0, 1), (-1, -1), font_name),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(price_table)
            story.append(Spacer(1, 0.2*cm))
        
        if market_recommendation.get("best_market"):
            best_market = market_recommendation["best_market"]
            # Translate market info dynamically
            market_text = f"<b>{t('Best Market', lang)}:</b> {best_market['name']}, {best_market['state']} ({best_market['price']} {best_market['unit']})"
            if lang == 'kn':
                market_text = translate_dynamic_text(market_text, TRANSLATIONS)
                
            market_info = Paragraph(market_text, normal_style)
            story.append(market_info)
            story.append(Spacer(1, 0.2*cm))
        
        if market_recommendation.get("recommendation"):
            rec_text = f"<b>{t('Market Advice', lang)}:</b> {market_recommendation['recommendation']}"
            if lang == 'kn':
                rec_text = translate_dynamic_text(rec_text, TRANSLATIONS)
            
            rec_para = Paragraph(rec_text, normal_style)
            story.append(rec_para)
        
        story.append(Spacer(1, 0.3*cm))
    
    # Soil Treatment Recommendations
    treatment_heading = Paragraph(clean_text(f"🌱 {t('Soil Treatment Recommendations', lang)}", lang), heading_green_style)
    story.append(treatment_heading)
    
    soil_treatment = data.get("soil_treatment", [])
    if soil_treatment:
        for suggestion in soil_treatment:
            clean_suggestion = clean_text(suggestion, lang)
            if lang == 'kn':
                clean_suggestion = translate_dynamic_text(clean_suggestion, TRANSLATIONS)
                
            if clean_suggestion:
                treatment_para = Paragraph(f"• {clean_suggestion}", bullet_style)
                story.append(treatment_para)
    else:
        no_treatment = Paragraph("No specific soil treatment recommendations available.", normal_style)
        story.append(no_treatment)
    story.append(Spacer(1, 0.3*cm))
    
    # Fertilizer Recommendations
    fertilizer_heading = Paragraph(clean_text(f"📦 {t('Fertilizer Recommendations', lang)}", lang), heading_green_style)
    story.append(fertilizer_heading)
    
    fertilizer_estimate = data.get("fertilizer_estimate", "")
    if fertilizer_estimate:
        # Split the fertilizer estimate into lines
        fertilizer_lines = fertilizer_estimate.split('\n')
        
        # Process each line with proper formatting
        for line in fertilizer_lines:
            if line.strip():
                clean_line = clean_text(line.strip(), lang)
                
                # Skip separator lines
                if clean_line.startswith('═') or clean_line.startswith('─'):
                    continue
                
                # Handle different types of lines
                if 'FERTILIZER RECOMMENDATIONS FOR' in clean_line:
                    continue
                elif clean_line.startswith('FARM DETAILS') or clean_line.startswith('FERTILIZER APPLICATION SCHEDULE') or clean_line.startswith('ORGANIC & BIO-FERTILIZER') or clean_line.startswith('SOIL NUTRIENT STATUS'):
                    # Translate headers
                    if lang == 'kn':
                        clean_line = translate_dynamic_text(clean_line, TRANSLATIONS)
                    story.append(Paragraph(f"<b>{clean_line}</b>", subheading_style))
                elif clean_line.startswith('🔹'):
                    if lang == 'kn':
                        clean_line = translate_dynamic_text(clean_line, TRANSLATIONS)
                    story.append(Paragraph(f"<b>{clean_line}</b>", normal_style))
                elif clean_line.startswith('Application Method:'):
                    if lang == 'kn':
                        clean_line = translate_dynamic_text(clean_line, TRANSLATIONS)
                    story.append(Paragraph(f"<i>{clean_line}</i>", normal_style))
                elif clean_line.startswith('•'):
                    if lang == 'kn':
                        clean_line = translate_dynamic_text(clean_line, TRANSLATIONS)
                    story.append(Paragraph(clean_line, bullet_style))
                elif clean_line.startswith('└─') or clean_line.startswith('✓'):
                    if lang == 'kn':
                        clean_line = translate_dynamic_text(clean_line, TRANSLATIONS)
                    story.append(Paragraph(clean_line, bullet_style))
                elif clean_line.startswith('Note:'):
                    if lang == 'kn':
                        clean_line = translate_dynamic_text(clean_line, TRANSLATIONS)
                    story.append(Paragraph(f"<i>{clean_line}</i>", normal_style))
                elif clean_line:
                    if lang == 'kn':
                        clean_line = translate_dynamic_text(clean_line, TRANSLATIONS)
                    story.append(Paragraph(clean_line, normal_style))
            else:
                story.append(Spacer(1, 0.05*cm))
    else:
        no_fert = Paragraph("Fertilizer recommendations not available for this crop.", normal_style)
        story.append(no_fert)
    story.append(Spacer(1, 0.3*cm))
    
    # Crop-Specific Tips
    crop = predicted_crop.lower() if predicted_crop else ""
    if crop in CROP_TIPS:
        tips_heading = Paragraph(clean_text(f"🌿 {t('Crop-Specific Tips for', lang)} {predicted_crop.title()}", lang), heading_green_style)
        story.append(tips_heading)
        
        tip_text = CROP_TIPS[crop]
        if lang == 'kn' and crop in CROP_TIPS_KN:
            tip_text = CROP_TIPS_KN[crop]
            
        tip_para = Paragraph(tip_text, normal_style)
        story.append(tip_para)
        story.append(Spacer(1, 0.3*cm))
    
    # Additional Notes
    notes_heading = Paragraph(clean_text(f"📝 {t('Additional Notes & Disclaimer', lang)}", lang), heading_blue_style)
    story.append(notes_heading)
    
    notes = [
        "These recommendations are based on comprehensive soil analysis and advanced ML predictions.",
        "Actual results may vary based on local conditions, weather patterns, and farming practices.",
        "Consult with local agricultural experts before making major farming decisions.",
        "Regular soil testing (every 2-3 years) is recommended for optimal crop management.",
        "Consider crop rotation and organic farming practices for long-term soil health.",
        "Monitor weather forecasts and adjust irrigation schedules accordingly."
    ]
    
    if lang == 'kn':
        notes = NOTES_KN
    
    for note in notes:
        note_para = Paragraph(f"• {note}", bullet_style)
        story.append(note_para)

def generate_pdf(data: dict, filename: str = "report.pdf", include_images: bool = True):
    """Generate a bilingual (English + Kannada) PDF report"""
    # Get absolute path for reports directory
    module_dir = Path(__file__).parent.parent.parent
    reports_dir = module_dir / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Create absolute filename
    if not os.path.isabs(filename):
        filename = str(reports_dir / filename)
    
    # Create document with custom canvas
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=2.5*cm
    )
    
    # Set PDF metadata
    doc.title = "Soil Health & Crop Recommendation Report"
    doc.author = "Soil Health & Crop Recommendation System"
    doc.subject = f"Crop Recommendation for {data.get('farmer_name', 'Farmer')}"
    
    story = []
    styles = getSampleStyleSheet()
    temp_files = []
    
    # 1. Generate English Section
    _generate_report_content(data, story, styles, temp_files, lang='en')
    
    # 2. Add Page Break
    story.append(PageBreak())
    
    # 3. Generate Kannada Section
    _generate_report_content(data, story, styles, temp_files, lang='kn')
    
    # Build PDF with custom canvas
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    
    # Clean up temporary files
    for temp_file in temp_files:
        try:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        except Exception as e:
            print(f"Warning: Could not delete temp file {temp_file}: {e}")

    print(f"✅ Saved Bilingual PDF at: {filename}")
    return filename
