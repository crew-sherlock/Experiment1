from azure.identity import ClientSecretCredential
from azure.ai.ml import MLClient
from dotenv import load_dotenv
import os


load_dotenv()

tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]

subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
resource_group = os.environ["RESOURCE_GROUP_NAME"]
workspace_name = os.environ["WORKSPACE_NAME"]


credential = ClientSecretCredential(tenant_id, client_id, client_secret)

ml_client = MLClient(
    credential=credential,
    subscription_id=subscription_id,
    resource_group_name=resource_group,
    workspace_name=workspace_name
)


try:

    workspace = ml_client.workspaces.get(workspace_name)
    print(f"Successfully accessed the workspace: {workspace_name}")
    print(f"Workspace Location: {workspace.location}")
except Exception as e:
    print(f"Failed to access the workspace: {workspace_name}")
    print(f"Error: {str(e)}")
