import argparse
import json
import logging
import os
import subprocess
import sys
from itertools import islice

if __name__ == "__main__":
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "tiktoken", "numpy", "openai",
         "azureml-core", "azureml-pipeline-core", "azureml-pipeline-steps"]
    )

import numpy as np
import tiktoken

from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep

from embedding_model import EmbeddingModel, EmbeddingStrategy
from aml_config import AMLConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GenerateEmbeddingsComponent:
    def __init__(self, embedding_model: EmbeddingModel) -> None:
        self.embedding_model = embedding_model

    def batched(self, iterable, n: int) -> iter:
        """Batch data into tuples of length n. The last batch may be shorter."""
        if n < 1:
            raise ValueError('n must be at least one')
        it = iter(iterable)
        while (batch := tuple(islice(it, n))):
            yield batch

    def chunked_tokens(self, text: str, encoding_name: str, chunk_length: int) -> iter:
        encoding = tiktoken.get_encoding(encoding_name)
        tokens = encoding.encode(text)
        chunks_iterator = self.batched(tokens, chunk_length)
        yield from chunks_iterator

    def len_safe_generate_embedding(
            self, text: str, max_tokens: int, encoding_name: str, average: bool = True,
            max_retries: int = 5) -> list:
        if max_tokens <= 0:
            raise ValueError("max_tokens must be greater than 0.")
        chunk_embeddings = []
        chunk_lens = []
        for chunk in self.chunked_tokens(
                text, encoding_name=encoding_name, chunk_length=max_tokens
                ):
            retries = 0
            while retries < max_retries:
                embedding = self.embedding_model.generate_embedding(chunk)
                if not np.isnan(embedding).any():
                    chunk_embeddings.append(embedding)
                    chunk_lens.append(len(chunk))
                    break
                else:
                    retries += 1
                    logger.info("Generated embedding for chunk contains NaN values."
                                + f" Retrying... {retries}/{max_retries}")
            if retries == max_retries:
                continue

        if average and chunk_embeddings:
            chunk_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)
            if np.isnan(chunk_embeddings).any():
                return None

            norm = np.linalg.norm(chunk_embeddings)
            if norm == 0:
                return chunk_embeddings.tolist()

            chunk_embeddings = chunk_embeddings / norm
            chunk_embeddings = chunk_embeddings.tolist()
        return chunk_embeddings

    def embed_chunks(self, file_path: str) -> list:
        embeddings = []
        try:
            with open(file_path, 'r') as file:
                chunks = json.load(file)
                for chunk in chunks:
                    chunk["text_vector"] = self.len_safe_generate_embedding(
                        text=chunk["text"],
                        # text-embedding-ada-002: max token limit of 8192
                        max_tokens=8192,
                        # text-embedding-ada-002: cl100k_base encoding for tokenization
                        encoding_name="cl100k_base")
                    embeddings.append(chunk)
        except Exception as e:
            logger.error(f"Error reading or processing file {file_path}: {e}")
            return None
        return embeddings

    def process_file(self, file_path: str, output_dir: str) -> None:
        logger.info(f"Processing file: {file_path}")
        embedded_chunks = self.embed_chunks(file_path)
        if embedded_chunks is None:
            logger.error(f"Failed to process file: {file_path}")
            return

        output_file_path = os.path.join(
            output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}.json")
        try:
            with open(output_file_path, 'w') as output_file:
                json.dump(embedded_chunks, output_file, indent=4)
            logger.info(f"Embeddings for {file_path} saved to {output_file_path}")
        except Exception as e:
            logger.error(f"Error writing to output file {output_file_path}: {e}")

    def process_path(self, input_path: str, output_dir: str) -> None:
        logger.info(f"Generating embeddings for files in: {input_path}"
                    + f" and saving to: {output_dir}")
        if not os.path.exists(output_dir):
            try:
                logger.info("Output directory not found."
                            + f"Creating output directory: {output_dir}")
                os.makedirs(output_dir)
            except Exception as e:
                logger.error(f"Error creating output directory: {e}")
                sys.exit(1)

        if os.path.isfile(input_path):
            self.process_file(input_path, output_dir)
        elif os.path.isdir(input_path):
            for root, _, files in os.walk(input_path):
                for file in files:
                    if file.endswith(".json"):
                        file_path = os.path.join(root, file)
                        self.process_file(file_path, output_dir)
                    else:
                        logger.info(f"Skipping file: {file}")
        else:
            logger.error(f"Invalid input path: {input_path}")

    @staticmethod
    def build_step(aml_config: AMLConfig,
                   compute_target: ComputeTarget,
                   chunking_output_dir: PipelineData,
                   embedding_output_dir: PipelineData,
                   run_config: RunConfiguration) -> PythonScriptStep:
        return PythonScriptStep(
            name="Generate embeddings for text chunks",
            script_name="components/generate_embeddings_component.py",
            compute_target=compute_target,
            source_directory=aml_config.path_to_script,
            inputs=[chunking_output_dir],
            outputs=[embedding_output_dir],
            arguments=[
                "--input_path", chunking_output_dir,
                "--output_dir", embedding_output_dir,
            ],
            runconfig=run_config,
            allow_reuse=False
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate embeddings for chunked files.")
    parser.add_argument(
        '--input_path', type=str, required=True,
        help="Input file or directory containing chunked files.")
    parser.add_argument(
        '--output_dir', type=str, required=True,
        help="Output directory to save chunked files with embeddings.")
    args = parser.parse_args()

    aml_config = AMLConfig('aml_pipeline_config.json')

    embedding_model = EmbeddingModel.get_by_strategy(
        EmbeddingStrategy.AOAI,
        azure_endpoint=aml_config.aoai_api_base,
        api_key=aml_config.aoai_api_key,
        api_version=aml_config.aoai_api_version,
        deployment_name=aml_config.embedding_model_deployment_name
        )

    component = GenerateEmbeddingsComponent(embedding_model)
    component.process_path(args.input_path, args.output_dir)
