import pyodbc
import pandas as pd

# Database connection details
server = 'insights-engine.database.windows.net'  # Azure SQL Server name
database = 'CustomerDataStore'  # Database name
username = 'insights-admin'       # Username
password = 'd£xXe96n2o+_'       # Password
driver = '{ODBC Driver 17 for SQL Server}'  # ODBC Driver

# CSV file path
csv_file_path = '/Users/ananthagutta/web-apps/eureka-backend-functions/fakertools/customer_profiles.csv'

# Table name
table_name = 'Customers'

# Create a connection to the database
def create_connection():
    connection_string = f"""
    DRIVER={driver};
    SERVER={server};
    PORT=1433;
    DATABASE={database};
    UID={username};
    PWD={password};
    """
    try:
        conn = pyodbc.connect(connection_string)
        print("Database connection successful.")
        return conn
    except pyodbc.Error as e:
        print("Error connecting to database:", e)
        exit(1)

# Load CSV into the database
def load_csv_to_database(conn, csv_file_path, table_name):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)

        # Insert data row by row
        cursor = conn.cursor()
        for index, row in df.iterrows():
            cursor.execute(f"""
                INSERT INTO {table_name} (first_name, last_name, email, phone_number, address, city, state, zip_code, company, job_title, dob)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            row['first_name'], row['last_name'], row['email'], row['phone_number'], 
            row['address'], row['city'], row['state'], row['zip_code'], 
            row['company'], row['job_title'], row['dob'])
        
        # Commit the transaction
        conn.commit()
        print("Data successfully loaded into the database.")

    except Exception as e:
        print("Error loading data:", e)
        conn.rollback()  # Rollback in case of error

# Main function
def main():
    # Create a database connection
    conn = create_connection()

    # Load the CSV data into the database
    load_csv_to_database(conn, csv_file_path, table_name)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()
