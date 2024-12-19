import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
import sys
from sqlalchemy import create_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data import db_cred
from blockchain import PoABlockchain, Validator
from encryption.homomorphic_mysql import encrypt_value, decrypt_value  # Importing the necessary homomorphic encryption functions
from ml_model import map_and_fill
from config import ENCRYPTED_DATA_PATH, RESULT_PATH, MODEL_PATH, PREPROCESSOR_PATH
import joblib
from time import time
import base64
from phe import paillier
import re

# Columns that should be encrypted
ENCRYPTION_COLUMNS = ['Gender', 'Fever', 'Cough', 'Fatigue', 'Difficulty_Breathing', 'Age', 'Blood_Pressure', 'Cholesterol_Level']

# Paillier encryption setup
public_key, private_key = paillier.generate_paillier_keypair()


def preprocess_data(data, preprocessor_path):
    """
    Preprocesses the data using the saved preprocessor pipeline.
    :param data: Raw decrypted DataFrame.
    :param preprocessor_path: Path to the preprocessor joblib file.
    :return: Preprocessed data ready for ML model.
    """
    if not os.path.exists(preprocessor_path):
        raise FileNotFoundError(f"Preprocessor not found at {preprocessor_path}")
    preprocessor = joblib.load(preprocessor_path)
    return preprocessor.transform(data)


