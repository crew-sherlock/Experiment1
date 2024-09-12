import json
import logging
import os

from dotenv import load_dotenv
from azureml.core import Environment
from azureml.core.runconfig import RunConfiguration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AMLConfig:
    def __init__(self, config_path):
        self.config_path = os.path.join(os.path.dirname(__file__), config_path)
        self.env_variables = {}
        self.load_config()
        self.load_env_variables()

    def load_config(self):
        try:
            with open(self.config_path) as config_file:
                config = json.load(config_file)
        except FileNotFoundError:
            logger.error(f"Error: The file at {self.config_path} was not found.")
            config = None
        except json.JSONDecodeError:
            logger.error(f"Error: The file at {self.config_path} is not a valid JSON.")
            config = None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            config = None

        if config:
            self.compute_name = config['compute_name']
            self.path_to_script = config['path_to_script']
            self.vm_size = config['vm_size']
            self.max_nodes = config['max_nodes']
            self.experiment_name = config['experiment_name']
            self.storage_account_name = config['storage_account_name']
            self.container_name = config['container_name']
            self.datastore_name = config['datastore_name']
            self.data_path = config['data_path']
            self.chunking_strategy = config['chunking_strategy']
            self.chunk_size = config['chunk_size']
            self.chunk_overlap = config['chunk_overlap']
            self.index_name = config['index_name']
            self.fields = config.get('fields')
            self.vector_search = config.get('vector_search')
            self.cors_options = config.get('cors_options')
            self.scoring_profiles = config.get('scoring_profiles')
        else:
            logger.error(
                "Error: Configuration could not be loaded. "
                "Please check the configuration file."
            )

    def load_env_variables(self):
        load_dotenv()
        self.subscription_id = self.load_env_variable('AZURE_SUBSCRIPTION_ID')
        self.resource_group = self.load_env_variable('RESOURCE_GROUP_NAME')
        self.workspace_name = self.load_env_variable('WORKSPACE_NAME')
        self.tenant_id = self.load_env_variable('AZURE_TENANT_ID')
        self.service_principal_id = self.load_env_variable('SERVICE_PRINCIPAL_ID')
        self.service_principal_password = self.load_env_variable(
            'SERVICE_PRINCIPAL_PASSWORD'
            )
        self.ai_doc_intelligence_service = self.load_env_variable(
            'AI_DOC_INTELLIGENCE_SERVICE'
            )
        self.ai_doc_intelligence_key = self.load_env_variable('AI_DOC_INTELLIGENCE_KEY')
        self.search_service_name = self.load_env_variable('SEARCH_SERVICE_NAME')
        self.aoai_api_base = self.load_env_variable('AOAI_API_BASE')
        self.aoai_api_key = self.load_env_variable('AOAI_API_KEY')
        self.aoai_api_version = self.load_env_variable('AOAI_API_VERSION')
        self.embedding_model_deployment_name = self.load_env_variable(
            'EMBEDDING_MODEL_DEPLOYMENT_NAME')

    def load_env_variable(self, env_var_name: str) -> str:
        value = os.getenv(env_var_name)
        self.env_variables[env_var_name] = value
        return value

    def convert_to_run_config(self, env_name: str) -> RunConfiguration:
        run_config = RunConfiguration()
        env = Environment(env_name)
        run_config.environment = env
        run_config.environment_variables = self.env_variables
        return run_config
