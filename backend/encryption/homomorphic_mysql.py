import mysql.connector
from phe import paillier
import base64

#! QUOTIONS WAG IRUN ULIT Masisira, TAMA NA YUNG ISANG RUN"

# Initialize Paillier encryption keys
public_key, private_key = paillier.generate_paillier_keypair()

# Function to encrypt a value using Paillier encryption
def encrypt_value(value):
    # Ensure the value is numeric before encrypting
    try:
        # If the value is not a number, convert it to an integer
        numeric_value = float(value)
    except ValueError:
        raise ValueError(f"Cannot encrypt non-numeric value: {value}")
    
    encrypted_value = public_key.encrypt(numeric_value).ciphertext()
    encrypted_bytes = encrypted_value.to_bytes((encrypted_value.bit_length() + 7) // 8, byteorder='big')
    return base64.b64encode(encrypted_bytes).decode('utf-8')

# Function to connect to the MySQL database
def db_cred():
    return mysql.connector.connect(
        host="localhost",
        user="md",
        password="(hC2T5Hm",
        database="patient_record"
    )

# Update categorical columns with mapped values directly in MySQL
def preprocess_and_encrypt_data():
    db = db_cred()
    cursor = db.cursor()

    # Debugging: Check data before any updates
    cursor.execute("""
    SELECT id, Gender, Fever, Cough, Fatigue, Difficulty_Breathing, Age, Blood_Pressure, Cholesterol_Level
    FROM disease_data LIMIT 10;
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Before Update - ID: {row[0]}, Gender: {row[1]}, Fever: {row[2]}, Cough: {row[3]}, Fatigue: {row[4]}, Difficulty_Breathing: {row[5]}, Age: {row[6]}, Blood_Pressure: {row[7]}, Cholesterol_Level: {row[8]}")

    # Update categorical values to integers directly in MySQL
    cursor.execute("""
    UPDATE disease_data
    SET
        Gender = CASE WHEN Gender = 'Male' THEN 1 WHEN Gender = 'Female' THEN 2 ELSE 0 END,
        Fever = CASE WHEN Fever = 'Yes' THEN 1 WHEN Fever = 'No' THEN 0 ELSE 0 END,
        Cough = CASE WHEN Cough = 'Yes' THEN 1 WHEN Cough = 'No' THEN 0 ELSE 0 END,
        Fatigue = CASE WHEN Fatigue = 'Yes' THEN 1 WHEN Fatigue = 'No' THEN 0 ELSE 0 END,
        Difficulty_Breathing = CASE WHEN Difficulty_Breathing = 'Yes' THEN 1 WHEN Difficulty_Breathing = 'No' THEN 0 ELSE 0 END,
        Blood_Pressure = CASE WHEN Blood_Pressure = 'Low' THEN 1 WHEN Blood_Pressure = 'Normal' THEN 2 WHEN Blood_Pressure = 'High' THEN 3 ELSE 0 END,
        Cholesterol_Level = CASE WHEN Cholesterol_Level = 'Low' THEN 1 WHEN Cholesterol_Level = 'Normal' THEN 2 WHEN Cholesterol_Level = 'High' THEN 2 ELSE 0 END;
        
    """)

    db.commit()

    # Debugging: Verify data after the update
    cursor.execute("""
    SELECT id, Gender, Fever, Cough, Fatigue, Difficulty_Breathing, Age, Blood_Pressure, Cholesterol_Level
    FROM disease_data LIMIT 10;
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"After Update - ID: {row[0]}, Gender: {row[1]}, Fever: {row[2]}, Cough: {row[3]}, Fatigue: {row[4]}, Difficulty_Breathing: {row[5]}, Age: {row[6]}, Blood_Pressure: {row[7]}, Cholesterol_Level: {row[8]}")

    # Encrypt selected columns using Paillier encryption and update them
    cursor.execute("""
    SELECT id, Gender, Fever, Cough, Fatigue, Difficulty_Breathing, Age, Blood_Pressure, Cholesterol_Level
    FROM disease_data;
    """)
    rows = cursor.fetchall()
    
    for row in rows:
        row_id = row[0]
        try:
            # Encrypt the required columns
            encrypted_gender = encrypt_value(row[1]) if row[1] is not None else None
            encrypted_fever = encrypt_value(row[2]) if row[2] is not None else None
            encrypted_cough = encrypt_value(row[3]) if row[3] is not None else None
            encrypted_fatigue = encrypt_value(row[4]) if row[4] is not None else None
            encrypted_difficulty_breathing = encrypt_value(row[5]) if row[5] is not None else None
            encrypted_age = encrypt_value(row[6]) if row[6] is not None else None
            encrypted_blood_pressure = encrypt_value(row[7]) if row[7] is not None else None
            encrypted_cholesterol_level = encrypt_value(row[8]) if row[8] is not None else None

            # Update encrypted values in MySQL
            cursor.execute("""
            UPDATE disease_data
            SET
                Gender = %s,
                Fever = %s,
                Cough = %s,
                Fatigue = %s,
                Difficulty_Breathing = %s,
                Age = %s,
                Blood_Pressure = %s,
                Cholesterol_Level = %s
            WHERE id = %s;
            """, (encrypted_gender, encrypted_fever, encrypted_cough, encrypted_fatigue, 
                  encrypted_difficulty_breathing, encrypted_age, encrypted_blood_pressure, 
                  encrypted_cholesterol_level, row_id))
            print(f"Encrypted and Updated Row ID: {row_id}")
        except Exception as e:
            print(f"Error encrypting Row ID {row_id}: {e}")

    db.commit()
    cursor.close()
    db.close()



# Function to execute the entire process
def process_data():
    preprocess_and_encrypt_data()

if __name__ == "__main__":
    process_data()
