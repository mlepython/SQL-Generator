import database_connect
import sql_generator
from connect_database.connect_postgres import PostgreSQLConnector


connect = PostgreSQLConnector(database_name='dvdrental')
# table_name = 'items_purchased_FACT'
# db_table = database_connect.get_table_info(table_name=table_name)

db_table = connect.get_multi_table_info(tables=connect.get_all_tables())

system = sql_generator.create_system_message(table_info=db_table)
user = sql_generator.create_user_message()

result = sql_generator.call_openai(system_message=system, user_message=user)
print(result)

query = sql_generator.extract_sql_query(result)
connect.execute_query(query)