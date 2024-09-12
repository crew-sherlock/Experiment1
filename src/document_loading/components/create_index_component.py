import argparse
import json
import logging
import subprocess
import sys

if __name__ == "__main__":
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "azure-search-documents",
         "azure-identity", "azure-core", "azureml-core", "azureml-pipeline-core",
         "azureml-pipeline-steps"]
    )

from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.steps import PythonScriptStep

from azure.identity import ClientSecretCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchFieldDataType,
    SearchIndex,
    SearchableField,
    SearchField,
    SimpleField,
    ComplexField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    HnswParameters,
    VectorSearchAlgorithmMetric,
    VectorSearchProfile,
)

from aml_config import AMLConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreateIndexComponent:
    def __init__(self, aml_config: AMLConfig) -> None:
        self.aml_config = aml_config

    def create_index(self, client: SearchIndexClient, name: str, fields: list = None,
                     vector_search: VectorSearch = None, cors_options: dict = None,
                     scoring_profiles: list = None) -> None:
        if fields is None:
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                SearchableField(name="filename", type=SearchFieldDataType.String,
                                filterable=True, sortable=True),
                SimpleField(name="ingestionDate",
                            type=SearchFieldDataType.DateTimeOffset,
                            filterable=True, sortable=True),
                # chunk fields must NOT be sortable or filterable
                # because their content is too large to process
                SearchableField(name="text", type=SearchFieldDataType.String),
                SearchField(name="textVector", type=SearchFieldDataType.Collection(
                    SearchFieldDataType.Single), vector_search_dimensions=1536,
                    vector_search_profile_name="myHnswProfile"),
                ComplexField(name="metadata", fields=[
                    SearchableField(name="Header1", type=SearchFieldDataType.String),
                    SearchableField(name="Header2", type=SearchFieldDataType.String),
                    SearchableField(name="Header3", type=SearchFieldDataType.String),
                ])
            ]

        if vector_search is None:
            vector_search = VectorSearch(
                algorithms=[
                    HnswAlgorithmConfiguration(
                        name="myHnsw",
                        parameters=HnswParameters(
                            m=4,
                            ef_construction=400,
                            ef_search=500,
                            metric=VectorSearchAlgorithmMetric.COSINE,
                        ),
                    ),
                ],
                profiles=[
                    VectorSearchProfile(
                        name="myHnswProfile",
                        algorithm_configuration_name="myHnsw"
                    ),
                ]
            )

        index = SearchIndex(
            name=name,
            fields=fields,
            vector_search=vector_search,
            scoring_profiles=scoring_profiles,
            cors_options=cors_options
        )

        try:
            client.create_or_update_index(index)
            logger.info(f"Index '{name}' created successfully.")
        except Exception as e:
            logger.error(f"Failed to create index '{name}': {e}")

    def create_client(self, credential: ClientSecretCredential,
                      index_name: str, fields: list = None,
                      vector_search: VectorSearch = None, cors_options: dict = None,
                      scoring_profiles: list = None) -> None:
        client = SearchIndexClient(self.aml_config.search_service_name, credential)
        logger.info(f"Creating index '{index_name}'...")
        self.create_index(client, index_name, fields, vector_search,
                          cors_options, scoring_profiles)

    @staticmethod
    def build_step(aml_config: AMLConfig,
                   compute_target: ComputeTarget,
                   run_config: RunConfiguration) -> PythonScriptStep:
        create_index_arguments = [
            "--index_name", aml_config.index_name,
        ]

        for arg_name, config_value in [("fields", aml_config.fields),
                                       ("vector_search", aml_config.vector_search),
                                       ("cors_options", aml_config.cors_options),
                                       ("scoring_profiles",
                                        aml_config.scoring_profiles)]:
            if config_value is not None:
                create_index_arguments.extend([f"--{arg_name}",
                                               json.dumps(config_value)])
        return PythonScriptStep(
            name="Create index schema in Azure AI Search",
            script_name="components/create_index_component.py",
            compute_target=compute_target,
            source_directory=aml_config.path_to_script,
            arguments=create_index_arguments,
            runconfig=run_config,
            allow_reuse=False
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a search index in Azure AI Search.")
    parser.add_argument(
        '--index_name', type=str, required=True,
        help="The name of the search index.")
    parser.add_argument(
        '--fields', type=str, help="The fields to include in the index.")
    parser.add_argument(
        '--vector_search', type=str,
        help="The vector search configuration for the index.")
    parser.add_argument(
        '--cors_options', type=str, help="The CORS options for the index.")
    parser.add_argument(
        '--scoring_profiles', type=str, help="The scoring profiles for the index.")
    args = parser.parse_args()

    aml_config = AMLConfig('aml_pipeline_config.json')
    credential = ClientSecretCredential(
        tenant_id=aml_config.tenant_id, client_id=aml_config.service_principal_id,
        client_secret=aml_config.service_principal_password)

    fields = json.loads(args.fields) if args.fields else None
    vector_search = json.loads(args.vector_search) if args.vector_search else None
    cors_options = json.loads(args.cors_options) if args.cors_options else None
    scoring_profiles = json.loads(
        args.scoring_profiles) if args.scoring_profiles else None

    create_index = CreateIndexComponent(aml_config)
    create_index.create_client(credential, args.index_name, fields, vector_search,
                               cors_options, scoring_profiles)
