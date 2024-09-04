from azure.identity import ClientSecretCredential
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os


load_dotenv()

tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]

sql_server_name = os.getenv("SQL_SERVER_NAME")
sql_database_name = os.getenv("SQL_DATABASE_NAME")
sql_admin_user = os.getenv("SQL_ADMIN_USER")


credential = ClientSecretCredential(tenant_id, client_id, client_secret)


access_token = credential.get_token("https://database.windows.net/").token

conn = f"mssql+pyodbc://{sql_admin_user}@{sql_server_name}"
conn += f".database.windows.net:1433/{sql_database_name}?"
conn += "driver=ODBC+Driver+17+for+SQL+Server"
conn += "&authentication=ActiveDirectoryAccessToken"

engine = create_engine(conn, connect_args={'autocommit': True, 'token': access_token})
try:
    with engine.connect() as connection:
        result = connection.execute("SELECT TOP 1 name FROM sys.tables;")
        for row in result:
            print(f"Successfully accessed the database: {sql_database_name}")
            print(f"First table name: {row[0]}")
except SQLAlchemyError as e:
    print(f"Failed to access the SQL Database: {sql_database_name}")
    print(f"Error: {str(e)}")
