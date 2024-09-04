import os
from azure.ai.ml import MLClient
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv
from azure.ai.ml.entities import AzureOpenAIConnection, ApiKeyConfiguration
# Retrieve the IDs and secret to use with ServicePrincipalCredentials

load_dotenv()

tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
resource_group_name = os.environ["RESOURCE_GROUP_NAME"]
workspace_name = os.environ["WORKSPACE_NAME"]
target = os.environ["AOAI_API_BASE"]
api_key = os.environ["AOAI_API_KEY"]

resource_id = f"""/subscriptions/{subscription_id}/resourceGroups/
{resource_group_name}/providers/Microsoft.MachineLearningServices/
workspaces/{workspace_name}"""

credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id,
                                    client_secret=client_secret)

ml_client = MLClient(
            subscription_id=subscription_id,
            resource_group_name=resource_group_name,
            workspace_name=workspace_name,
            credential=credential,
        )

name = "aoai"

wps_connection = AzureOpenAIConnection(
    name=name,
    azure_endpoint=target,
    credentials=ApiKeyConfiguration(key=api_key),
    api_version="2023-05-15"
)
ml_client.connections.create_or_update(wps_connection)
