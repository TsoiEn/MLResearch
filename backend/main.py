from utils import read_csv, write_csv
from encryption.homomorphic import encrypt_data
from blockchain.blockchain import Blockchain
from ml_model.ml_pipeline import predict_on_encrypted_data

def main():
    # Step 1: Load dataset
    data = read_csv("data/dataset.csv")

    # Step 2: Encrypt data
    encrypted_data = encrypt_data(data)
    write_csv("data/encrypted_data.csv", encrypted_data)

    # Step 3: Initialize blockchain
    blockchain = Blockchain()
    blockchain.add_transaction(encrypted_data)

    # Step 4: Apply ML model
    predictions = predict_on_encrypted_data(encrypted_data)
    write_csv("data/results.csv", predictions)

    print("Process completed successfully!")

if __name__ == "__main__":
    main()
