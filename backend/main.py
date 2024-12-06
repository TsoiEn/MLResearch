from blockchain import PoABlockchain, Validator
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    # Step 1: Create validators
    validator_1 = Validator("Validator_1")
    validator_2 = Validator("Validator_2")
    validators = [validator_1, validator_2]

    # Step 2: Initialize the PoA blockchain
    blockchain = PoABlockchain(validators)

    # Step 3: Add blocks
    print("Adding blocks to the PoA Blockchain...")
    blockchain.add_block(data="First block data", validator=validator_1)
    blockchain.add_block(data="Second block data", validator=validator_2)

    # Step 4: Validate the chain
    print("Is blockchain valid?", blockchain.is_chain_valid())

    # Step 5: Print the blockchain
    for block in blockchain.chain:
        print(f"Block {block.index} | Data: {block.data} | Validator: {block.validator.name if block.validator else 'None'} | Signature: {block.signature}")

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
