from phe import paillier
import pandas as pd

# Generate a public/private keypair
public_key, private_key = paillier.generate_paillier_keypair()

def encrypt_data(data):
    """
    Encrypt a Pandas DataFrame or Series using Paillier encryption.
    :param data: DataFrame or Series to encrypt.
    :return: Encrypted DataFrame with same structure.
    """
    encrypted_data = data.applymap(lambda x: public_key.encrypt(x) if isinstance(x, (int, float)) else x)
    return encrypted_data

def decrypt_data(encrypted_data):
    """
    Decrypt a Pandas DataFrame or Series using Paillier encryption.
    :param encrypted_data: Encrypted DataFrame or Series.
    :return: Decrypted DataFrame with same structure.
    """
    decrypted_data = encrypted_data.applymap(lambda x: private_key.decrypt(x) if isinstance(x, paillier.EncryptedNumber) else x)
    return decrypted_data

def process_encrypted_data(encrypted_data):
    """
    Example: Process data while still encrypted (e.g., summation of numeric columns).
    :param encrypted_data: Encrypted DataFrame.
    :return: Decrypted results of computation.
    """
    encrypted_sum = encrypted_data.sum(numeric_only=True).apply(private_key.decrypt)
    return encrypted_sum

# Test the encryption and decryption using a sample DataFrame
if __name__ == "__main__":
    sample_data = pd.DataFrame({
        "Age": [25, 30, 35],
        "Cholesterol Level": [200, 180, 220],
        "Disease": ["Flu", "Cold", "Asthma"]
    })
    print("Original Data:\n", sample_data)

    encrypted_data = encrypt_data(sample_data)
    print("\nEncrypted Data:\n", encrypted_data)

    decrypted_data = decrypt_data(encrypted_data)
    print("\nDecrypted Data:\n", decrypted_data)

    encrypted_sum = process_encrypted_data(encrypted_data)
    print("\nSum of Encrypted Data:\n", encrypted_sum)
