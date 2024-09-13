from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys import KeyClient
from azure.keyvault.certificates import CertificateClient
from dotenv import load_dotenv
import os


load_dotenv('python.env')

tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]

subscription_id = os.environ["AML_AZURE_SUBSCRIPTION_ID"]
resource_group_name = os.environ["AML_RESOURCE_GROUP_NAME"]
workspace_name = os.environ["AML_WORKSPACE_NAME"]


storage_account_name = os.environ['STORAGE_ACCOUNT_NAME']
container_name = os.environ['CONTAINER_NAME']
folder_path = os.environ['FOLDER_PATH']
key_vault_name = os.getenv("KEY_VAULT_NAME")

key_vault_url = f"https://{key_vault_name}.vault.azure.net/"

credential = ClientSecretCredential(tenant_id, client_id, client_secret)

secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
key_client = KeyClient(vault_url=key_vault_url, credential=credential)
certificate_client = CertificateClient(vault_url=key_vault_url, credential=credential)

try:

    secrets = secret_client.list_properties_of_secrets()
    secrets_list = list(secrets)
    print(f"Successfully accessed the Key Vault: {key_vault_name}")
    print(f"Number of secrets: {len(secrets_list)}")
    keys = key_client.list_properties_of_keys()
    keys_list = list(keys)
    print(f"Number of keys: {len(keys_list)}")

    certificates = certificate_client.list_properties_of_certificates()
    certificates_list = list(certificates)
    print(f"Number of certificates: {len(certificates_list)}")

except Exception as e:
    print(f"Failed to access the Key Vault: {key_vault_name}")
    print(f"Error: {str(e)}")
