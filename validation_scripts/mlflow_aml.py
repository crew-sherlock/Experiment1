import os

from azure.ai.ml import MLClient
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv
from azure.ai.ml.entities import Data as AMLData
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes as AMLAssetTypes
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
# registering a dataset
local_data_path = 'data/bert-paper-qna-1-line.jsonl'
name = "validation_resources"
flow_path = "promptflow/inference"

aml_dataset = AMLData(
    path=local_data_path,
    type=AMLAssetTypes.URI_FILE,
    name=name,
)

ml_client.data.create_or_update(aml_dataset)
print("asset validated")
model = Model(
        name=name,
        path=flow_path,
        stage=None
    )
ml_client.models.create_or_update(model)
