import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
from encryption.homomorphic import decrypt_data

# Paths
MODEL_PATH = Path("/home/tsoien/github/MLResearch/backend/ml_model/model.joblib")
PREPROCESSOR_PATH = Path("/home/tsoien/github/MLResearch/backend/ml_model/preprocessor.joblib")
DATA_PATH = Path("/home/tsoien/github/MLResearch/backend/data/Disease_symptom_and_patient_profile_dataset.csv")
PROCESSED_DATA_PATH = Path("/home/tsoien/github/MLResearch/backend/data/processed_data.csv")
RESULT_PATH = Path("/home/tsoien/github/MLResearch/backend/data/results.csv")

# Helper function to map and handle missing values
def map_and_fill(data):
    """Maps and fills missing values in the dataset."""
    mapping = {'Yes': 1, 'No': 0}
    gender_mapping = {'Male': 1, 'Female': 2}
    bp_mapping = {'Low': 1, 'Normal': 2, 'High': 3}
    cholesterol_mapping = {'Normal': 1, 'High': 2, 'Very High': 3}

    columns_to_map = {
        'Fever': mapping,
        'Cough': mapping,
        'Fatigue': mapping,
        'Difficulty Breathing': mapping,
        'Gender': gender_mapping,
        'Blood Pressure': bp_mapping,
        'Cholesterol Level': cholesterol_mapping,
    }

    for column, col_mapping in columns_to_map.items():
        if column in data.columns:
            data[column] = data[column].map(col_mapping).fillna(0)
        else:
            raise ValueError(f"Missing required column: {column}")

    return data

def main():
    try:
        # Step 1: Load encrypted data
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"Data not found at {DATA_PATH}")
        encrypted_data = pd.read_csv(DATA_PATH)
        print(f"Encrypted data loaded from {DATA_PATH}")

        # Step 2: Decrypt the data
        data = decrypt_data(encrypted_data)
        print("Data decrypted successfully.")

        # Step 3: Map and fill missing values
        data = map_and_fill(data)
        print("Mapping and filling missing values completed.")

        # Step 4: Save raw data for debugging purposes
        data.to_csv(PROCESSED_DATA_PATH, index=False)
        print(f"Processed data saved to {PROCESSED_DATA_PATH}")

        # Step 5: Load the preprocessor
        if not PREPROCESSOR_PATH.exists():
            raise FileNotFoundError(f"Preprocessor not found at {PREPROCESSOR_PATH}")
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        print(f"Preprocessor loaded from {PREPROCESSOR_PATH}")

        # Step 6: Apply preprocessing
        processed_data = preprocessor.transform(data)
        print("Data preprocessed successfully.")

        # Step 7: Load the model
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")

        # Step 8: Validate processed data shape
        print(f"Processed data shape: {processed_data.shape}")
        print(f"Model expects {model.n_features_in_} features")
        if processed_data.shape[1] != model.n_features_in_:
            raise ValueError(f"Feature mismatch! Model expects {model.n_features_in_} features, but got {processed_data.shape[1]} features")

        # Step 9: Make predictions
        predictions = model.predict(processed_data)
        print("Predictions generated successfully.")

        # # Step 10: Save results
        # results = data.copy()
        # results["Predictions"] = predictions
        # results.to_csv(RESULT_PATH, index=False)
        # print(f"Results saved to {RESULT_PATH}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
