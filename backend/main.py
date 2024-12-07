import pandas as pd
from blockchain import PoABlockchain, Validator
from encryption.homomorphic import encrypt_data, decrypt_data
from ml_model import map_and_fill
from config import DATA_PATH, ENCRYPTED_DATA_PATH, RESULT_PATH, MODEL_PATH, PREPROCESSOR_PATH
import joblib
from time import time

def preprocess_data(data, preprocessor_path):
    """
    Preprocesses the data using the saved preprocessor pipeline.
    :param data: Raw decrypted DataFrame.
    :param preprocessor_path: Path to the preprocessor joblib file.
    :return: Preprocessed data ready for ML model.
    """
    if not preprocessor_path.exists():
        raise FileNotFoundError(f"Preprocessor not found at {preprocessor_path}")
    preprocessor = joblib.load(preprocessor_path)
    return preprocessor.transform(data)

def load_model(model_path):
    """
    Loads a trained ML model.
    :param model_path: Path to the model joblib file.
    :return: Loaded model object.
    """
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    return joblib.load(model_path)

def main():
    # Step 1: Load Dataset
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
    data = pd.read_csv(DATA_PATH)
    print("Dataset loaded.")

    # Step 2: Encrypt Dataset
    encrypted_data = encrypt_data(data)
    encrypted_data.to_csv(ENCRYPTED_DATA_PATH, index=False)
    print(f"Encrypted dataset saved to {ENCRYPTED_DATA_PATH}.")

    # Step 3: Decrypt and Preprocess Data
    decrypted_data = decrypt_data(encrypted_data)
    processed_data = preprocess_data(map_and_fill(decrypted_data), PREPROCESSOR_PATH)
    print("Data decrypted, mapped, and preprocessed.")

    # Step 4: Make Predictions
    model = load_model(MODEL_PATH)
    if processed_data.shape[1] != model.n_features_in_:
        raise ValueError(f"Feature mismatch: Model expects {model.n_features_in_} features, but got {processed_data.shape[1]}")
    predictions = model.predict(processed_data)
    print("Predictions made.")

    # Step 5: Save Prediction Results
    results = data.copy()
    results["Predictions"] = predictions
    results.to_csv(RESULT_PATH, index=False)
    print(f"Results saved to {RESULT_PATH}.")

    # Step 6: Initialize Blockchain
    validator_1 = Validator("Validator_1")
    validators = [validator_1]
    blockchain = PoABlockchain(validators)

    # Step 7: Add Data and Predictions to Blockchain
    block_timestamp = time()
    blockchain.add_block(
        patient_data=encrypted_data.to_dict(),
        prediction=predictions.tolist(),
        validator=validator_1
    )
    print("Data and predictions added to blockchain.")

    # Step 8: Validate Blockchain
    print("Blockchain valid:", blockchain.is_chain_valid())

    # Step 9: Print Blockchain Details
    print("\nBlockchain Contents:")
    for block in blockchain.chain:
        print(f"Block {block.index} | Timestamp: {block.timestamp} | Validator: {block.validator_name}")
        print(f"  Patient Data: {block.patient_data}")
        print(f"  Prediction: {block.prediction}")
        print(f"  Hash: {block.hash}")
        print("-" * 60)

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
