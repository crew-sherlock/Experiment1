import pytest
import unittest
from unittest.mock import patch, MagicMock
from src.document_loading.components.chunking_component import ChunkingComponent
from src.document_loading.aml_config import AMLConfig


class TestChunkingComponent(unittest.TestCase):

    def setUp(self):
        self.aml_config = MagicMock(AMLConfig)
        self.aml_config.ai_doc_intelligence_service = "service"
        self.aml_config.ai_doc_intelligence_key = "key"
        self.chunking = ChunkingComponent(self.aml_config)

    @patch("src.document_loading.components.chunking_component.MarkdownHeaderTextSplitter")
    def test_chunk_by_headers(self, mock_markdown_header_text_splitter):
        docs_string = "# Header 1\nText 1\n## Header 2\nText 2\n### Header 3\nText 3"
        mock_markdown_header_text_splitter.return_value.split_text.return_value = [
            MagicMock(page_content="Text 1", metadata="Header 1"),
            MagicMock(page_content="Text 2", metadata="Header 2"),
            MagicMock(page_content="Text 3", metadata="Header 3"),
        ]
        result = self.chunking.chunk_by_headers(docs_string)
        self.assertEqual(
            result,
            [
                {"text": "Text 1", "metadata": "Header 1"},
                {"text": "Text 2", "metadata": "Header 2"},
                {"text": "Text 3", "metadata": "Header 3"},
            ],
        )
        mock_markdown_header_text_splitter.assert_called_once_with(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ],
            strip_headers=True,
        )

    def test_chunk_by_headers_with_empty_string(self):
        docs_string = ""
        result = self.chunking.chunk_by_headers(docs_string)
        self.assertEqual(result, [])

    @patch("src.document_loading.components.chunking_component.RecursiveCharacterTextSplitter")
    def test_chunk_by_characters(self, mock_recursive_character_text_splitter):
        docs_string = "Text 1\nText 2\nText 3"
        mock_recursive_character_text_splitter.return_value.split_text.return_value = [
            "Text 1",
            "Text 2",
            "Text 3",
        ]
        result = self.chunking.chunk_by_characters(docs_string, 10, 5)
        self.assertEqual(
            result, [{"text": "Text 1"}, {"text": "Text 2"}, {"text": "Text 3"}]
        )
        mock_recursive_character_text_splitter.assert_called_once_with(
            chunk_size=10, chunk_overlap=5
        )

    @patch("src.document_loading.components.chunking_component.AzureAIDocumentIntelligenceLoader")
    @patch("src.document_loading.components.chunking_component.ChunkingComponent.chunk_by_headers")
    @patch("src.document_loading.components.chunking_component.ChunkingComponent.chunk_by_characters")
    def test_chunk_file(self, _, mock_chunk_by_headers, mock_loader):
        mock_loader.return_value.load.return_value = [MagicMock(page_content="Text 1")]
        mock_chunk_by_headers.return_value = [
            {"text": "Text 1", "metadata": "Header 1"}
        ]
        result = self.chunking.chunk_file("file_path", "headers", 10, 5)
        self.assertEqual(result, [{"text": "Text 1", "metadata": "Header 1"}])
        mock_loader.assert_called_once_with(
            api_endpoint=self.aml_config.ai_doc_intelligence_service,
            api_key=self.aml_config.ai_doc_intelligence_key,
            file_path="file_path",
            api_model="prebuilt-layout",
        )

    @patch("src.document_loading.components.chunking_component.AzureAIDocumentIntelligenceLoader")
    @patch("src.document_loading.components.chunking_component.ChunkingComponent.chunk_by_headers")
    @patch("src.document_loading.components.chunking_component.ChunkingComponent.chunk_by_characters")
    @patch("src.document_loading.components.chunking_component.logger")
    def test_chunk_file_with_invalid_strategy(self, mock_logger, _, __, mock_loader):
        mock_loader.return_value.load.return_value = [MagicMock(page_content="Text 1")]
        result = self.chunking.chunk_file("file_path", "invalid_strategy", 10, 5)
        self.assertEqual(result, [])
        mock_logger.error.assert_called_once_with(
            "Invalid chunking strategy: invalid_strategy"
        )

    @patch("src.document_loading.components.chunking_component.AzureAIDocumentIntelligenceLoader")
    @patch("src.document_loading.components.chunking_component.ChunkingComponent.chunk_by_headers")
    @patch("src.document_loading.components.chunking_component.ChunkingComponent.chunk_by_characters")
    @patch("src.document_loading.components.chunking_component.logger")
    def test_chunk_file_with_exception(self, mock_logger, _, __, mock_loader):
        mock_loader.return_value.load.side_effect = Exception("error")
        result = self.chunking.chunk_file("file_path", "headers", 10, 5)
        self.assertEqual(result, [])
        mock_logger.error.assert_called_once_with(
            "Error processing file file_path: error"
        )

    @patch("src.document_loading.components.chunking_component.ChunkingComponent.chunk_file")
    @patch("src.document_loading.components.chunking_component.open")
    @patch("src.document_loading.components.chunking_component.json")
    def test_process_file(self, mock_json, mock_open, mock_chunk_file):
        mock_json.dump = MagicMock()
        mock_open_context_manager = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_open_context_manager
        mock_chunk_file.return_value = [{"text": "Text 1", "metadata": "Header 1"}]
        result = self.chunking.process_file("file_path", "output_dir", "headers", 10, 5)
        self.assertIsNone(result)
        mock_open.assert_called_once_with("output_dir/file_path.json", "w")
        mock_json.dump.assert_called_once_with(
            [{"text": "Text 1", "metadata": "Header 1"}],
            mock_open_context_manager,
            indent=4,
        )

    @patch("src.document_loading.components.chunking_component.ChunkingComponent.process_file")
    @patch("src.document_loading.components.chunking_component.os")
    def test_process_path_when_path_is_file(self, mock_os, mock_process_file):
        mock_os.path.isfile.return_value = True
        mock_os.path.exists.return_value = True
        result = self.chunking.process_path("file_path", "output_dir", "headers", 10, 5)
        self.assertIsNone(result)
        mock_process_file.assert_called_once_with(
            "file_path", "output_dir", "headers", 10, 5
        )

    @patch("src.document_loading.components.chunking_component.ChunkingComponent.process_file")
    @patch("src.document_loading.components.chunking_component.os")
    @patch("src.document_loading.components.chunking_component.logger")
    def test_process_path_when_path_is_directory(
        self, mock_logger, mock_os, mock_process_file
    ):
        mock_os.path.isfile.return_value = False
        mock_os.path.isdir.return_value = True
        mock_os.path.exists.return_value = True
        mock_os.walk.return_value = [
            ("root", ["dir1", "dir2"], ["file1.docx", "file2.txt"]),
            ("root/dir1", [], ["file3.docx"]),
            ("root/dir2", [], ["file4.txt"]),
        ]
        mock_os.path.join.side_effect = lambda *args: "/".join(args)

        result = self.chunking.process_path(
            "input_path", "output_dir", "headers", 10, 5
        )
        self.assertIsNone(result)
        mock_process_file.assert_has_calls(
            [
                unittest.mock.call("root/file1.docx", "output_dir", "headers", 10, 5),
                unittest.mock.call(
                    "root/dir1/file3.docx", "output_dir", "headers", 10, 5
                ),
            ],
            any_order=True,
        )
        mock_logger.info.assert_has_calls(
            [
                unittest.mock.call(
                    "Chunking files in input_path and saving to output_dir"
                ),
                unittest.mock.call("Skipping file: file2.txt"),
                unittest.mock.call("Skipping file: file4.txt"),
            ],
            any_order=True,
        )

    @patch("src.document_loading.components.chunking_component.ChunkingComponent.process_file")
    @patch("src.document_loading.components.chunking_component.os")
    @patch("src.document_loading.components.chunking_component.logger")
    def test_process_path_when_path_is_invalid(self, mock_logger, mock_os, _):
        mock_os.path.isfile.return_value = False
        mock_os.path.isdir.return_value = False
        result = self.chunking.process_path(
            "invalid_path", "output_dir", "headers", 10, 5
        )
        self.assertIsNone(result)
        mock_logger.error.assert_called_once_with("Invalid input path: invalid_path")

    @patch("src.document_loading.components.chunking_component.ChunkingComponent.process_file")
    @patch("src.document_loading.components.chunking_component.os")
    @patch("src.document_loading.components.chunking_component.logger")
    def test_process_path_when_chunk_size_is_smaller_than_overlap(
        self, mock_logger, mock_os, _
    ):
        mock_os.path.exists.return_value = True
        with pytest.raises(SystemExit) as excinfo:
            self.chunking.process_path("input_path", "output_dir", "characters", 5, 10)
        self.assertEqual(excinfo.value.code, 1)
        mock_logger.error.assert_called_once_with(
            "Error: chunk_size (5) must be greater than chunk_overlap (10) "
            + "when chunking by characters."
        )


if __name__ == "__main__":
    unittest.main()
