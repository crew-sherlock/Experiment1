import os
import numpy as np
import unittest
from unittest.mock import patch, MagicMock
from src.document_loading.components.generate_embeddings_component import (
    GenerateEmbeddingsComponent
)


class TestGenerateEmbeddingsComponent(unittest.TestCase):

    @patch('components.generate_embeddings_component.EmbeddingModel')
    def setUp(self, mock_embedding_model):
        self.mock_embedding_model = mock_embedding_model
        self.component = GenerateEmbeddingsComponent(self.mock_embedding_model)

    def test_initialization(self):
        self.assertEqual(self.component.embedding_model, self.mock_embedding_model)

    def test_batched(self):
        iterable = [1, 2, 3, 4, 5]
        result = list(self.component.batched(iterable, 2))
        self.assertEqual(result, [(1, 2), (3, 4), (5,)])

    def test_batched_invalid_n(self):
        with self.assertRaises(ValueError):
            list(self.component.batched([1, 2, 3], 0))

    @patch('tiktoken.get_encoding')
    def test_chunked_tokens(self, mock_get_encoding):
        mock_encoding = MagicMock()
        mock_encoding.encode.return_value = [1, 2, 3, 4, 5]
        mock_get_encoding.return_value = mock_encoding

        result = list(self.component.chunked_tokens("test", "test_encoding", 2))
        self.assertEqual(result, [(1, 2), (3, 4), (5,)])

    @patch.object(GenerateEmbeddingsComponent, 'chunked_tokens')
    def test_len_safe_generate_embedding(self, mock_chunked_tokens):
        mock_chunked_tokens.return_value = [[1, 2], [3, 4]]
        self.mock_embedding_model.generate_embedding.side_effect = [
            np.array([0.1, 0.2]), np.array([0.3, 0.4])
        ]

        result = self.component.len_safe_generate_embedding("test", 2, "test_encoding")
        self.assertEqual(result, [0.5547001962252291, 0.8320502943378437])

    @patch('builtins.open', new_callable=unittest.mock.mock_open,
           read_data='[{"text": "test"}]')
    @patch.object(GenerateEmbeddingsComponent, 'len_safe_generate_embedding')
    def test_embed_chunks(self, mock_len_safe_generate_embedding, mock_open):
        mock_len_safe_generate_embedding.return_value = [0.1, 0.2]

        result = self.component.embed_chunks("test_path")
        self.assertEqual(result, [{"text": "test", "text_vector": [0.1, 0.2]}])

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch.object(GenerateEmbeddingsComponent, 'embed_chunks')
    def test_process_file(self, mock_embed_chunks, mock_open):
        mock_embed_chunks.return_value = [{"text": "test", "text_vector": [0.1, 0.2]}]

        self.component.process_file("test_path", "output_dir")
        mock_open.assert_called_with(os.path.join("output_dir", "test_path.json"), 'w')

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch.object(GenerateEmbeddingsComponent, 'process_file')
    def test_process_path(self, mock_process_file, mock_os_walk, mock_os_isdir,
                          mock_os_isfile, mock_os_makedirs, mock_os_exists):
        mock_os_exists.return_value = False
        mock_os_isfile.return_value = True
        mock_os_isdir.return_value = False

        self.component.process_path("input_path", "output_dir")
        mock_os_makedirs.assert_called_with("output_dir")
        mock_process_file.assert_called_with("input_path", "output_dir")

        mock_os_exists.return_value = True
        mock_os_isfile.return_value = False
        mock_os_isdir.return_value = True
        mock_os_walk.return_value = [("root", [], ["file.json"])]

        self.component.process_path("input_path", "output_dir")
        mock_process_file.assert_called_with(
            os.path.join("root", "file.json"), "output_dir")


if __name__ == '__main__':
    unittest.main()
