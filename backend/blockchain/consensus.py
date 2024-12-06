import hashlib
from time import time
from blockchain.blockchain import Block


class Validator:
    """Represents a validator in the PoA blockchain."""
    def __init__(self, name):
        self.name = name

    def sign_block(self, block):
        """Sign a block with the validator's name."""
        block.sign_block(self.name)


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

    def add_block(self, data, validator):
        """Add a new block to the chain."""
        if validator not in self.validators:
            raise ValueError("Validator is not authorized to add a block!")

        # Create the block
        new_block = Block(
            index=len(self.chain),
            timestamp=time(),
            data=data,
            previous_hash=self.get_latest_block().hash,
            validator=validator
        )
        new_block.sign_block(validator.name)

        # Validate the block
        if not self.is_block_valid(new_block):
            raise ValueError("Block signature is invalid!")

        # Append to chain
        self.chain.append(new_block)

    def is_block_valid(self, block):
        """Check if a block's signature is valid."""
        expected_signature = hashlib.sha256(f"{block.validator.name}{block.index}{block.timestamp}".encode()).hexdigest()
        return block.signature == expected_signature

    def is_chain_valid(self):
        """Validate the entire blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check the previous hash
            if current_block.previous_hash != previous_block.hash:
                return False

            # Validate the block
            if not self.is_block_valid(current_block):
                return False

        return True
