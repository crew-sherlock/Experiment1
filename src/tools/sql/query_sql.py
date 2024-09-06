import logging
import os
import struct
from typing import List

import pyodbc
from azure.identity.aio import DefaultAzureCredential
import pandas as pd
import aioodbc

logger = logging.getLogger("sql_helper")
logger.setLevel(logging.DEBUG)

driver_name = ''
driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
if driver_names:
    driver_name = driver_names[0]


class QuerySql:

    def __init__(self):
        self.azure_sql_token_url = "https://database.windows.net/.default"
        self.sql_copt_ss_access_token = (1256)
        self.db_name = os.getenv("AZ_SQL_DATABASE")
        self.az_sql_server = os.getenv("AZ_SQL_SERVER")

    async def execute(self,
                      query: str, params: List[str]
                      ) -> pd.DataFrame:
        async with await self._get_aioodbc_connection() as connection:

            async with connection.cursor() as cursor:
                await cursor.execute(query, params)
                columns = [column[0] for column in cursor.description]
                rows = await cursor.fetchall()

        return pd.DataFrame.from_records(rows, columns=columns)

    def _get_connection_string(self) -> str:
        connection_string: str = f"DRIVER={driver_name};"
        connection_string += (f"SERVER=tcp:{self.az_sql_server}"
                              f".database.windows.net,1433;")
        connection_string += (
            f"DATABASE={self.db_name};Encrypt=yes;TrustServerCertificate=yes;"
            f"Connection Timeout=30"
        )
        return connection_string

    async def _get_aioodbc_connection(self) -> aioodbc.Connection:
        """Asynchronous SQL Connection using aioodbc library and returned
        Create a new ODBC connection to a database.
        Returns:
            aioodbc.Connection: Asynchronous ODBC SQL Connection
        """
        credential = DefaultAzureCredential()
        try:
            token = await credential.get_token(self.azure_sql_token_url)
            token_bytes = token.token.encode("UTF-16-LE")
            token_struct = struct.pack(
                f"<I{len(token_bytes)}s", len(token_bytes), token_bytes
            )

            connection = await aioodbc.connect(
                dsn=self._get_connection_string(),
                attrs_before={self.sql_copt_ss_access_token: token_struct}
            )
            return connection

        finally:
            await credential.close()
