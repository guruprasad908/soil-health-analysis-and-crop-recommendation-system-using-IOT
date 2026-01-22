"""
Reinforcement Learning Model for Crop Recommendation
Learns from farmer feedback and self-improves over time
Uses Q-Learning approach with experience replay
"""

import sys
import os
# Add parent directory to path so we can import from app.main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import json
from datetime import datetime

# Import the class from app.main so pickle can find it
from app.main import CropRecommendationRL


# Load dataset
print("=" * 70)
print("🧠 REINFORCEMENT LEARNING MODEL TRAINING")
print("=" * 70)

print("\n📊 Loading North Karnataka dataset...")
data = pd.read_csv("data/north_karnataka_crops.csv")
print(f"✅ Dataset loaded: {data.shape[0]} samples")

# Get unique crops
crops = sorted(data['label'].unique())
print(f"✅ Crops: {len(crops)} unique crops")

# Encode soil types
soil_encoder = LabelEncoder()
data['soil_type_encoded'] = soil_encoder.fit_transform(data['soil_type'])

# Create RL model
print("\n🤖 Initializing Reinforcement Learning Model...")
rl_model = CropRecommendationRL(
    crops=crops,
    learning_rate=0.1,
    discount_factor=0.95,
    epsilon=0.2
)
print("✅ Model initialized!")

# Pre-train with existing dataset (bootstrap learning)
print("\n🔄 Pre-training with historical data...")
print("   (Simulating farmer feedback from dataset)")

train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

correct_predictions = 0
total_samples = len(train_data)

for idx, row in train_data.iterrows():
    features = {
        'N': row['N'],
        'P': row['P'],
        'K': row['K'],
        'temperature': row['temperature'],
        'humidity': row['humidity'],
        'ph': row['ph'],
        'rainfall': row['rainfall'],
        'soil_type_encoded': row['soil_type_encoded']
    }
    
    actual_crop = row['label']
    
    # Get prediction
    predicted_crop, confidence = rl_model.predict(features)
    
    # Simulate reward
    if predicted_crop == actual_crop:
        reward = 1.0  # Perfect match
        correct_predictions += 1
    else:
        reward = -0.5  # Wrong prediction
    
    # Update model
    rl_model.update(features, predicted_crop, actual_crop, reward)
    
    if (idx + 1) % 1000 == 0:
        accuracy = correct_predictions / (idx + 1)
        print(f"   Progress: {idx + 1}/{total_samples} samples | Accuracy: {accuracy:.2%}")

print(f"✅ Pre-training complete!")

# Test on test set
print("\n📈 Testing on test set...")
test_correct = 0
for idx, row in test_data.iterrows():
    features = {
        'N': row['N'],
        'P': row['P'],
        'K': row['K'],
        'temperature': row['temperature'],
        'humidity': row['humidity'],
        'ph': row['ph'],
        'rainfall': row['rainfall'],
        'soil_type_encoded': row['soil_type_encoded']
    }
    
    predicted_crop, confidence = rl_model.predict(features)
    if predicted_crop == row['label']:
        test_correct += 1

test_accuracy = test_correct / len(test_data)
print(f"✅ Test Accuracy: {test_accuracy:.2%}")

# Display statistics
print("\n" + "=" * 70)
print("📊 MODEL STATISTICS")
print("=" * 70)
stats = rl_model.get_stats()
for key, value in stats.items():
    print(f"   {key:25s}: {value}")

# Save model
print("\n💾 Saving Reinforcement Learning Model...")
model_path = "app/models/rl_model.joblib"
joblib.dump(rl_model, model_path)
print(f"✅ Model saved: {model_path}")

# Save soil encoder
encoder_path = "app/models/rl_soil_encoder.joblib"
joblib.dump(soil_encoder, encoder_path)
print(f"✅ Soil encoder saved: {encoder_path}")

# Save metadata
metadata = {
    'model_type': 'Reinforcement Learning (Q-Learning)',
    'crops': crops,
    'training_date': datetime.now().isoformat(),
    'training_samples': len(train_data),
    'test_samples': len(test_data),
    'test_accuracy': float(test_accuracy),
    'hyperparameters': {
        'learning_rate': rl_model.learning_rate,
        'discount_factor': rl_model.discount_factor,
        'epsilon': rl_model.epsilon
    },
    'stats': stats
}

metadata_path = "app/models/rl_model_metadata.json"
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"✅ Metadata saved: {metadata_path}")

print("\n" + "=" * 70)
print("✅ REINFORCEMENT LEARNING MODEL READY!")
print("=" * 70)
print(f"\nTest Accuracy: {test_accuracy:.2%}")
print(f"States Explored: {stats['states_explored']}")
print(f"Success Rate: {stats['success_rate']:.2%}")

print("\n📦 Saved Files:")
print("   • rl_model.joblib")
print("   • rl_soil_encoder.joblib")
print("   • rl_model_metadata.json")

print("\n🎯 How It Works:")
print("   1. Model learns from farmer feedback over time")
print("   2. Uses Q-Learning to improve recommendations")
print("   3. Balances exploration (new crops) vs exploitation (proven crops)")
print("   4. Continuously adapts to real-world results")

print("\n🔄 Next Steps:")
print("   1. Integrate into main.py")
print("   2. Add feedback endpoint for farmers to rate recommendations")
print("   3. Model will self-improve with each feedback!")
print("\n" + "=" * 70)
