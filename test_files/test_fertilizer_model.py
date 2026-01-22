import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

try:
    # ✅ Load Dataset
    print("Loading dataset...")
    data_path = os.path.join("data", "Fertilizer Prediction.csv")
    df = pd.read_csv(data_path)
    print("Data shape:", df.shape)
    print("First 5 rows:")
    print(df.head())

    # ✅ Encode Categorical Columns
    print("Encoding categorical columns...")
    cat_cols = ['Soil Type', 'Crop Type', 'Fertilizer Name']
    encoders = {}

    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    # ✅ Split Features and Target
    print("Splitting features and target...")
    X = df.drop('Fertilizer Name', axis=1)
    y = df['Fertilizer Name']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ✅ Train Model
    print("Training model...")
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # ✅ Evaluate
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # ✅ Save Model and Encoders
    print("Saving model and encoders...")
    # Create models directory if it doesn't exist
    os.makedirs("app/models", exist_ok=True)

    model_path = os.path.join("app", "models", "fertilizer_model.joblib")
    encoders_path = os.path.join("app", "models", "fertilizer_encoders.joblib")

    joblib.dump(model, model_path)
    joblib.dump(encoders, encoders_path)

    print("✅ Model and encoders saved successfully.")
    print(f"Model saved to: {model_path}")
    print(f"Encoders saved to: {encoders_path}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()