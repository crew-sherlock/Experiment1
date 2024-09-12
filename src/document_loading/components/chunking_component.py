import argparse
import json
import logging
import os
import subprocess
import sys

if __name__ == "__main__":
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "langchain-community",
         "langchain", "azure-ai-documentintelligence", "azureml-core",
         "azureml-pipeline-core", "azureml-pipeline-steps"]
    )

from azureml.core import Dataset
from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep

from langchain.text_splitter import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader

from aml_config import AMLConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChunkingComponent:
    def __init__(self, aml_config: AMLConfig) -> None:
        self.aml_config = aml_config

    def chunk_by_headers(self, docs_string: str) -> list:
        headers_to_split_on = [
            ("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3"),
        ]
        text_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, strip_headers=True)
        splits = text_splitter.split_text(docs_string)
        return [
            {"text": chunk.page_content, "metadata": chunk.metadata}
            for chunk in splits
        ]

    def chunk_by_characters(self, docs_string: str, chunk_size: int,
                            chunk_overlap: int) -> list:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        splits = text_splitter.split_text(docs_string)
        return [{"text": chunk} for chunk in splits]

    def chunk_file(self, file_path: str, chunk_by: str, chunk_size: int,
                   chunk_overlap: int) -> list:
        if chunk_by not in ["headers", "characters"]:
            logger.error(f"Invalid chunking strategy: {chunk_by}")
            return []
        try:
            loader = AzureAIDocumentIntelligenceLoader(
                api_endpoint=self.aml_config.ai_doc_intelligence_service,
                api_key=self.aml_config.ai_doc_intelligence_key,
                file_path=file_path, api_model="prebuilt-layout"
            )
            documents = loader.load()
            docs_string = documents[0].page_content

            if chunk_by == "headers":
                chunks = self.chunk_by_headers(docs_string)
            elif chunk_by == "characters":
                chunks = self.chunk_by_characters(docs_string, chunk_size,
                                                  chunk_overlap)
            return chunks
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return []

    def process_file(self, file_path: str, output_dir: str, chunk_by: str,
                     chunk_size: int, chunk_overlap: int) -> None:
        logger.info(f"Processing file: {file_path}")
        chunks = self.chunk_file(file_path, chunk_by, chunk_size, chunk_overlap)

        output_file_path = os.path.join(
            output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}.json")
        with open(output_file_path, 'w') as output_file:
            json.dump(chunks, output_file, indent=4)
        logger.info(f"Chunks for {file_path} saved to {output_file_path}")

    def process_path(self, input_path: str, output_dir: str, chunk_by: str,
                     chunk_size: int, chunk_overlap: int) -> None:
        logger.info(f"Chunking files in {input_path} and saving to {output_dir}")
        if not os.path.exists(output_dir):
            try:
                logger.info("Output directory not found."
                            + f"Creating output directory: {output_dir}")
                os.makedirs(output_dir)
            except Exception as e:
                logger.error(f"Error creating output directory: {e}")
                sys.exit(1)

        if chunk_by == "characters" and chunk_size <= chunk_overlap:
            logger.error(f"Error: chunk_size ({chunk_size}) must be greater than "
                         + f"chunk_overlap ({chunk_overlap}) when chunking by "
                         + "characters.")
            sys.exit(1)

        if os.path.isfile(input_path):
            self.process_file(input_path, output_dir, chunk_by, chunk_size,
                              chunk_overlap)
        elif os.path.isdir(input_path):
            for root, _, files in os.walk(input_path):
                for file in files:
                    if file.endswith(".docx"):
                        file_path = os.path.join(root, file)
                        self.process_file(file_path, output_dir, chunk_by, chunk_size,
                                          chunk_overlap)
                    else:
                        logger.info(f"Skipping file: {file}")
        else:
            logger.error(f"Invalid input path: {input_path}")

    @staticmethod
    def build_step(aml_config: AMLConfig,
                   compute_target: ComputeTarget,
                   dataset: Dataset,
                   chunking_output_dir: PipelineData,
                   run_config: RunConfiguration) -> PythonScriptStep:
        return PythonScriptStep(
            name="Chunking documents with Azure AI Document Intelligence",
            script_name="components/chunking_component.py",
            compute_target=compute_target,
            source_directory=aml_config.path_to_script,
            inputs=[dataset.as_mount()],
            outputs=[chunking_output_dir],
            arguments=[
                "--input_path", dataset.as_mount(),
                "--output_dir", chunking_output_dir,
                "--chunk_by", aml_config.chunking_strategy,
                "--chunk_size", aml_config.chunk_size,
                "--chunk_overlap", aml_config.chunk_overlap,
            ],
            runconfig=run_config,
            allow_reuse=False
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Chunk DOCX files based on headers or characters.")
    parser.add_argument(
        '--input_path', type=str, required=True,
        help="Input file or directory containing DOCX files.")
    parser.add_argument(
        '--output_dir', type=str, required=True,
        help="Output directory to save chunked files.")
    parser.add_argument(
        '--chunk_by', type=str, choices=['headers', 'characters'], default='headers',
        help="Chunk by headers or characters.")
    parser.add_argument(
        '--chunk_size', type=int, default=1000,
        help="Chunk size if chunking by characters.")
    parser.add_argument(
        '--chunk_overlap', type=int, default=200,
        help="Chunk overlap if chunking by characters.")
    args = parser.parse_args()

    aml_config = AMLConfig('aml_pipeline_config.json')
    chunking = ChunkingComponent(aml_config)
    chunking.process_path(args.input_path, args.output_dir, args.chunk_by,
                          args.chunk_size, args.chunk_overlap)
