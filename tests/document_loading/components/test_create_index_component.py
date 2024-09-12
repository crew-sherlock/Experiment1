import unittest
from unittest.mock import MagicMock, patch

from azure.identity import ClientSecretCredential
from azure.search.documents.indexes.models import SearchIndex

from src.document_loading.components.create_index_component import CreateIndexComponent
from src.document_loading.aml_config import AMLConfig


class TestCreateIndexComponent(unittest.TestCase):

    def setUp(self):
        self.aml_config = MagicMock(AMLConfig)
        self.aml_config.search_service_name = "https://test.search.windows.net"
        self.create_index_component = CreateIndexComponent(self.aml_config)
        self.credential = MagicMock(spec=ClientSecretCredential)

    @patch('components.create_index_component.SearchIndexClient')
    def test_create_index_with_no_args(self, mock_search_index_client):
        mock_client = mock_search_index_client.return_value
        self.create_index_component.create_index(mock_client, "test-index")
        mock_client.create_or_update_index.assert_called_once()
        args, kwargs = mock_client.create_or_update_index.call_args
        self.assertIsInstance(args[0], SearchIndex)
        self.assertEqual(args[0].name, "test-index")
        self.assertEqual(args[0].fields[0].name, "id")
        self.assertEqual(args[0].fields[1].name, "filename")
        self.assertEqual(args[0].fields[2].name, "ingestionDate")
        self.assertEqual(args[0].fields[3].name, "text")
        self.assertEqual(args[0].fields[4].name, "textVector")
        self.assertEqual(args[0].fields[5].name, "metadata")

    @patch('components.create_index_component.SearchIndexClient')
    def test_create_index_with_args(self, mock_search_index_client):
        mock_client = mock_search_index_client.return_value
        self.create_index_component.create_index(mock_client, "test-index", fields=[
            {"name": "id", "type": "String", "key": True},
            {"name": "file", "type": "String", "filterable": True, "sortable": True},
            {"name": "date", "type": "DateTimeOffset",
             "filterable": True, "sortable": True},
            {"name": "content", "type": "String"},
            {"name": "content_vector", "type": "Collection",
             "vector_search_dimensions": 1536,
             "vector_search_profile_name": "myHnswProfile"}
        ])
        mock_client.create_or_update_index.assert_called_once()
        args, kwargs = mock_client.create_or_update_index.call_args
        self.assertIsInstance(args[0], SearchIndex)
        self.assertEqual(args[0].name, "test-index")
        self.assertEqual(args[0].fields[0]['name'], "id")
        self.assertEqual(args[0].fields[1]['name'], "file")
        self.assertEqual(args[0].fields[2]['name'], "date")
        self.assertEqual(args[0].fields[3]['name'], "content")
        self.assertEqual(args[0].fields[4]['name'], "content_vector")

    @patch('components.create_index_component.SearchIndexClient')
    @patch.object(CreateIndexComponent, 'create_index')
    def test_create_client(self, mock_create_index, _):
        self.create_index_component.create_client(self.credential, "index_name")
        mock_create_index.assert_called_once()


if __name__ == '__main__':
    unittest.main()
