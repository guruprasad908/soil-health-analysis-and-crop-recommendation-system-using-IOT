"""
Train ML models specifically for North Karnataka crops dataset
Saves models with '_nk' suffix to differentiate from original models
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("🌾 NORTH KARNATAKA CROP RECOMMENDATION MODEL TRAINING")
print("=" * 70)

# Load North Karnataka dataset
print("\n📊 Loading North Karnataka dataset...")
data = pd.read_csv("data/north_karnataka_crops.csv")
print(f"✅ Dataset loaded: {data.shape[0]} samples, {data.shape[1]} features")
print(f"✅ Crops: {sorted(data['label'].unique())}")

# Encode soil_type
print("\n🔄 Encoding soil types...")
soil_encoder = LabelEncoder()
data['soil_type_encoded'] = soil_encoder.fit_transform(data['soil_type'])
print(f"✅ Soil types: {list(soil_encoder.classes_)}")

# Define features and label
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_type_encoded']]
y = data['label']

print(f"✅ Features: {list(X.columns)}")
print(f"✅ Target: {len(y.unique())} unique crops")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True, stratify=y
)
print(f"✅ Train set: {X_train.shape[0]} samples")
print(f"✅ Test set: {X_test.shape[0]} samples")

# Train individual models
print("\n" + "=" * 70)
print("🤖 TRAINING MODELS")
print("=" * 70)

models = {}
scores = {}

# 1. Random Forest
print("\n🌲 Training Random Forest...")
rf_model = RandomForestClassifier(n_estimators=200, max_depth=25, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_score = accuracy_score(y_test, rf_pred)
models['Random Forest'] = rf_model
scores['Random Forest'] = rf_score
print(f"   ✅ Accuracy: {rf_score:.4f} ({rf_score*100:.2f}%)")

# 2. Gradient Boosting
print("\n🚀 Training Gradient Boosting...")
gb_model = GradientBoostingClassifier(n_estimators=150, max_depth=10, random_state=42)
gb_model.fit(X_train, y_train)
gb_pred = gb_model.predict(X_test)
gb_score = accuracy_score(y_test, gb_pred)
models['Gradient Boosting'] = gb_model
scores['Gradient Boosting'] = gb_score
print(f"   ✅ Accuracy: {gb_score:.4f} ({gb_score*100:.2f}%)")

# 3. Decision Tree
print("\n🌳 Training Decision Tree...")
dt_model = DecisionTreeClassifier(max_depth=25, random_state=42)
dt_model.fit(X_train, y_train)
dt_pred = dt_model.predict(X_test)
dt_score = accuracy_score(y_test, dt_pred)
models['Decision Tree'] = dt_model
scores['Decision Tree'] = dt_score
print(f"   ✅ Accuracy: {dt_score:.4f} ({dt_score*100:.2f}%)")

# 4. AdaBoost
print("\n⚡ Training AdaBoost...")
ada_model = AdaBoostClassifier(n_estimators=100, random_state=42)
ada_model.fit(X_train, y_train)
ada_pred = ada_model.predict(X_test)
ada_score = accuracy_score(y_test, ada_pred)
models['AdaBoost'] = ada_model
scores['AdaBoost'] = ada_score
print(f"   ✅ Accuracy: {ada_score:.4f} ({ada_score*100:.2f}%)")

# 5. Stacking Classifier (Best ensemble)
print("\n🎯 Training Stacking Classifier...")
stacking_model = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=200, max_depth=25, random_state=42, n_jobs=-1)),
        ('gb', GradientBoostingClassifier(n_estimators=150, max_depth=10, random_state=42)),
        ('dt', DecisionTreeClassifier(max_depth=25, random_state=42)),
        ('ada', AdaBoostClassifier(n_estimators=100, random_state=42))
    ],
    final_estimator=LogisticRegression(max_iter=1000, random_state=42),
    cv=5,
    n_jobs=-1
)
stacking_model.fit(X_train, y_train)
stacking_pred = stacking_model.predict(X_test)
stacking_score = accuracy_score(y_test, stacking_pred)
models['Stacking'] = stacking_model
scores['Stacking'] = stacking_score
print(f"   ✅ Accuracy: {stacking_score:.4f} ({stacking_score*100:.2f}%)")

# Display results
print("\n" + "=" * 70)
print("📊 MODEL PERFORMANCE SUMMARY")
print("=" * 70)
for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
    print(f"   {name:25s}: {score:.4f} ({score*100:.2f}%)")

# Find best model
best_model_name = max(scores, key=scores.get)
best_model = models[best_model_name]
best_score = scores[best_model_name]

print("\n" + "=" * 70)
print(f"🏆 BEST MODEL: {best_model_name} ({best_score*100:.2f}%)")
print("=" * 70)

# Save models
print("\n💾 Saving models...")
models_dir = "app/models"

# Save all models with _nk suffix
joblib.dump(models['Random Forest'], f"{models_dir}/rf_model_nk.joblib")
print("   ✅ Random Forest saved: rf_model_nk.joblib")

joblib.dump(models['Gradient Boosting'], f"{models_dir}/gb_model_nk.joblib")
print("   ✅ Gradient Boosting saved: gb_model_nk.joblib")

joblib.dump(models['Decision Tree'], f"{models_dir}/dt_model_nk.joblib")
print("   ✅ Decision Tree saved: dt_model_nk.joblib")

joblib.dump(models['AdaBoost'], f"{models_dir}/ada_model_nk.joblib")
print("   ✅ AdaBoost saved: ada_model_nk.joblib")

joblib.dump(models['Stacking'], f"{models_dir}/stacking_model_nk.joblib")
print("   ✅ Stacking saved: stacking_model_nk.joblib")

joblib.dump(soil_encoder, f"{models_dir}/soil_encoder_nk.joblib")
print("   ✅ Soil encoder saved: soil_encoder_nk.joblib")

# Generate classification report for best model
print("\n" + "=" * 70)
print(f"📈 DETAILED REPORT - {best_model_name}")
print("=" * 70)
print(classification_report(y_test, best_model.predict(X_test), zero_division=0))

# Feature importance (if available)
if hasattr(best_model, 'feature_importances_'):
    print("\n" + "=" * 70)
    print("🔍 FEATURE IMPORTANCE")
    print("=" * 70)
    feature_names = ['N', 'P', 'K', 'Temperature', 'Humidity', 'pH', 'Rainfall', 'Soil Type']
    importances = best_model.feature_importances_
    for name, importance in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
        print(f"   {name:15s}: {importance:.4f} ({importance*100:.2f}%)")

print("\n" + "=" * 70)
print("✅ TRAINING COMPLETE!")
print("=" * 70)
print("\n📦 Saved Models:")
print("   • rf_model_nk.joblib")
print("   • gb_model_nk.joblib")
print("   • dt_model_nk.joblib")
print("   • ada_model_nk.joblib")
print("   • stacking_model_nk.joblib")
print("   • soil_encoder_nk.joblib")

print("\n🎯 Next Steps:")
print("   1. Update main.py to load these models")
print("   2. Add 'North Karnataka Model' to available models in frontend")
print("   3. Test predictions with real farmer cases")
print("   4. Collect feedback for continuous improvement")
print("\n" + "=" * 70)
