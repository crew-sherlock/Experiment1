import os

from promptflow.azure import PFClient as PFClientAzure
from azure.ai.ml import MLClient
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv
from llmops.common.common import resolve_env_vars
# Retrieve the IDs and secret to use with ServicePrincipalCredentials

load_dotenv()

tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
resource_group_name = os.environ["RESOURCE_GROUP_NAME"]
workspace_name = os.environ["WORKSPACE_NAME"]

credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id,
                                    client_secret=client_secret)

ml_client = MLClient(
            subscription_id=subscription_id,
            resource_group_name=resource_group_name,
            workspace_name=workspace_name,
            credential=credential,
        )

pf = PFClientAzure(
            credential=credential,
            subscription_id=subscription_id,
            workspace_name=workspace_name,
            resource_group_name=resource_group_name
        )

data_path = "data/data.jsonl"
env_vars = resolve_env_vars("promptflow")
flow_path = "promptflow/validation"
runtime_resources = ({"instance_type": "Standard_E4ds_v4"})
common_params = {
                "flow": flow_path,
                "data": data_path,
                "environment_variables": env_vars,
                "resources": runtime_resources,
                "stream": True,
                "raise_on_error": True,
                        }
run = pf.run(**common_params)
