import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')))
from phe import paillier
import pandas as pd
from pathlib import Path
import joblib
import mysql.connector
from data_config import db_cred
from encryption.homomorphic import encrypt_data, decrypt_data

# Generate public/private keys
public_key, private_key = paillier.generate_paillier_keypair()

# Paths
MODEL_PATH = Path("/home/tsoien/github/MLResearch/backend/ml_model/model.joblib")
PREPROCESSOR_PATH = Path("/home/tsoien/github/MLResearch/backend/ml_model/preprocessor.joblib")
DATA_PATH = Path("/home/tsoien/github/MLResearch/backend/data/Disease_symptom_and_patient_profile_dataset.csv")
PROCESSED_DATA_PATH = Path("/home/tsoien/github/MLResearch/backend/data/processed_data.csv")

def map_and_fill(data):
    """Maps and fills missing values in the dataset."""
    mapping = {'Yes': 1, 'No': 0}
    gender_mapping = {'Male': 1, 'Female': 2}
    bp_mapping = {'Low': 1, 'Normal': 2, 'High': 3}
    cholesterol_mapping = {'Low': 1, 'Normal': 2, 'High': 3}

    columns_to_map = {
        'Fever': mapping,
        'Cough': mapping,
        'Fatigue': mapping,
        'Difficulty_Breathing': mapping,
        'Gender': gender_mapping,
        'Blood_Pressure': bp_mapping,
        'Cholesterol_Level': cholesterol_mapping,
    }

    for column, col_mapping in columns_to_map.items():
        if column in data.columns:
            data[column] = data[column].map(col_mapping).fillna(0)
        else:
            raise ValueError(f"Missing required column: {column}")

    return data

def save_predictions_to_mysql(predictions):
    db = db_cred()
    cursor = db.cursor()

    # Update the disease_data table with predictions
    for i, prediction in enumerate(predictions):
        sql = """
        UPDATE disease_data 
        SET Predicted_Outcome = %s 
        WHERE id = %s;
        """
        cursor.execute(sql, (prediction, i + 1))  # Assuming 'id' is the row index in the database
    db.commit()
    cursor.close()
    db.close()

def main():
    try:
        # Step 1: Load plain text data
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"Data not found at {DATA_PATH}")
        raw_data = pd.read_csv(DATA_PATH)
        print(f"Raw data loaded from {DATA_PATH}")

        # Step 2: Encrypt the data
        encrypted_data = encrypt_data(raw_data)
        print("Data encrypted successfully.")

        # Step 3: Decrypt the data for processing
        decrypted_data = decrypt_data(encrypted_data)
        print("Data decrypted successfully.")

        # Step 4: Map and fill missing values
        processed_data = map_and_fill(decrypted_data)
        print("Mapping and filling missing values completed.")

        # Step 5: Save raw processed data for debugging purposes
        processed_data.to_csv(PROCESSED_DATA_PATH, index=False)
        print(f"Processed data saved to {PROCESSED_DATA_PATH}")

        # Step 6: Load the preprocessor
        if not PREPROCESSOR_PATH.exists():
            raise FileNotFoundError(f"Preprocessor not found at {PREPROCESSOR_PATH}")
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        print(f"Preprocessor loaded from {PREPROCESSOR_PATH}")

        # Step 7: Apply preprocessing
        preprocessed_data = preprocessor.transform(processed_data)
        print("Data preprocessed successfully.")

        # Step 8: Load the model
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")

        # Step 9: Make predictions
        predictions = model.predict(preprocessed_data)
        print("Predictions generated successfully.")

        # Step 10: Calculate accuracy (if ground truth exists)
        if 'Outcome_Variable' in processed_data.columns:
            from sklearn.metrics import accuracy_score

            true_labels = processed_data['Outcome_Variable']
            accuracy = accuracy_score(true_labels, predictions)
            print(f"Accuracy of predictions: {accuracy:.2f}")
        else:
            print("Ground truth column 'Outcome Variable' not found. Accuracy cannot be calculated.")

        # Step 11: Output results
        processed_data["Predictions"] = predictions
        print(f"Predictions added to the dataset:\n{processed_data.head()}")
        
        # Step 12: Save predictions to MySQL
        save_predictions_to_mysql(predictions)
        print("Predictions saved to MySQL.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
