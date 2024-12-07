"#! QUOTIONS WAG IRUN ULIT MAGDUDUPLICATE TAMA NA YUNG ISANG RUN"

import csv
from config import db_cred

# Database connection
db = db_cred()
cursor = db.cursor()

# Insert CSV into MySQL
def insert_csv_to_db(file_path):
    with open(file_path, 'r') as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Skip the header row
        for row in csv_data:
            sql = """
            INSERT INTO disease_data (
                Disease, Gender, Fever, Cough, Fatigue, Difficulty_Breathing, Age, Blood_Pressure, Cholesterol_Level, Outcome_Variable
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql, tuple(row))
        db.commit()
        print(f"Inserted {cursor.rowcount} rows.")

# Call the function
file_path = '/home/tsoien/github/MLResearch/backend/data/Disease_symptom_and_patient_profile_dataset.csv'  # Update with your file location
insert_csv_to_db(file_path)

cursor.close()
db.close()
