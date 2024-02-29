from dotenv import load_dotenv
import os
from pathlib import Path
import psycopg2

class PostgreSQLConnector:
    def __init__(self, database_name='salesdata'):
        self.load_environment()
        self.username = os.getenv('PG_USERNAME')
        self.password = os.getenv('PG_PASSWORD')
        self.database_name = database_name

    def load_environment(self):
        load_dotenv(dotenv_path=Path(__file__).parent/".env")

    def connect_to_postgres(self):
        connection = psycopg2.connect(
            user=self.username,
            password=self.password,
            host='localhost',
            port='5432',
            database=self.database_name
        )
        cursor = connection.cursor()
        return connection, cursor

    def get_table_info(self, table_name):
        connection, cursor = self.connect_to_postgres()
        table_query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
        cursor.execute(table_query)
        columns_info = cursor.fetchall()

        db_table = f"Table Name: {table_name}\nColumn Name | Data Type\n"
        for column_info in columns_info:
            db_table += f"{column_info[0]} | {column_info[1]}\n"

        print(db_table)
        cursor.close()
        connection.close()

        return db_table

    def get_multi_table_info(self, tables):
        my_tables = ""
        for table in tables:
            my_tables += self.get_table_info(table_name=table)
        
        return my_tables

    def execute_query(self, query):
        connection, cursor = self.connect_to_postgres()
        try:
            cursor.execute(query)
            results = cursor.fetchone()
            print("Results of Query:\n", results)
        except psycopg2.Error as e:
            print("Error executing query:", e)
            results = None
        finally:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    connector = PostgreSQLConnector()
    connector.get_multi_table_info(tables=['customer', 'transactions_FACT'])
