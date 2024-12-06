import pandas as pd
from blockchain import PoABlockchain, Validator
from encryption import encrypt_data, decrypt_data
from ml_model import map_and_fill
from config import DATA_PATH, ENCRYPTED_DATA_PATH, RESULT_PATH
import joblib
from time import time

def main():
    try:
        # Step 1: Load the dataset
        print("Loading dataset...")
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
        dataset = pd.read_csv(DATA_PATH)
        print("Dataset loaded successfully.")

        # Step 2: Encrypt the data
        print("Encrypting data...")
        encrypted_data = encrypt_data(dataset)
        encrypted_data.to_csv(ENCRYPTED_DATA_PATH, index=False)
        print(f"Encrypted data saved to {ENCRYPTED_DATA_PATH}")

        # Step 3: Initialize validators and blockchain
        print("Initializing blockchain...")
        validator_1 = Validator("Validator_1")
        validator_2 = Validator("Validator_2")
        validators = [validator_1, validator_2]
        blockchain = PoABlockchain(validators)

        # Step 4: Add encrypted data to the blockchain
        print("Adding encrypted data to the blockchain...")
        for _, row in encrypted_data.iterrows():
            patient_data = row.to_dict()
            blockchain.add_block(patient_data=patient_data, prediction=None, validator=validator_1)
        print("Encrypted data added to the blockchain successfully.")

        # Step 5: Load the machine learning model
        print("Loading the ML model and preprocessor...")
        model_path = "backend/ml_model/model.pkl"
        preprocessor_path = "backend/ml_model/preprocessor.pkl"
        model = joblib.load(model_path)
        preprocessor = joblib.load(preprocessor_path)
        print("ML model and preprocessor loaded successfully.")

        # Step 6: Predict disease for each patient
        print("Predicting diseases for patients...")
        decrypted_data = decrypt_data(encrypted_data)
        preprocessed_data = preprocessor.transform(map_and_fill(decrypted_data))
        predictions = model.predict(preprocessed_data)

        # Step 7: Add predictions to the blockchain
        print("Adding predictions to the blockchain...")
        for idx, prediction in enumerate(predictions):
            blockchain.chain[idx + 1].prediction = prediction
        print("Predictions added to the blockchain successfully.")

        # Step 8: Save results to `results.csv`
        print("Saving results to results.csv...")
        results = decrypted_data.copy()
        results["Prediction"] = predictions
        results.to_csv(RESULT_PATH, index=False)
        print(f"Results saved to {RESULT_PATH}")

        # Step 9: Validate the blockchain
        print("Validating the blockchain...")
        is_valid = blockchain.is_chain_valid()
        print(f"Is blockchain valid? {is_valid}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()








# from utils import read_csv, write_csv
# from encryption.homomorphic import encrypt_data
# from blockchain.blockchain import Blockchain
# from ml_model.ml_pipeline import predict_on_encrypted_data

# def main():
#     # Step 1: Load dataset
#     data = read_csv("/home/tsoien/github/MLResearch/backend/data/Disease_symptom_and_patient_profile_dataset.csv")

#     # Step 2: Encrypt data
#     encrypted_data = encrypt_data(data)
#     write_csv("/home/tsoien/github/MLResearch/backend/data/Disease_symptom_and_patient_profile_dataset.csv", encrypted_data)

#     # Step 3: Initialize blockchain
#     blockchain = Blockchain()
#     blockchain.add_transaction(encrypted_data)

#     # Step 4: Apply ML model
#     predictions = predict_on_encrypted_data(encrypted_data)
#     write_csv("d/home/tsoien/github/MLResearch/backend/data/Disease_symptom_and_patient_profile_dataset.csvcl", predictions)

#     print("Process completed successfully!")

# if __name__ == "__main__":
#     main()
