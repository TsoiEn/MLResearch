from data_config import db_cred
from phe import paillier
import base64
from mappings import GENDER_MAP, FEVER_MAP, BLOOD_PRESSURE_MAP, COUGH_MAP, FATIGUE_MAP, DIFFICULTY_BREATHING_MAP, CHOLESTEROL_LEVEL_MAP


# Initialize Paillier encryption keys
public_key, private_key = paillier.generate_paillier_keypair()


# Encrypt function for individual columns
def encrypt_data(value):
    # If the value is a string, convert it to a numeric representation (e.g., using its UTF-8 bytes)
    if isinstance(value, str):
        # Convert string to a number (e.g., sum of ASCII values or hash)
        value = sum(ord(c) for c in value)  # You can choose a different method if needed
    
    encrypted_value = public_key.encrypt(value)
    encrypted_bytes = encrypted_value.ciphertext().to_bytes((encrypted_value.ciphertext().bit_length() + 7) // 8, byteorder='big')
    return base64.b64encode(encrypted_bytes).decode('utf-8')


# Decrypt function for individual columns
def decrypt_data(encrypted_value):
    if not isinstance(encrypted_value, str) or not is_base64(encrypted_value):
        return encrypted_value  # Return the original value if it's not encrypted
    
    try:
        encrypted_bytes = base64.b64decode(encrypted_value)
        decrypted_value = private_key.decrypt(encrypted_bytes)
        return decrypted_value
    except Exception as e:
        print(f"Decryption error: {e}")
        return encrypted_value  # Return the original value if decryption fails


def is_base64(s):
    try:
        # Check if it is a valid Base64-encoded string
        return base64.b64encode(base64.b64decode(s)).decode('utf-8') == s
    except Exception:
        return False


# Insert data with encryption
def insert_data():
    db = db_cred()
    cursor = db.cursor()

    # Encrypt only the specified columns, leave others in plain form
    encrypted_values = (
        'Influenza',  # Disease is not encrypted
        encrypt_data(GENDER_MAP.get('Female', 0)),  # Encrypt Gender
        encrypt_data(FEVER_MAP.get('Yes', 0)),     # Encrypt Fever
        encrypt_data(COUGH_MAP.get('No', 0)),      # Encrypt Cough
        encrypt_data(FATIGUE_MAP.get('Yes', 0)),   # Encrypt Fatigue
        encrypt_data(DIFFICULTY_BREATHING_MAP.get('Yes', 0)), # Encrypt Difficulty_Breathing
        encrypt_data(19),  # Encrypting the Age
        encrypt_data(BLOOD_PRESSURE_MAP.get('Low', 0)), # Encrypt Blood Pressure
        encrypt_data(CHOLESTEROL_LEVEL_MAP.get('Normal', 0)), # Encrypt Cholesterol Level
        'Positive',  # Outcome_Variable is not encrypted
        None  # Assuming Predicted_Outcome is handled separately (if necessary)
    )

    sql = """
    INSERT INTO disease_data (
        Disease, Gender, Fever, Cough, Fatigue, Difficulty_Breathing, Age, Blood_Pressure, Cholesterol_Level, Outcome_Variable, Predicted_Outcome
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(sql, encrypted_values)
    db.commit()
    print(f"Inserted ID: {cursor.lastrowid}")
    cursor.close()
    db.close()


# Read and decrypt data
def fetch_data():
    db = db_cred()
    cursor = db.cursor()
    sql = "SELECT * FROM disease_data;"
    cursor.execute(sql)
    records = cursor.fetchall()
    for record in records:
        print(record)  # Print the raw data for debugging
        decrypted_record = [
            decrypt_data(record[i]) if isinstance(record[i], str) else record[i]
            for i in range(len(record))
        ]
        print(decrypted_record)
    cursor.close()
    db.close()


# Update data with encryption
def update_data():
    db = db_cred()
    cursor = db.cursor()

    # Encrypt the Predicted_Outcome before updating
    encrypted_outcome = encrypt_data('Positive')
    sql = "UPDATE disease_data SET Predicted_Outcome = %s WHERE id = %s;"
    values = (encrypted_outcome, 1)
    cursor.execute(sql, values)
    db.commit()
    print(f"Updated rows: {cursor.rowcount}")
    cursor.close()
    db.close()


# Delete data by ID
def delete_data():
    db = db_cred()
    cursor = db.cursor()
    sql = "DELETE FROM disease_data WHERE id = %s;"
    value = (2,)
    cursor.execute(sql, value)
    db.commit()
    print(f"Deleted rows: {cursor.rowcount}")
    cursor.close()
    db.close()


# Call CRUD functions
if __name__ == "__main__":
    # Example function calls
    insert_data()  # Insert new data into the database
    fetch_data()   # Fetch and decrypt data
    update_data()  # Update data in the database
    delete_data()  # Delete a record from the database
