import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')))
from datetime import datetime
import hashlib
import json
import logging
from time import time
from data_config import db_cred  # Import the database credential function

logging.basicConfig(level=logging.INFO)


def unix_to_datetime(unix_time):
    """Convert a UNIX timestamp to MySQL DATETIME format."""
    return datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')


class Block:
    def __init__(self, index, timestamp, data, previous_hash, current_hash=None, validator_name=None, signature=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = current_hash if current_hash else self.calculate_hash()
        self.validator_name = validator_name
        self.signature = signature

    def calculate_hash(self):
        """Calculate the hash of the block."""
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def sign_block(self, validator_name):
        """Sign the block with the validator's name."""
        self.validator_name = validator_name
        self.signature = hashlib.sha256(f"{validator_name}{self.index}{self.timestamp}".encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = self.load_chain_from_db()

    def connect_db(self):
        """Establish a connection to the database using db_cred."""
        connection = db_cred()
        if not connection:
            raise ConnectionError("Failed to connect to the database.")
        return connection

    def create_genesis_block(self):
        """Create the genesis block."""
        genesis_block = Block(0, time(), "Genesis Block", "0")
        self.save_block_to_db(genesis_block)
        return genesis_block

    def load_chain_from_db(self):
        """Load the blockchain from the database."""
        connection = self.connect_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blockchain ORDER BY block_id ASC")
        rows = cursor.fetchall()
        connection.close()

        if not rows:
            # If the chain is empty, create the genesis block
            return [self.create_genesis_block()]

        # Recreate the blockchain from the database
        chain = []
        for row in rows:
            block = Block(
                index=row["block_id"],
                timestamp=row["timestamp"],
                data=row["data"],
                previous_hash=row["previous_hash"],
                current_hash=row["current_hash"],
                validator_name=row.get("validator_name"),
                signature=row.get("signature"),
            )
            chain.append(block)
        return chain

    def save_block_to_db(self, block):
        """Save a block to the database."""
        connection = self.connect_db()
        cursor = connection.cursor()

        # Convert UNIX timestamp to MySQL DATETIME format
        timestamp_datetime = unix_to_datetime(block.timestamp)

        insert_query = """
        INSERT INTO blockchain (timestamp, data, previous_hash, current_hash, validator_name, signature)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            timestamp_datetime,  # Convert the timestamp
            block.data,
            block.previous_hash,
            block.hash,
            block.validator_name,
            block.signature,
        ))
        connection.commit()
        connection.close()

    def get_latest_block(self):
        """Get the latest block in the chain."""
        return self.chain[-1]

    def add_block(self, data, validator_name):
        """Add a new block to the chain."""
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time(),
            data=data,
            previous_hash=previous_block.hash,
        )
        new_block.sign_block(validator_name)

        # Validate and save the block
        if new_block.previous_hash != previous_block.hash:
            raise ValueError("Previous hash does not match!")
        if new_block.hash != new_block.calculate_hash():
            raise ValueError("Block hash is invalid!")

        self.chain.append(new_block)
        self.save_block_to_db(new_block)
        logging.info(f"Block {new_block.index} added to the chain.")

    def is_chain_valid(self):
        """Validate the blockchain."""
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


# Example usage:
if __name__ == "__main__":
    blockchain = Blockchain()

    # Add new blocks
    blockchain.add_block("Patient record added", "Validator_A")
    blockchain.add_block("Another patient record added", "Validator_B")

    # Check blockchain validity
    if blockchain.is_chain_valid():
        logging.info("Blockchain is consistent and valid.")
