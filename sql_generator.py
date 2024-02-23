from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent/".env")

client = OpenAI()
model_name = "gpt-3.5-turbo-1106"
model_name = "gpt-4-1106-preview"

def call_openai(system_message, user_message, max_tokens=300):
    messages = [{'role': 'system', 'content': system_message}, {'role': 'user', 'content': user_message}]
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=int(max_tokens)
    )
    return response.choices[0].message.content

def create_system_message(table_info):
    return f"""
You are a SQL generator. Show below is a table(s) with its columns and their respective data types:
{table_info}
Using the provided information about the table, the user will ask you to complete a SQL query. the output formation should be:
```sql
<sql text>
```
Provied a commented line in the sql query explaining the purpose.
"""

def create_user_message():
    # this will depend on the user input
    user = input("What is your query? or skip")
    if len(user) == 0:
        user = "Generate a random sql query."
    return user + '\nThe table names are case sensitive. Surround the table names in quotes " " and use aliases if required'

def extract_sql_query(text):
    query = text.split("```sql")[-1].split("```")[0]
    return query
