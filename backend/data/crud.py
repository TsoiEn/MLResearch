from config import db_cred

# Create
def insert_data():
    db = db_cred()
    cursor = db.cursor()
    sql = """
    INSERT INTO disease_data (
        Disease, Gender, Fever, Cough, Fatigue, Difficulty_Breathing, Age, Blood_Pressure, Cholesterol_Level, Outcome_Variable, Predicted_Outcome
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = ('Influenza', 'Female', 'Yes', 'No', 'Yes', 'Yes', 19, 'Low', 'Normal', 'Positive', None)
    cursor.execute(sql, values)
    db.commit()
    print(f"Inserted ID: {cursor.lastrowid}")
    cursor.close()
    db.close()

# Read
def fetch_data():
    db = db_cred()
    cursor = db.cursor()
    sql = "SELECT * FROM disease_data;"
    cursor.execute(sql)
    records = cursor.fetchall()
    for record in records:
        print(record)
    cursor.close()
    db.close()

# Update
def update_data():
    db = db_cred()
    cursor = db.cursor()
    sql = "UPDATE disease_data SET Predicted_Outcome = %s WHERE id = %s;"
    values = ('Positive', 1)
    cursor.execute(sql, values)
    db.commit()
    print(f"Updated rows: {cursor.rowcount}")
    cursor.close()
    db.close()

# Delete
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
    insert_data()
    fetch_data()
    update_data()
    delete_data()
