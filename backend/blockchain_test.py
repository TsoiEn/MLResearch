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

    # Step 3: Simulate patient data and predictions
    patient_data_1 = {"name": "John Doe", "age": 45, "symptoms": ["fever", "cough"]}
    prediction_1 = "Flu"

    patient_data_2 = {"name": "Jane Smith", "age": 30, "symptoms": ["shortness of breath", "fatigue"]}
    prediction_2 = "Asthma"

    # Step 4: Add blocks with patient data and predictions
    print("Adding blocks to the PoA Blockchain...")
    blockchain.add_block(patient_data=patient_data_1, prediction=prediction_1, validator=validator_1)
    blockchain.add_block(patient_data=patient_data_2, prediction=prediction_2, validator=validator_2)

    # Step 5: Validate the blockchain
    print("Validating the blockchain...")
    is_valid = blockchain.is_chain_valid()
    print(f"Is blockchain valid? {is_valid}")

    # Step 6: Print the blockchain
    print("\nBlockchain contents:")
    for block in blockchain.chain:
        print(f"Block {block.index}:")
        print(f"  Timestamp: {block.timestamp}")
        print(f"  Patient Data: {block.patient_data}")
        print(f"  Prediction: {block.prediction}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Current Hash: {block.hash}")
        print(f"  Validator: {block.validator_name}")
        print(f"  Signature: {'Present' if block.signature else 'None'}")
        print("-" * 60)

if __name__ == "__main__":
    main()