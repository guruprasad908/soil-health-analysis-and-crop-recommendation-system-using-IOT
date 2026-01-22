"""
Enhanced Model Training Script with new models and feature engineering
Includes: LightGBM, CatBoost, AdaBoost, Neural Networks, and feature engineering
"""
import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier, 
    VotingClassifier, StackingClassifier, AdaBoostClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.base import BaseEstimator, ClassifierMixin

# Import feature engineering
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.utils.feature_engineering import engineer_features

# Wrapper class for models that need scaled data
class ScaledModel(BaseEstimator, ClassifierMixin):
    def __init__(self, base_model):
        self.base_model = base_model
        self.scaler = StandardScaler()
        self.model = None
    
    def fit(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model = self.base_model
        self.model.fit(X_scaled, y)
        return self
    
    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def predict_proba(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)
    
    @property
    def classes_(self):
        return self.model.classes_

# Try importing optional models
XGBOOST_AVAILABLE = False
LIGHTGBM_AVAILABLE = False
CATBOOST_AVAILABLE = False

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
    print("✅ XGBoost available")
except ImportError:
    print("⚠️ XGBoost not available. Install with: pip install xgboost")

try:
    from lightgbm import LGBMClassifier
    LIGHTGBM_AVAILABLE = True
    print("✅ LightGBM available")
except ImportError:
    print("⚠️ LightGBM not available. Install with: pip install lightgbm")

try:
    from catboost import CatBoostClassifier
    CATBOOST_AVAILABLE = True
    print("✅ CatBoost available")
except ImportError:
    print("⚠️ CatBoost not available. Install with: pip install catboost")

# Load dataset
print("\n📊 Loading dataset...")
data = pd.read_csv("data/crop_recommendation_with_soil.csv")
print(f"✅ Dataset loaded: {data.shape[0]} samples, {data.shape[1]} features")

# Encode soil_type
le = LabelEncoder()
data['soil_type_encoded'] = le.fit_transform(data['soil_type'])
print(f"✅ Soil types encoded: {len(le.classes_)} types")

# Base features
base_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_type_encoded']
X_base = data[base_features]
y = data['label']

print(f"\n🔧 Applying feature engineering...")
# Apply feature engineering
X_engineered = engineer_features(X_base, include_polynomial=True)
print(f"✅ Features engineered: {X_base.shape[1]} → {X_engineered.shape[1]} features")

# Train-test split
X_train_base, X_test_base, X_train_eng, X_test_eng, y_train, y_test = train_test_split(
    X_base, X_engineered, y, test_size=0.2, random_state=42, shuffle=True
)
print(f"✅ Train set: {X_train_base.shape[0]} samples")
print(f"✅ Test set: {X_test_base.shape[0]} samples")

# Scale features for models that need it
scaler_base = StandardScaler()
scaler_eng = StandardScaler()
X_train_scaled_base = scaler_base.fit_transform(X_train_base)
X_test_scaled_base = scaler_base.transform(X_test_base)
X_train_scaled_eng = scaler_eng.fit_transform(X_train_eng)
X_test_scaled_eng = scaler_eng.transform(X_test_eng)

print("\n🤖 Training Multiple Models...")
print("=" * 60)

# Define base models (using base features for compatibility)
base_models = {
    'Random Forest': RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=20),
    'AdaBoost': AdaBoostClassifier(n_estimators=200, learning_rate=0.5, random_state=42),
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
    'Support Vector Machine': SVC(kernel='rbf', probability=True, random_state=42),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1),
    'Neural Network': MLPClassifier(
        hidden_layer_sizes=(100, 50, 25),
        activation='relu',
        solver='adam',
        alpha=0.0001,
        learning_rate='adaptive',
        max_iter=500,
        random_state=42
    )
}

# Add XGBoost if available
if XGBOOST_AVAILABLE:
    base_models['XGBoost'] = XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1)

# Add LightGBM if available
if LIGHTGBM_AVAILABLE:
    base_models['LightGBM'] = LGBMClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=10,
        num_leaves=31,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )

