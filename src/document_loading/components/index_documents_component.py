import argparse
from datetime import datetime, timezone
import hashlib
import json
import logging
import os
import subprocess
import sys
from json.decoder import JSONDecodeError

if __name__ == "__main__":
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "azure-search-documents",
         "azure-identity", "azure-core", "azureml-core", "azureml-pipeline-core",
         "azureml-pipeline-steps"]
    )

from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep

from azure.core.exceptions import HttpResponseError
from azure.identity import ClientSecretCredential
from azure.search.documents import SearchClient

from aml_config import AMLConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndexDocumentsComponent:
    def __init__(self, aml_config: AMLConfig) -> None:
        self.aml_config = aml_config

    def validate_json(self, json_data: str) -> bool:
        try:
            json.loads(json_data)
            return True
        except JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            return False

    def filename_to_id(self, filename: str) -> str:
        encoded_filename = filename.encode('utf-8')
        hash_object = hashlib.sha256(encoded_filename)
        file_name_hash = hash_object.hexdigest()
        return file_name_hash

    def remove_documents(self, client: SearchClient, filename: str) -> None:
        try:
            search_results = client.search(
                search_text="", filter=f"filename eq '{filename}'")
            documents_to_delete = [{"id": doc["id"]} for doc in search_results]

            if not documents_to_delete:
                return

            client.delete_documents(documents=documents_to_delete)
            logger.info(f"Existing documents with {filename} deleted.")
        except HttpResponseError as e:
            logger.error(f"Failed to delete documents: {e}")

    def load_chunks_from_file(self, file_path: str) -> list:
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
                if not self.validate_json(file_content):
                    logger.error(f"Skipping invalid JSON file: {file_path}")
                    return []
                chunks = json.loads(file_content)
                return chunks
        except Exception as e:
            logger.error(f"Unexpected error reading file {file_path}: {e}")
            return []

    def create_document(self, filename: str, file_id: str, current_datetime_str: str,
                        idx: int, chunk: dict) -> dict:
        metadata = chunk.get("metadata", {})
        metadata = {
            "Header1": metadata.get("Header 1", ""),
            "Header2": metadata.get("Header 2", ""),
            "Header3": metadata.get("Header 3", "")
        }
        document = {
            "id": (
                f"file-{file_id}-"
                f"date-{current_datetime_str}-"
                f"chunk-{idx}"
            ),
            "filename": filename,
            "ingestionDate": datetime.now().replace(tzinfo=timezone.utc),
            "text": chunk["text"],
            "textVector": chunk.get("text_vector", []),
            "metadata": metadata
        }
        return document

    def process_file(self, client: SearchClient, filename: str, input_path: str,
                     current_datetime_str: str) -> list:
        file_path = os.path.join(input_path, filename)
        self.remove_documents(client, filename)
        chunks = self.load_chunks_from_file(file_path)
        file_id = self.filename_to_id(filename)
        documents = [
            self.create_document(filename, file_id, current_datetime_str, idx, chunk)
            for idx, chunk in enumerate(chunks)
        ]
        return documents

    def index_documents(self, client: SearchClient, index_name: str,
                        input_path: str) -> None:
        documents = []
        current_datetime_str = datetime.now().replace(
            tzinfo=timezone.utc).strftime('%Y%m%d%H%M%S%f')

        for filename in os.listdir(input_path):
            if filename.endswith(".json"):
                logger.info(f"Processing file: {filename}")
                documents.extend(self.process_file(client, filename, input_path,
                                                   current_datetime_str))

        logger.info(f"Uploading {len(documents)} documents to index '{index_name}'...")
        try:
            result = client.upload_documents(documents=documents)
            for res in result:
                if not res.succeeded:
                    logger.error(f"Failed to upload document ID {res.key}: "
                                 + f"{res.error_message}")
                else:
                    logger.info(f"Successfully uploaded document ID {res.key}")
        except HttpResponseError as e:
            logger.error(f"Failed to upload documents: {e}")

    def create_client(self, credential: ClientSecretCredential,
                      index_name: str, input_path: str) -> None:
        client = SearchClient(self.aml_config.search_service_name, index_name,
                              credential)
        self.index_documents(client, index_name, input_path)

    @staticmethod
    def build_step(aml_config: AMLConfig, compute_target: ComputeTarget,
                   embedding_output_dir: PipelineData,
                   run_config: RunConfiguration) -> PythonScriptStep:
        return PythonScriptStep(
            name="Index documents in Azure AI Search",
            script_name="components/index_documents_component.py",
            compute_target=compute_target,
            source_directory=aml_config.path_to_script,
            inputs=[embedding_output_dir],
            arguments=[
                "--index_name", aml_config.index_name,
                "--input_path", embedding_output_dir,
            ],
            runconfig=run_config,
            allow_reuse=False
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Index documents in the Azure AI Search")
    parser.add_argument(
        '--index_name', type=str, required=True, help="The name of the search index.")
    parser.add_argument(
        '--input_path', type=str, required=True,
        help="The path to the directory containing JSON files with chunked documents.")
    args = parser.parse_args()

    aml_config = AMLConfig('aml_pipeline_config.json')
    credential = ClientSecretCredential(
        tenant_id=aml_config.tenant_id, client_id=aml_config.service_principal_id,
        client_secret=aml_config.service_principal_password)

    index_documents = IndexDocumentsComponent(aml_config)
    index_documents.create_client(credential, args.index_name, args.input_path)
