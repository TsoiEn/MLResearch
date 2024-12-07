import mysql.connector

# connection to database
def db_cred():
    return mysql.connector.connect(
        host="localhost",
        user="md",
        password="(hC2T5Hm",
        database="patient_record"
    )