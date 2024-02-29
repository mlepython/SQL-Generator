import json
import os
os.add_dll_directory(r"C:\Program Files\IBM\clidriver\bin")
import ibm_db
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import yaml


class IBMdb2Connector:
    def __init__(self, ibm_credentials=None):
        self.load_environment()
        if ibm_credentials:
            self.load_credentials(ibm_credentials)
        else:
            self.load_config()

    def load_environment(self):
        load_dotenv(dotenv_path=Path(__file__).parent/".env")
        self.username = os.getenv('IBM_USERNAME')
        self.password = os.getenv('IBM_PASSWORD')

    def load_config(self):
        print("Loading configuration")
        config_file_path = Path(__file__).parent/'ibm_config.yaml'

        with open(config_file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)

        self.dsn_driver = config["dsn_driver"]
        self.dsn_database = config["dsn_database"]
        self.dsn_hostname = config["dsn_hostname"]
        self.dsn_port = config["dsn_port"]
        self.dsn_protocol = config["dsn_protocol"]
        self.dsn_security = config["dsn_security"]

    def load_credentials(self, ibm_credentials):
        print('Loading Credentials')
        with open(ibm_credentials, 'r') as json_file:
            credentials = json.load(json_file)

        self.dsn_driver = "{IBM DB2 ODBC DRIVER}"
        self.dsn_database = credentials['connection']['db2']['database']
        self.dsn_hostname = credentials['connection']['db2']['hosts'][0]['hostname']
        self.dsn_port = credentials['connection']['db2']['hosts'][0]['port']
        self.dsn_protocol = "TCPIP"
        self.username = credentials['connection']['db2']['authentication']['username']
        self.password = credentials['connection']['db2']['authentication']['password']
        self.dsn_security = "SSL"

    def connect_db(self):

        dsn = (
            "DRIVER={0};"
            "DATABASE={1};"
            "HOSTNAME={2};"
            "PORT={3};"
            "PROTOCOL={4};"
            "UID={5};"
            "PWD={6};"
            "SECURITY={7};").format(self.dsn_driver, self.dsn_database, self.dsn_hostname,
                                    self.dsn_port, self.dsn_protocol, 
                                    self.username, self.password, self.dsn_security)

        # dsn = f"DRIVER={dsn_driver};DATABASE={dsn_database};HOSTNAME={dsn_hostname};PORT={dsn_port};PROTCOL={dsn_protocol};UID={dsn_uid};PWD={dsn_pwd};SECURITY={dsn_security};"
        try:
            self.conn = ibm_db.connect(dsn, "", "")
            print("Connected to database: ", self.dsn_database, "as user: ", self.username, "on host: ", self.dsn_hostname)
            

        except:
            print("Unable to connect: ", ibm_db.conn_errormsg())

    def execute_db_query(self, query):
        try:
            stmt = ibm_db.exec_immediate(self.conn, query)
            result = ibm_db.fetch_assoc(stmt)
            
            while result:
                print(result)
                result = ibm_db.fetch_assoc(stmt)
                
            ibm_db.free_stmt(stmt)
            
        except Exception as e:
            print("Error executing query:", e)

        finally:
            pass
            # No need to close the connection here; it can be closed in the calling code

if __name__ == '__main__':
    ibm_credentials = Path(__file__).parent/'ibm_credentials.json'
    ibm = IBMdb2Connector()
    ibm.connect_db()
    # with open(ibm_credentials, 'r') as json_file:
    #     credentials = json.load(json_file)

    # conn = connect_db(credentials)

    query = "SELECT * FROM FACTSALES LIMIT 10;"
    ibm.execute_db_query(query)

    # ibm_db.close(conn)
