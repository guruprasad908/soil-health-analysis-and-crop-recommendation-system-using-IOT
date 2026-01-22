from PIL import Image, ImageDraw
import os

# Create textures directory if it doesn't exist
textures_dir = "frontend/src/assets/textures"
os.makedirs(textures_dir, exist_ok=True)

# Create a soil texture
soil_img = Image.new('RGB', (100, 100), '#8B4513')  # Brown color
draw = ImageDraw.Draw(soil_img)
# Add some texture details
for i in range(0, 100, 10):
    for j in range(0, 100, 10):
        if (i + j) % 20 == 0:
            draw.rectangle([i, j, i+5, j+5], fill='#A0522D')

soil_img.save(os.path.join(textures_dir, "soil.png"))

# Create a default crop texture
default_img = Image.new('RGB', (100, 100), '#32CD32')  # Green color
draw = ImageDraw.Draw(default_img)
# Add some texture details
for i in range(0, 100, 20):
    draw.line([i, 0, i, 100], fill='#228B22', width=2)
    draw.line([0, i, 100, i], fill='#228B22', width=2)

default_img.save(os.path.join(textures_dir, "default_crop.png"))

# Create specific crop textures
crops = {
    "pigeonpeas": "#FFD700",  # Gold
    "wheat": "#F0E68C",       # Khaki
    "mustard": "#FFA500",     # Orange
    "chickpea": "#DAA520",    # Goldenrod
}

for crop, color in crops.items():
    crop_img = Image.new('RGB', (100, 100), color)
    draw = ImageDraw.Draw(crop_img)
    # Add some texture details
    for i in range(0, 100, 15):
        draw.ellipse([i, i, i+10, i+10], fill='#8B4513', outline='#654321')
    
    filename = f"{crop}.png"
    crop_img.save(os.path.join(textures_dir, filename))

print("Texture files generated successfully!")