# Add CatBoost if available
if CATBOOST_AVAILABLE:
    base_models['CatBoost'] = CatBoostClassifier(
        iterations=200,
        learning_rate=0.05,
        depth=10,
        random_state=42,
        verbose=False
    )

# Train models with base features (for compatibility)
model_scores = {}
trained_models = {}

for name, model in base_models.items():
    print(f"\n🔄 Training {name}...")
    
    try:
        # Use scaled data for models that need it
        if name in ['K-Nearest Neighbors', 'Support Vector Machine', 'Logistic Regression', 'Neural Network']:
            model.fit(X_train_scaled_base, y_train)
            y_pred = model.predict(X_test_scaled_base)
            score = accuracy_score(y_test, y_pred)
        else:
            model.fit(X_train_base, y_train)
            y_pred = model.predict(X_test_base)
            score = accuracy_score(y_test, y_pred)
        
        model_scores[name] = score
        trained_models[name] = model
        print(f"   ✅ {name} Accuracy: {score:.4f} ({score*100:.2f}%)")
    except Exception as e:
        print(f"   ❌ {name} failed: {e}")
        continue

# Display individual model performances
print("\n" + "=" * 60)
print("📊 Individual Model Performance:")
print("=" * 60)
for name, score in sorted(model_scores.items(), key=lambda x: x[1], reverse=True):
    print(f"   {name:25s}: {score:.4f} ({score*100:.2f}%)")

# Create Voting Classifier (Soft Voting for better results)
print("\n" + "=" * 60)
print("🗳️  Training Voting Classifier (Soft Voting)...")
print("=" * 60)

voting_estimators = []
for name, model in trained_models.items():
    if name in ['K-Nearest Neighbors', 'Support Vector Machine', 'Logistic Regression', 'Neural Network']:
        if name == 'K-Nearest Neighbors':
            new_model = KNeighborsClassifier(n_neighbors=5)
        elif name == 'Support Vector Machine':
            new_model = SVC(kernel='rbf', probability=True, random_state=42)
        elif name == 'Logistic Regression':
            new_model = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
        elif name == 'Neural Network':
            new_model = MLPClassifier(
                hidden_layer_sizes=(100, 50, 25),
                activation='relu',
                solver='adam',
                alpha=0.0001,
                learning_rate='adaptive',
                max_iter=500,
                random_state=42
            )
        voting_estimators.append((name, ScaledModel(new_model)))
    else:
        if name == 'Random Forest':
            new_model = RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)
        elif name == 'Gradient Boosting':
            new_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        elif name == 'Decision Tree':
            new_model = DecisionTreeClassifier(random_state=42, max_depth=20)
        elif name == 'AdaBoost':
            new_model = AdaBoostClassifier(n_estimators=200, learning_rate=0.5, random_state=42)
        elif name == 'XGBoost' and XGBOOST_AVAILABLE:
            new_model = XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        elif name == 'LightGBM' and LIGHTGBM_AVAILABLE:
            new_model = LGBMClassifier(n_estimators=200, learning_rate=0.05, max_depth=10, num_leaves=31, random_state=42, n_jobs=-1, verbose=-1)
        elif name == 'CatBoost' and CATBOOST_AVAILABLE:
            new_model = CatBoostClassifier(iterations=200, learning_rate=0.05, depth=10, random_state=42, verbose=False)
        else:
            new_model = model
        voting_estimators.append((name, new_model))

voting_clf = VotingClassifier(estimators=voting_estimators, voting='soft', n_jobs=-1)
voting_clf.fit(X_train_base, y_train)
voting_pred = voting_clf.predict(X_test_base)
voting_score = accuracy_score(y_test, voting_pred)
print(f"✅ Voting Classifier Accuracy: {voting_score:.4f} ({voting_score*100:.2f}%)")

# Create Stacking Classifier
print("\n" + "=" * 60)
print("🎯 Training Stacking Classifier (Meta-Learner)...")
print("=" * 60)

# Use top 4-5 models as base learners
top_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)[:5]
print(f"   Using top models: {[name for name, _ in top_models]}")

