import os
import requests
from tqdm import tqdm
import json

# 🔑 Your Pexels API key
PEXELS_API_KEY = "51CSGTgl4Svc165Y2v7wo5yJYwSjx8Dj5vRkuzdjPl5xxqZsyUBxUJCp"

# 🧩 More precise fertilizer-related topics for Pexels search
image_topics = {
    "nitrogen_fertilizer": "nitrogen fertilizer agriculture field closeup",
    "phosphorus_fertilizer": "phosphate fertilizer soil crop roots",
    "potassium_fertilizer": "potash fertilizer potassium granules soil",
    "compost_fertilizer": "compost heap organic manure farming",
    "farmyard_manure": "cow dung manure field organic farming",
    "vermicompost": "vermicompost worms composting bin",
    "rhizobium_culture": "rhizobium bacteria root nodules legumes",
    "mycorrhiza_fungi": "mycorrhiza fungi plant roots symbiosis",
    "fertilizer_application": "farmer applying fertilizer field crop",
    "fertigation_method": "fertigation drip irrigation greenhouse",
    "organic_fertilizer": "organic fertilizer agriculture",
    "soil_health": "soil test fertility nutrients",
    "biofertilizer_bacteria": "biofertilizer microbial culture agriculture",
    "nutrient_management": "crop nutrient management precision farming",
}

# 🗂 Destination folder
output_folder = r"C:\Users\admin\Desktop\major project phase 1\soil_crop_recommender\frontend\src\assets\images"
os.makedirs(output_folder, exist_ok=True)

headers = {"Authorization": PEXELS_API_KEY}

def download_image(topic, filename):
    """Fetch and download the first relevant image from Pexels."""
    url = f"https://api.pexels.com/v1/search?query={topic}&per_page=1&orientation=landscape"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])
            if photos:
                image_url = photos[0]["src"]["large2x"]
                img_data = requests.get(image_url, stream=True, timeout=15)
                file_path = os.path.join(output_folder, f"{filename}.jpg")
                with open(file_path, "wb") as f:
                    for chunk in img_data.iter_content(1024):
                        f.write(chunk)
                return True
            else:
                print(f"⚠️ No results found for '{topic}'")
        else:
            print(f"⚠️ Request failed ({response.status_code}) for '{filename}'")
    except Exception as e:
        print(f"❌ Error downloading '{filename}': {e}")
    return False


print(f"\n📸 Downloading {len(image_topics)} fertilizer images via Pexels API...\n")

for key, topic in tqdm(image_topics.items(), desc="Downloading Images"):
    success = download_image(topic, key)
    if success:
        tqdm.write(f"✅ Saved: {key}.jpg")
    else:
        tqdm.write(f"❌ Skipped: {key}")

# 🧾 Generate JSON map for React
image_map = {k: f"./assets/images/{k}.jpg" for k in image_topics.keys()}
json_path = os.path.join(os.path.dirname(output_folder), "fertilizerImageMap.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(image_map, f, indent=2)

print(f"\n✨ Done! All images saved to:\n{output_folder}")
print(f"🗂  JSON map saved as: {json_path}")
