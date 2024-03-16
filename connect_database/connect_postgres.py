from dotenv import load_dotenv
import os
from pathlib import Path
import psycopg2
import time

class PostgreSQLConnector:
    def __init__(self, database_name='salesdata'):
        self.load_environment()
        self.username = os.getenv('POSTGRES_USERNAME')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.postgres_port = os.environ.get('POSTGRES_PORT', '5432')
        # self.postgres_host = os.environ.get('POSTGRES_HOST', 'host.docker.internal')
        self.database_name = database_name

    def load_environment(self):
        load_dotenv(dotenv_path=Path(__file__).parent/".env")

    def connect_to_postgres(self):
        # Forming the connection string
        connection_string = f"host=host.docker.internal port={self.postgres_port} dbname={self.database_name} user={self.username} password={self.password}"
        connection = psycopg2.connect(connection_string)
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

    def get_all_tables(self):
        connection, cursor = self.connect_to_postgres()
        db_query = '''SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        '''
        cursor.execute(db_query)
        table_names = cursor.fetchall()

        tables = []
        for table in table_names:
            tables.append(table[0])

        cursor.close()
        connection.close()
        return tables
        

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
    # connector.connect_to_postgres()
    # connector.get_all_tables()
    connector.get_multi_table_info(tables=connector.get_all_tables())