def load_model(model_path):
    """
    Loads a trained ML model.
    :param model_path: Path to the model joblib file.
    :return: Loaded model object.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    return joblib.load(model_path)


def fetch_data_from_db():
    """
    Fetches patient data from MySQL database.
    :return: Raw patient data as a pandas DataFrame.
    """
    conn = db_cred()  # Call db_cred() to get the MySQL connection
    if conn is None:
        raise Exception("Failed to connect to the database.")
    
    query = "SELECT * FROM disease_data;"
    data = pd.read_sql(query, conn)
    conn.close()
    print("Data fetched from MySQL.")
    return data


def decrypt_data(encrypted_data):
    """
    Decrypts the encrypted values in the DataFrame.
    :param encrypted_data: DataFrame containing encrypted values.
    :return: Decrypted DataFrame.
    """
    decrypted_data = encrypted_data.copy()  # Start by copying the dataframe
    for column in encrypted_data.columns:
        decrypted_data[column] = encrypted_data[column].apply(decrypt_value)  # Decrypt individual values
    return decrypted_data


def insert_predictions_to_db(predictions):
    """
    Inserts prediction results into the MySQL database.
    :param predictions: List of predictions to insert.
    """
    db_config = db_cred()  # Call the db_cred() function to get the connection details
    if db_config is None:
        raise Exception("Failed to get database credentials.")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for idx, pred in enumerate(predictions):
        cursor.execute(
            "UPDATE disease_data SET prediction = %s WHERE id = %s",
            (pred, idx + 1)  # Assuming IDs start from 1
        )
    conn.commit()
    conn.close()
    print("Predictions saved to MySQL.")


def is_column_encrypted(column_data):
    """
    Determines if a column is encrypted by checking if its values match the expected encrypted format.
    :param column_data: pandas Series containing column values.
    :return: True if the column is encrypted, False otherwise.
    """
    try:
        # Attempt to decrypt the first non-null value
        for value in column_data.dropna().head():
            decrypted_value = decrypt_value(value)  # If decryption fails, the value is not encrypted
            if decrypted_value is None:
                return False
        return True
    except Exception:
        return False


ENCRYPTION_PATTERN = r"^[A-Za-z0-9+/=]+$"  # A basic check for base64-like encoding

def encrypt_value(value):
    """
    Encrypts a given value if it is not already encrypted.
    If the value is already encrypted (detected by a pattern), it returns the value as-is.
    """
    # Check if the value appears to be already encrypted (e.g., base64 or long ciphertext)
    if isinstance(value, str) and re.match(ENCRYPTION_PATTERN, value):
        print(f"Value already encrypted: {value}")
        return value  # Return the already encrypted value

    # If not encrypted, proceed with encryption
    try:
        numeric_value = float(value)  # Try to convert to numeric
        encrypted_value = encrypt_numeric(numeric_value)  # Your encryption function for numbers
        return encrypted_value
    except ValueError:
        # If not numeric, treat it as a string and encrypt it
        encrypted_value = encrypt_string(value)  # Your encryption function for strings
        return encrypted_value

def encrypt_numeric(value):
    """Encrypt numeric values."""
    # Add your encryption logic here for numeric values
    # For the sake of example, we return the value multiplied by a factor
    return value * 10  # Replace with your encryption logic

def encrypt_string(value):
    """Encrypt string values."""
    # Add your encryption logic here for string values
    # For the sake of example, we return the reversed string
    return value[::-1]  # Replace with your encryption logic

def fetch_data_from_mysql():
    """Fetch data from MySQL and return it as a DataFrame."""
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='password', database='mediChain')
        query = "SELECT * FROM disease_data"
        data = pd.read_sql(query, conn)
        conn.close()
        print("Data fetched from MySQL.")
        return data
    except Error as e:
        print(f"Error while fetching data from MySQL: {e}")
        return pd.DataFrame()

def encrypt_dataset(data):
    """
    Encrypt the dataset. If the value is already encrypted, it won't be encrypted again.
    """
    encrypted_data = data.copy()
    for col in encrypted_data.columns:
        encrypted_data[col] = encrypted_data[col].apply(lambda x: encrypt_value(x) if pd.notnull(x) else x)
    return encrypted_data


def main():
    # Step 1: Fetch Data from MySQL
    data = fetch_data_from_db()
    print("Dataset loaded from MySQL.")
    
    # Print the first few rows of the dataset
    print("Head of the dataset from MySQL:")
    print(data.head())

    # Step 2: Encrypt Data if necessary
    encrypted_data = encrypt_dataset(data)

    # Step 3: Decrypt the encrypted data (if you need to preprocess it for ML model)
    decrypted_data = decrypt_data(encrypted_data)
    print("Data decrypted for model processing.")


        


        # # Step 3: Decrypt and Preprocess Data
        # decrypted_data = decrypt_data(encrypted_data)  # Use decrypt_data, not decrypt_value for a DataFrame
        # processed_data = preprocess_data(map_and_fill(decrypted_data), PREPROCESSOR_PATH)
        # print("Data decrypted, mapped, and preprocessed.")

        # # Step 4: Make Predictions
        # model = load_model(MODEL_PATH)
        # if processed_data.shape[1] != model.n_features_in_:
        #     raise ValueError(f"Feature mismatch: Model expects {model.n_features_in_} features, but got {processed_data.shape[1]}")
        # predictions = model.predict(processed_data)
        # print("Predictions made.")

    #     # Step 5: Save Prediction Results to MySQL
    # insert_predictions_to_db(predictions)

    # # Step 6: Initialize Blockchain
    # validator_1 = Validator("Validator_1")
    # validators = [validator_1]
    # blockchain = PoABlockchain(validators)

    # # Step 7: Add Data and Predictions to Blockchain
    # block_timestamp = time()
    # blockchain.add_block(
    #     patient_data=encrypted_data.to_dict(),
    #     prediction=predictions.tolist(),
    #     validator=validator_1
    # )
    # print("Data and predictions added to blockchain.")

    # # Step 8: Validate Blockchain
    # print("Blockchain valid:", blockchain.is_chain_valid())

    # # Step 9: Print Blockchain Details
    # print("\nBlockchain Contents:")
    # for block in blockchain.chain:
    #     print(f"Block {block.index} | Timestamp: {block.timestamp} | Validator: {block.validator_name}")
    #     print(f"  Patient Data: {block.patient_data}")
    #     print(f"  Prediction: {block.prediction}")
    #     print(f"  Hash: {block.hash}")
    #     print("-" * 60)

if __name__ == "__main__":
    main()
