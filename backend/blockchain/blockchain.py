import hashlib
import json
import logging
from time import time

logging.basicConfig(level=logging.INFO)



class Block:
    def __init__(self, index, timestamp, patient_data, prediction, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.patient_data = patient_data
        self.prediction = prediction
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.signature = None
        self.validator_name = None
        self.validator_public_key = None

    def calculate_hash(self):
        """Calculate the hash of the block."""
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "patient_data": self.patient_data,
            "prediction": self.prediction,
            "previous_hash": self.previous_hash,
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    def sign_block(self, validator_name):
        """Sign the block with the validator's name."""
        self.signature = hashlib.sha256(f"{validator_name}{self.index}{self.timestamp}".encode()).hexdigest()



class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        try:
            # Validate block
            if new_block.previous_hash != self.get_latest_block().hash:
                raise ValueError("Previous hash does not match!")
            if new_block.hash != new_block.calculate_hash():
                raise ValueError("Block hash is invalid!")
            # Append block
            self.chain.append(new_block)
            logging.info(f"Block {new_block.index} added to the chain.")
        except Exception as e:
            logging.error(f"Error adding block: {e}")
            raise

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                logging.error(f"Block {current_block.index} hash is invalid.")
                return False
            if current_block.previous_hash != previous_block.hash:
                logging.error(f"Block {current_block.index} previous hash does not match.")
                return False
        logging.info("Blockchain is valid.")
        return True

    def add_transaction(self, patient_data, prediction, validator):
        new_block = Block(len(self.chain), time(), patient_data, prediction, self.get_latest_block().hash, validator)
        self.add_block(new_block)

