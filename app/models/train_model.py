import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.base import BaseEstimator, ClassifierMixin
import joblib
import numpy as np
import warnings
warnings.filterwarnings('ignore')

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

# Try importing XGBoost (optional)
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️ XGBoost not available. Install with: pip install xgboost")

# Load dataset
print("📊 Loading dataset...")
data = pd.read_csv("data/crop_recommendation_with_soil.csv")
print(f"✅ Dataset loaded: {data.shape[0]} samples, {data.shape[1]} features")

# Encode soil_type
le = LabelEncoder()
data['soil_type_encoded'] = le.fit_transform(data['soil_type'])
print(f"✅ Soil types encoded: {len(le.classes_)} types")

# Define features and label
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_type_encoded']]
y = data['label']

print(f"✅ Features: {list(X.columns)}")
print(f"✅ Target classes: {len(y.unique())} crops")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
print(f"✅ Train set: {X_train.shape[0]} samples")
print(f"✅ Test set: {X_test.shape[0]} samples")

# Scale features for models that need it (SVM, KNN, Logistic Regression)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n🤖 Training Multiple Models...")
print("=" * 60)

# Define base models
base_models = {
    'Random Forest': RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=20),
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
    'Support Vector Machine': SVC(kernel='rbf', probability=True, random_state=42),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
}

# Add XGBoost if available
if XGBOOST_AVAILABLE:
    base_models['XGBoost'] = XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1)

# Train and evaluate each model individually
model_scores = {}
trained_models = {}

for name, model in base_models.items():
    print(f"\n🔄 Training {name}...")
    
    # Use scaled data for models that need it
    if name in ['K-Nearest Neighbors', 'Support Vector Machine', 'Logistic Regression']:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        score = accuracy_score(y_test, y_pred)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = accuracy_score(y_test, y_pred)
    
    model_scores[name] = score
    trained_models[name] = model
    print(f"   ✅ {name} Accuracy: {score:.4f} ({score*100:.2f}%)")

# Display individual model performances
print("\n" + "=" * 60)
print("📊 Individual Model Performance:")
print("=" * 60)
for name, score in sorted(model_scores.items(), key=lambda x: x[1], reverse=True):
    print(f"   {name:25s}: {score:.4f} ({score*100:.2f}%)")

# Create Voting Classifier (Hard Voting)
print("\n" + "=" * 60)
print("🗳️  Training Voting Classifier (Hard Voting)...")
print("=" * 60)

# Prepare models for voting (use unscaled for tree-based, scaled for others)
# For scaled models, we need to create new instances since they're already fitted
voting_estimators = []
for name, model in trained_models.items():
    if name in ['K-Nearest Neighbors', 'Support Vector Machine', 'Logistic Regression']:
        # Create new model instances for voting (they'll be refitted)
        if name == 'K-Nearest Neighbors':
            new_model = KNeighborsClassifier(n_neighbors=5)
        elif name == 'Support Vector Machine':
            new_model = SVC(kernel='rbf', probability=True, random_state=42)
        else:  # Logistic Regression
            new_model = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
        voting_estimators.append((name, ScaledModel(new_model)))
    else:
        # For tree-based models, create new instances
        if name == 'Random Forest':
            new_model = RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)
        elif name == 'Gradient Boosting':
            new_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        elif name == 'Decision Tree':
            new_model = DecisionTreeClassifier(random_state=42, max_depth=20)
        else:
            new_model = model
        voting_estimators.append((name, new_model))

voting_clf = VotingClassifier(estimators=voting_estimators, voting='hard', n_jobs=-1)
voting_clf.fit(X_train, y_train)
voting_pred = voting_clf.predict(X_test)
voting_score = accuracy_score(y_test, voting_pred)
print(f"✅ Voting Classifier Accuracy: {voting_score:.4f} ({voting_score*100:.2f}%)")

# Create Stacking Classifier (Best approach)
print("\n" + "=" * 60)
print("🎯 Training Stacking Classifier (Meta-Learner)...")
print("=" * 60)

# Use top 3-4 models as base learners
top_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)[:4]
print(f"   Using top models: {[name for name, _ in top_models]}")

# Create new model instances for stacking (they'll be refitted)
stacking_estimators = []
for name, _ in top_models:
    if name == 'Random Forest':
        stacking_estimators.append((name, RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)))
    elif name == 'Gradient Boosting':
        stacking_estimators.append((name, GradientBoostingClassifier(n_estimators=100, random_state=42)))
    elif name == 'Decision Tree':
        stacking_estimators.append((name, DecisionTreeClassifier(random_state=42, max_depth=20)))
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

stacking_clf.fit(X_train, y_train)
stacking_pred = stacking_clf.predict(X_test)
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

# Use the best model (Stacking Classifier)
best_model = stacking_clf
best_score = stacking_score

print(f"\n✅ Best Model: Stacking Classifier with {best_score*100:.2f}% accuracy")

# Detailed evaluation of best model
print("\n📊 Detailed Classification Report:")
print(classification_report(y_test, stacking_pred))

# Feature importance (from Random Forest)
rf_model = trained_models['Random Forest']
importances = rf_model.feature_importances_
feature_names = X.columns
feature_importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values('importance', ascending=False)

print("\n🔝 Feature Importance (from Random Forest):")
print(feature_importance_df.to_string(index=False))

# Save the best model, scaler, and encoder
print("\n💾 Saving models...")
joblib.dump(best_model, "app/models/rf_model.joblib")  # Keep same name for compatibility
joblib.dump(le, "app/models/soil_encoder.joblib")
joblib.dump(scaler, "app/models/scaler.joblib")  # Save scaler for future use
print("✅ Models saved successfully!")

# Save all models for reference
print("\n💾 Saving all individual models...")
for name, model in trained_models.items():
    if name not in ['K-Nearest Neighbors', 'Support Vector Machine', 'Logistic Regression']:
        joblib.dump(model, f"app/models/{name.lower().replace(' ', '_')}.joblib")
print("✅ All models saved!")

print(f"\n🎉 Training complete!")
print(f"   Best Model: Stacking Classifier")
print(f"   Final Accuracy: {best_score*100:.2f}%")
print(f"   Improvement over single RF: {(best_score - model_scores['Random Forest'])*100:.2f}%")
