from dotenv import load_dotenv
import os
from pathlib import Path
import psycopg2

load_dotenv(dotenv_path=Path(__file__).parent/".env")

username = os.getenv('PG_USERNAME')
password = os.getenv('PG_PASSWORD')

database_name = 'salesdata'
table_name = 'customer'

def connect_to_postgres():
    connection = psycopg2.connect(
        user=username,
        password=password,
        host='localhost',
        port='5432',
        database=database_name
    )
    cursor = connection.cursor()
    return connection, cursor

def get_table_info(table_name):
    connection, cursor = connect_to_postgres()
    table_query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
    cursor.execute(table_query)
    # Fetch all the results
    columns_info = cursor.fetchall()
    # Print the column names and data types
    db_table = f"Table Name: {table_name}\nColumn Name | Data Type\n"
    for column_info in columns_info:
        db_table += f"{column_info[0]} | {column_info[1]}\n"
        # print(f"Column Name: {column_info[0]}, Data Type: {column_info[1]}")
    print(db_table)
    # Close the cursor and connection
    cursor.close()
    connection.close()

    return db_table

def get_multi_table_info(tables: list):
    my_tables = ""
    for table in tables:
        my_tables += get_table_info(table_name=table)
    
    return my_tables

def execute_query(query):
    connection, cursor = connect_to_postgres()
    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        print(result)
    # Close the cursor and connection
    cursor.close()
    connection.close()

if __name__=='__main__':
    get_multi_table_info(tables=['customer', 'transactions_FACT'])