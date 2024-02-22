# SQL Query Generation and Execution Framework

## Overview

This framework is designed to provide an automated way to generate SQL queries using a language model and then execute those queries against a PostgreSQL database. The codebase consists of three main components:

1. `app.py` is the main application driver that orchestrates interactions between the user, the AI model, and the database.
2. `database_connect.py` handles the database connection, schema retrieval, and SQL execution.
3. `sql_generator.py` interfaces with OpenAI's language model to generate SQL queries based on the provided schema and user input.

The application allows for retrieving information about database table structures, submitting a query request to an AI, and executing the resultant SQL command on a database.

## Dependencies

The following dependencies are required to run this code:

- Python 3.x
- `psycopg2` - PostgreSQL adapter for Python
- `openai` - Official OpenAI Python client library
- `python-dotenv` - Reads key-value pairs from a .env file and sets them as environment variables

Ensure you have `pip` installed to handle these dependencies. It is also recommended to use a virtual environment.

## Usage

### Setting Up Environment Variables
Before running the system, create a `.env