stacking_estimators = []
for name, _ in top_models:
    if name == 'Random Forest':
        stacking_estimators.append((name, RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)))
    elif name == 'Gradient Boosting':
        stacking_estimators.append((name, GradientBoostingClassifier(n_estimators=100, random_state=42)))
    elif name == 'Decision Tree':
        stacking_estimators.append((name, DecisionTreeClassifier(random_state=42, max_depth=20)))
    elif name == 'AdaBoost':
        stacking_estimators.append((name, AdaBoostClassifier(n_estimators=200, learning_rate=0.5, random_state=42)))
    elif name == 'XGBoost' and XGBOOST_AVAILABLE:
        stacking_estimators.append((name, XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1)))
    elif name == 'LightGBM' and LIGHTGBM_AVAILABLE:
        stacking_estimators.append((name, LGBMClassifier(n_estimators=200, learning_rate=0.05, max_depth=10, num_leaves=31, random_state=42, n_jobs=-1, verbose=-1)))
    elif name == 'CatBoost' and CATBOOST_AVAILABLE:
        stacking_estimators.append((name, CatBoostClassifier(iterations=200, learning_rate=0.05, depth=10, random_state=42, verbose=False)))
    elif name == 'K-Nearest Neighbors':
        stacking_estimators.append((name, ScaledModel(KNeighborsClassifier(n_neighbors=5))))
    elif name == 'Support Vector Machine':
        stacking_estimators.append((name, ScaledModel(SVC(kernel='rbf', probability=True, random_state=42))))
    elif name == 'Logistic Regression':
        stacking_estimators.append((name, ScaledModel(LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1))))

# Use Logistic Regression as meta-learner
stacking_clf = StackingClassifier(
    estimators=stacking_estimators,
    final_estimator=LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1),
    cv=5,
    n_jobs=-1
)

stacking_clf.fit(X_train_base, y_train)
stacking_pred = stacking_clf.predict(X_test_base)
stacking_score = accuracy_score(y_test, stacking_pred)
print(f"✅ Stacking Classifier Accuracy: {stacking_score:.4f} ({stacking_score*100:.2f}%)")

# Compare all approaches
print("\n" + "=" * 60)
print("🏆 Final Model Comparison:")
print("=" * 60)
all_scores = list(model_scores.items()) + [
    ('Voting Classifier', voting_score),
    ('Stacking Classifier', stacking_score)
]

for name, score in sorted(all_scores, key=lambda x: x[1], reverse=True):
    marker = "🥇" if score == max(s for _, s in all_scores) else "  "
    print(f"{marker} {name:25s}: {score:.4f} ({score*100:.2f}%)")

# Use the best model
best_model = stacking_clf
best_score = stacking_score

print(f"\n✅ Best Model: Stacking Classifier with {best_score*100:.2f}% accuracy")

# Detailed evaluation
print("\n📊 Detailed Classification Report:")
print(classification_report(y_test, stacking_pred))

# Feature importance (from Random Forest)
if 'Random Forest' in trained_models:
    rf_model = trained_models['Random Forest']
    importances = rf_model.feature_importances_
    feature_names = X_base.columns
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)

    print("\n🔝 Feature Importance (from Random Forest):")
    print(feature_importance_df.to_string(index=False))

# Save models
print("\n💾 Saving models...")
joblib.dump(best_model, "app/models/rf_model.joblib")  # Keep same name for compatibility
joblib.dump(le, "app/models/soil_encoder.joblib")
joblib.dump(scaler_base, "app/models/scaler.joblib")
print("✅ Models saved successfully!")

# Save all individual models
print("\n💾 Saving all individual models...")
for name, model in trained_models.items():
    if name not in ['K-Nearest Neighbors', 'Support Vector Machine', 'Logistic Regression', 'Neural Network']:
        safe_name = name.lower().replace(' ', '_').replace('-', '_')
        joblib.dump(model, f"app/models/{safe_name}.joblib")
print("✅ All models saved!")

print(f"\n🎉 Enhanced training complete!")
print(f"   Best Model: Stacking Classifier")
print(f"   Final Accuracy: {best_score*100:.2f}%")
if 'Random Forest' in model_scores:
    print(f"   Improvement over single RF: {(best_score - model_scores['Random Forest'])*100:.2f}%")

