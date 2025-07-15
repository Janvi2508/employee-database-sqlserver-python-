import pyodbc
import pandas as pd

# Remote SQL Server configuration (Azure-hosted)
server_ip = '20.192.43.161'  
server = 'companydbserver.database.windows.net' 
database = 'CompanyDB'
username = 'Janvi_sharma'
password = 'Mukul@2530'
driver = '{ODBC Driver 17 for SQL Server}'

def connect_to_sql_server():
    try:
        connection_string = (
            f'DRIVER={driver};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        conn = pyodbc.connect(connection_string)
        print(f" Connection successful. Connected to SQL Server at IP: {server_ip}")

        # Query first 5 employees
        query = "SELECT TOP 5 * FROM Employees"
        df = pd.read_sql(query, conn)
        print("\n👨‍💼 First 5 Employees:")
        print(df)

    except Exception as e:
        print(" Connection failed:")
        print(e)

    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    connect_to_sql_server()
