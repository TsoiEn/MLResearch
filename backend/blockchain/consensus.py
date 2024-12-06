import hashlib
from time import time
from blockchain.blockchain import Block
# import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as _Padding


class Validator:
    """Represents a validator in the PoA blockchain."""
    def __init__(self, name):
        self.name = name
        # Generate RSA key pair
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def sign_block(self, block):
        """Sign a block with the validator's private key."""
        if not self.private_key:
            raise ValueError(f"Validator {self.name} does not have a private key for signing.")
        
        signature = self.private_key.sign(
            block.hash.encode(),
            _Padding.PSS(
                mgf=_Padding.MGF1(hashes.SHA256()),
                salt_length=_Padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        block.signature = signature
        block.validator_name = self.name
        block.validator_public_key = self.public_key

    def validate_block(self, block):
        """Verify if the block was signed by this validator."""
        if block.validator_name != self.name:
            return False
        if block.signature is None or block.validator_public_key is None:
            return False
        try:
            block.validator_public_key.verify(
                block.signature,
                block.hash.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False


class PoABlockchain:
    """Implements a PoA blockchain."""
    def __init__(self, validators):
        self.chain = [self.create_genesis_block()]
        self.validators = validators  # List of authorized Validator objects

    def create_genesis_block(self):
        """Create the genesis block."""
        genesis_block = Block(0, time(), "Genesis Block", "0", None)
        genesis_block.signature = "GENESIS_BLOCK"
        return genesis_block

    def get_latest_block(self):
        """Retrieve the latest block on the chain."""
        return self.chain[-1]

    def add_block(self, patient_data, prediction,validator):
        """Add a new block to the chain."""
        if validator not in self.validators:
            raise ValueError("{validator.name} is not a recognized validator.")

        latest_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time(),
            patient_data=patient_data,
            prediction=prediction,
            previous_hash=latest_block.hash
        )
        validator.sign_block(new_block)  # Validator signs the new block
        self.chain.append(new_block)

    def is_block_valid(self, block):
        """Check if a block's signature is valid."""
        expected_signature = hashlib.sha256(f"{block.validator.name}{block.index}{block.timestamp}".encode()).hexdigest()
        return block.signature == expected_signature

    def is_chain_valid(self):
        """Validate the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check current block's hash
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} hash mismatch.")
                return False

            # Check previous hash linkage
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} previous hash mismatch.")
                return False

            # Validate the block's signature
            validator_name = current_block.validator_name
            validator = next((v for v in self.validators if v.name == validator_name), None)
            if validator and not validator.validate_block(current_block):
                print(f"Block {current_block.index} failed signature validation.")
                return False

        return True
