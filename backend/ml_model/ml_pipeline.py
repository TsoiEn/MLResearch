import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from pathlib import Path
from encryption.homomorphic import decrypt_data  # Now it should work
  # Assuming encryption module

# Load configuration for paths
MODEL_PATH = Path("/home/tsoien/github/MLResearch/backend/ml_model/model.joblib")
DATA_PATH = Path("/home/tsoien/github/MLResearch/backend/data/Disease_symptom_and_patient_profile_dataset.csv")  # Adjust to your encrypted dataset file
RESULT_PATH = Path("/home/tsoien/github/MLResearch/backend/data/results.csv")

def preprocess_data(data):
    """
    Preprocess the input data (e.g., decrypt, scale, encode).
    This is where the preprocessing pipeline for your model is applied.
    """
    # Define the preprocessing pipeline
    categorical_features = ['Disease', 'Gender', 'Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']
    
    # Check if columns like 'Blood Pressure' and 'Cholesterol Level' are categorical
    numerical_features = ['Age', 'Blood Pressure', 'Cholesterol Level']  # You might need to recheck these columns
    
    # If columns like 'Blood Pressure' and 'Cholesterol Level' are categorical, adjust as follows:
    # numerical_features = [] # If they are categorical, add them to categorical_features
    
    # Column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),  # Scale numerical columns
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),  # Encode categorical columns
        ]
    )
    
    return preprocessor


def load_model():
    """Load the trained machine learning model."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Trained model not found at {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
    return model

def make_predictions(model, data):
    """
    Use the trained model to make predictions on the processed data.
    """
    predictions = model.predict(data)
    return predictions

def main():
    # Step 1: Load the encrypted data
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Encrypted data not found at {DATA_PATH}")
    encrypted_data = pd.read_csv(DATA_PATH)
    print(f"Encrypted data loaded from {DATA_PATH}")
    
    # Step 2: Decrypt the data (if encrypted)
    data = decrypt_data(encrypted_data)  # Decrypt your data
    print("Data decrypted successfully.")
    
    # Step 3: Preprocess the data
    preprocessor = preprocess_data(data)
    processed_data = preprocessor.fit_transform(data)  # Fit-transform the input data
    
    # Step 4: Load the trained model
    model = load_model()
    
    # Step 5: Make predictions
    predictions = make_predictions(model, processed_data)
    print("Predictions generated successfully.")
    
    # Step 6: Save the results
    results = data.copy()
    results["Predictions"] = predictions
    results.to_csv(RESULT_PATH, index=False)
    print(f"Results saved to {RESULT_PATH}")

if __name__ == "__main__":
    main()
