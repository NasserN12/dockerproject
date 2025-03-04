import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='db-container',
        user='root',
        password='password',
        database='dockerproject1'
    )