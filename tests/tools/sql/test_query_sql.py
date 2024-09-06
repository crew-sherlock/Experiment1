import os

import pytest
from unittest.mock import AsyncMock, patch, MagicMock, Mock
import pandas as pd

from src.tools.sql.query_sql import QuerySql
from azure.core.credentials import AccessToken

os.environ["AZ_SQL_DATABASE"] = "myazuredatabase"
os.environ["AZ_SQL_SERVER"] = "myazureserver"
driver_str = ('DRIVER=ODBC Driver 13 for SQL Server;SERVER=tcp:'
              'myazureserver.database.windows.net,1433;DATABASE='
              'myazuredatabase;Encrypt=yes;TrustServerCertificate=yes;'
              'Connection Timeout=30')
attrs = {1256: b'\x14\x00\x00\x00<\x00P\x00A\x00S\x00S\x00W\x00O\x00R\x00D\x00>\x00'}


@pytest.mark.asyncio
@patch('src.tools.sql.query_sql.aioodbc.connect', new_callable=AsyncMock)
@patch('src.tools.sql.query_sql.DefaultAzureCredential', autospec=True)
async def test_execute(mock_az_creds, mock_connect):
    # Arrange
    query_sql = QuerySql()
    mock_token = Mock(spec=AccessToken)
    mock_token.token = '<PASSWORD>'
    mock_az_creds.return_value.get_token.return_value = mock_token

    # Mock the database connection and cursor
    mock_connection = MagicMock()
    mock_cursor = AsyncMock()

    mock_connect.return_value.__aenter__.return_value = mock_connection
    mock_connection.cursor.return_value.__aenter__.return_value = mock_cursor

    # Mock the cursor execute and fetchall
    mock_cursor.execute = AsyncMock()
    mock_cursor.description = [("column1",), ("column2",)]
    mock_cursor.fetchall.return_value = [("row1_col1", "row1_col2"),
                                         ("row2_col1", "row2_col2")]

    # Act
    params = ["column1", "table_name"]
    result = await query_sql.execute("SELECT ? FROM ?",
                                     params)

    # Assert

    mock_az_creds.return_value.get_token.assert_called_once_with(
        query_sql.azure_sql_token_url)
    mock_az_creds.return_value.close.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT ? FROM ?", params)
    mock_connect.assert_called_once_with(dsn=driver_str,
                                         attrs_before=attrs)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 2)
    assert result.columns.tolist() == ["column1", "column2"]
    assert result.iloc[0].tolist() == ["row1_col1", "row1_col2"]
    assert result.iloc[1].tolist() == ["row2_col1", "row2_col2"]


@pytest.mark.asyncio
@patch('src.tools.sql.query_sql.DefaultAzureCredential', autospec=True)
async def test_get_aioodbc_connection(mock_credential_class):
    # Arrange
    query_sql = QuerySql()

    # Mock the get_token method
    mock_credential = mock_credential_class.return_value
    mock_token = AsyncMock()
    mock_token.token = '<PASSWORD>'
    mock_credential.get_token.return_value = mock_token

    # Mock the connection function
    with patch('src.tools.sql.query_sql.aioodbc.connect',
               new_callable=AsyncMock) as mock_connect:
        # Act
        connection = await query_sql._get_aioodbc_connection()

        # Assert
        mock_credential.get_token.assert_called_once_with(query_sql.azure_sql_token_url)
        mock_connect.assert_called_once_with(dsn=driver_str,
                                             attrs_before=attrs)
        assert connection == mock_connect.return_value
