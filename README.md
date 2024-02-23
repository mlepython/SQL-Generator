# SQL Generation and Execution Helper

## Overview

This collection of Python scripts is designed to assist developers and data analysts in generating SQL queries and executing them on a PostgreSQL database. Utilizing the OpenAI API and a connection to a PostgreSQL database, this codebase automates the process of SQL query creation and execution, streamlining data retrieval and analysis.

The system works by obtaining relevant database schema information using `database_connect.py`, generating SQL queries with the aid of GPT-powered AI provided by `sql_generator.py`, and finally executing the generated SQL queries on the PostgreSQL database.

## Dependencies and Prerequisites

Make sure the following dependencies are installed and the setup is complete before running the code:

- Python 3.x
- `psycopg2` library to connect to the PostgreSQL database.
- `openai` SDK to interact with the OpenAI API and access GPT models.
- Access to a running PostgreSQL server and valid credentials (configured in the `.env` file).
- An OpenAI API key for using GPT-powered models (configured in the `.env` file).

The `.env` file should be located within the same directory as the scripts and contain the following environment variables:

```shell
PG_USERNAME=<your_postgresql_username>
PG_PASSWORD=<your_postgresql_password>
OPENAI_API_KEY=<your_openai_api_key>
```

## Usage

### Database Operations

Use `database_connect.py`