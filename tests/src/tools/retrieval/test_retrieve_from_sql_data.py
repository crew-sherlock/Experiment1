from unittest.mock import patch, MagicMock
import pytest
from src.tools.retrieval.retrieve_sql_data import retrieve_sql_data


@pytest.fixture
def mock_query_sql():
    with patch("src.tools.retrieval.retrieve_sql_data.QuerySql") as mock:
        yield mock


@pytest.fixture
def mock_asyncio_run():
    with patch("asyncio.run") as mock:
        yield mock


def test_retrieve_sql_data_no_query():
    result = retrieve_sql_data("", ["param1"])
    assert result == {"status": "error", "message": "Please provide a SQL query"}


def test_retrieve_sql_data_success(mock_query_sql, mock_asyncio_run):
    # Arrange
    mock_df = MagicMock()
    mock_df.to_dict.return_value = {"key": "value"}
    mock_asyncio_run.return_value = mock_df

    # Act
    result = retrieve_sql_data("SELECT * FROM table", ["param1"])

    # Assert
    mock_query_sql.assert_called_once()
    mock_asyncio_run.assert_called_once()
    assert result == {"status": "success", "data": {"key": "value"}}


def test_retrieve_sql_data_exception(mock_query_sql, mock_asyncio_run):
    # Arrange
    mock_asyncio_run.side_effect = Exception("Database error")

    # Act
    result = retrieve_sql_data("SELECT * FROM table", ["param1"])

    # Assert
    mock_query_sql.assert_called_once()
    mock_asyncio_run.assert_called_once()
    assert result == {
        "status": "error",
        "message": "Failed to execute query with error Database error"}
