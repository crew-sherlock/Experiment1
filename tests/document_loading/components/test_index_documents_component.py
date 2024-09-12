import unittest
from unittest.mock import patch, MagicMock

from azure.identity import ClientSecretCredential
from datetime import datetime, timezone
import hashlib

from src.document_loading.components.index_documents_component import (
    IndexDocumentsComponent
)
from src.document_loading.aml_config import AMLConfig


class TestIndexDocumentsComponent(unittest.TestCase):

    def setUp(self):
        self.aml_config = MagicMock(AMLConfig)
        self.aml_config.search_service_name = "https://test.search.windows.net"
        self.component = IndexDocumentsComponent(self.aml_config)
        self.mock_client = MagicMock()
        self.filename = "test.json"
        self.file_id = "test_file_id"
        self.current_datetime_str = datetime.now().replace(
            tzinfo=timezone.utc).strftime('%Y%m%d%H%M%S%f')
        self.credential = MagicMock(spec=ClientSecretCredential)

    def test_validate_json(self):
        valid_json = '{"key": "value"}'
        invalid_json = '{"key": "value"'
        self.assertTrue(self.component.validate_json(valid_json))
        self.assertFalse(self.component.validate_json(invalid_json))

    def test_filename_to_id(self):
        filename = "test.json"
        expected_hash = hashlib.sha256(filename.encode('utf-8')).hexdigest()
        self.assertEqual(self.component.filename_to_id(filename), expected_hash)

    @patch('os.path.exists')
    @patch('os.remove')
    def test_remove_documents(self, mock_remove, mock_exists):
        mock_exists.return_value = True
        self.mock_client.search.return_value = [{"id": "doc1"}, {"id": "doc2"}]
        self.component.remove_documents(self.mock_client, self.filename)
        self.mock_client.delete_documents.assert_called_once_with(
            documents=[{"id": "doc1"}, {"id": "doc2"}])

    @patch('builtins.open', new_callable=unittest.mock.mock_open,
           read_data='[{"text": "test"}]')
    def test_load_chunks_from_file(self, mock_file):
        chunks = self.component.load_chunks_from_file("test_path")
        self.assertEqual(chunks, [{"text": "test"}])

    @patch('builtins.open', new_callable=unittest.mock.mock_open,
           read_data='invalid json')
    def test_load_chunks_from_file_invalid_json(self, mock_file):
        chunks = self.component.load_chunks_from_file("test_path")
        self.assertEqual(chunks, [])

    def test_create_document(self):
        chunk = {"text": "test", "text_vector": [0.1, 0.2],
                 "metadata": {"Header 1": "value1"}}
        document = self.component.create_document(self.filename, self.file_id,
                                                  self.current_datetime_str, 0, chunk)
        self.assertEqual(document["filename"], self.filename)
        self.assertEqual(document["text"], "test")
        self.assertEqual(document["textVector"], [0.1, 0.2])
        self.assertEqual(document["metadata"]["Header1"], "value1")

    @patch.object(IndexDocumentsComponent, 'load_chunks_from_file')
    @patch.object(IndexDocumentsComponent, 'remove_documents')
    def test_process_file(self, mock_remove_documents, mock_load_chunks_from_file):
        mock_load_chunks_from_file.return_value = [{"text": "test"}]
        documents = self.component.process_file(
            self.mock_client, self.filename, "input_path", self.current_datetime_str)
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0]["filename"], self.filename)

    @patch('os.listdir')
    @patch.object(IndexDocumentsComponent, 'process_file')
    def test_index_documents(self, mock_process_file, mock_listdir):
        mock_listdir.return_value = ["test.json"]
        mock_process_file.return_value = [{"id": "doc1"}]
        self.component.index_documents(self.mock_client, "index_name", "input_path")
        self.mock_client.upload_documents.assert_called_once_with(
            documents=[{"id": "doc1"}])

    @patch('azure.search.documents.SearchClient')
    @patch.object(IndexDocumentsComponent, 'index_documents')
    def test_create_client(self, mock_index_documents, _):
        self.component.create_client(self.credential, "index_name", "input_path")
        mock_index_documents.assert_called_once()


if __name__ == '__main__':
    unittest.main()
