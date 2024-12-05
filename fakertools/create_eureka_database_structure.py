import pyodbc
import os
import sys

def execute_sql_file(sql_file):
    """
    Executes a SQL script file against an MS SQL Server database using a connection string from an environment variable.

    Args:
        sql_file (str): Path to the SQL file.
    """
    # Read connection string from environment variable
    connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=insights-engine.database.windows.net,1433;Database=eureka;Uid=insights-admin;Pwd=d£xXe96n2o+_;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    if not connection_string:
        raise EnvironmentError("Environment variable 'SqlConnectionString' is not set.")

    try:
        # Connect to the database
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Read the SQL file
        with open(sql_file, 'r') as file:
            sql_script = file.read()

        # Split and execute each SQL statement
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
                print(f"Executed statement: {statement[:50]}...")

        # Commit changes
        connection.commit()
        print("SQL script executed successfully.")

    except pyodbc.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"SQL file not found: {sql_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) != 2:
        print("Usage: python create_eureka_database_structure.py <sql_file>")
        sys.exit(1)

    sql_file = sys.argv[1]
    try:
        execute_sql_file(sql_file)
    except EnvironmentError as env_err:
        print(env_err)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
