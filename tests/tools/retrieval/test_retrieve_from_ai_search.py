from unittest.mock import patch

import pytest
from src.tools.retrieval.retrieve_from_ai_search import retrieve_from_ai_search


@pytest.mark.parametrize("query,index_name", [
    (None, "index_name"),
    ("", "index_name"),
    ("query", None),
    ("query", "")
])
def test_retrieve_from_ai_search_returns_empty_array_when_inputs_are_empty(
    query,
    index_name
):
    result = retrieve_from_ai_search(query, index_name, "https://127.0.0.1:8080")

    assert result == []


@patch('src.tools.retrieval.retrieve_from_ai_search.SearchClient')
def test_retrieve_from_ai_search_uses_query_for_search_when_value_is_passed(
    mock_search_client
):
    mock_instance = mock_search_client.return_value
    mock_instance.search.return_value = []

    query = "test query"
    retrieve_from_ai_search(query, "index_name", "https://127.0.0.1:8080")

    assert mock_instance.search.call_args[1]["search_text"] == query


@patch('src.tools.retrieval.retrieve_from_ai_search.SearchClient')
def test_retrieve_from_ai_search_returns_empty_array_when_no_results(
    mock_search_client
):
    mock_instance = mock_search_client.return_value
    mock_instance.search.return_value = []

    result = retrieve_from_ai_search("test query", "index_name", "https://127.0.0.1:8")

    assert result == []


@patch('src.tools.retrieval.retrieve_from_ai_search.SearchClient')
def test_retrieve_from_ai_search_returns_mapped_array_when_search_has_results(
    mock_search_client
):
    mock_instance = mock_search_client.return_value
    mock_instance.search.return_value = [
        {"content": "test content", "url": "my url"},
        {"content": "test content 2", "url": "my url 2"},
    ]

    result = retrieve_from_ai_search("test query", "index_name", "https://127.0.0.1:8")

    assert len(result) == 2
    assert result == [
        {"content": "test content", "source": "my url"},
        {"content": "test content 2", "source": "my url 2"},
    ]
