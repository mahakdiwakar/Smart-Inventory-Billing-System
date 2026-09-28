#Database Connection Settings
import psycopg2


def connection():
    con = psycopg2.connect(
        host="localhost",
        database="ecommerce",
        user="postgres",
        password="123456",
        port="5432"
    )

    if con:
        print("Connention successful")
    else:
        print("Connection failed")
    return con
conn = connection()