from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv


load_dotenv('python.env')


tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]

storage_account_name = os.environ['STORAGE_ACCOUNT_NAME']
container_name = os.environ['CONTAINER_NAME']
folder_path = os.environ['FOLDER_PATH']

credential = ClientSecretCredential(tenant_id, client_id, client_secret)


blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net",
    credential=credential
)


def upload_blob_data(blob_service_client: BlobServiceClient, container_name: str):
    blob_client = blob_service_client.get_blob_client(container=container_name,
                                                      blob="data/sample-blob.txt")
    data = b"Sample data for blob"

    # Upload the blob data - default blob type is BlockBlob
    blob_client.upload_blob(data, blob_type="BlockBlob")


try:
    print(container_name)
    # blob_service_client.create_container(container_name)
    upload_blob_data(blob_service_client=blob_service_client,
                     container_name=container_name)
    print("data uploaded")
    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blobs(name_starts_with=folder_path)
    blobs_list = list(blobs)
    if blobs_list:
        print(f"Successfully accessed the folder: {folder_path}")
        print(f"Number of blobs in the folder: {len(blobs_list)}")
    else:
        print(f"Folder '{folder_path}' exists but is empty or not accessible.")

except Exception as e:
    print(f"Failed to access the folder: {folder_path}")
    print(f"Error: {str(e)}")
