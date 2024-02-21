from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent/".env")

client = OpenAI()
model_name = "gpt-3.5-turbo-1106"

def call_openai(system_message, user_message, max_tokens=100):
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
"""

def create_user_message():
    # this will depend on the user input
    return """
Generate a random sql query.
"""