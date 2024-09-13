# GitHub Secrets

AIGA leverages Azure Key Vault to store secrets and keys used in the application. The
Key Vault is a pre-requisite for AIGA and should be populated with the necessary secrets
and keys ahead of time.

## Required Secrets

The following secrets are required to be provisioned in the Key Vault:

| Secret Name                           | Description                                            | Team to provision |
|---------------------------------------|--------------------------------------------------------|-------------------|
| AI-DOC-INTELLIGENCE-SERVICE           | The base URL for the Azure AI Document Intelligence    | CO                |
| AI-DOC-INTELLIGENCE-KEY               | The API key for the Azure AI Document Intelligence     | CO                |
| AML-AZURE-SUBSCRIPTION-ID             | The Azure subscription ID where AML workspace is       | CO                |
| AML-WORKSPACE-NAME                    | The name of the Azure Machine Learning workspace       | CO                |
| AML-RESOURCE-GROUP-NAME               | The name of the Azure resource group where AML is      | CO                |
| AOAI-API-BASE                         | The base URL for the Azure OpenAI Service              | CO                |
| AOAI-API-KEY                          | The API key for the Azure OpenAI Service               | CO                |
| AOAI-API-VERSION                      | The version of the Azure OpenAI Service                | CO                |
| APPLICATIONINSIGHTS-CONNECTION-STRING | The connection string for Azure Application Insights   | PSC               |
| AZ-SQL-SERVER                         | The name of the SQL server in azure                    | CO                |
| AZ-SQL-DATABASE                       | The name of the SQL database in azure                  | CO                |
| AZURE-CLIENT-ID                       | The client Id of the Service Principal                 | Manual (Hosting)  |
| AZURE-CLIENT-SECRET                   | The Secret of the Service Principal                    | Manual (Hosting)  |
| AZURE_TENANT_ID                       | The Azure tenant ID                                    | Manual (Hosting)  |
| DOCKER-IMAGE-REGISTRY                 | The name of the container registry                     | PSC               |
| DOCKER-IMAGE-REGISTRY-SECRET          | The access key for the container registry              | PSC               |
| EMBEDDING-MODEL-DEPLOYMENT-NAME       | The name of the Azure OpenAI deployment for embeddings | CO                |
| PROMPT-FLOW-KONG-API-GATEWAY-ENDPOINT | The token generation API base URL for the Kong Gateway (pink federated generation) | CO |
| PROMPT-FLOW-KONG-CLIENT-ID            | The Secret for the  Kong Gateway                       | CO                |
| PROMPT-FLOW-KONG-CLIENT-SECRET        | The Client Id of the Pink Federated service            | CO                |
| SEARCH-SERVICE-NAME                   | The base URL for the Azure AI Search Service           | CO                |
| WA-AZURE-SUBSCRIPTION-ID              | The name of the web app service subscription ID        | PSC               |
| WA-RESOURCE-GROUP-NAME                | The name of the web app service resource group         | PSC               |
| WA-NAME                               | The name of the web app service                        | PSC               |

> **Note**: Secrets loaded from Azure Key Vault will supersede any GitHub Actions
> variables and secrets with the same name.

## Integrating with GitHub Actions

AIGA provides a custom GitHub Action (`load-secrets`) to load secrets from Azure Key
Vault into a GitHub Actions workflow.

```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4.1.5
  - name: Azure login
    uses: azure/login@v2.1.1
    with:
      creds: ${{ secrets.AZURE_CREDENTIALS }}
  - name: Load Secrets from Azure Key Vault
    uses: ./.github/actions/load-secrets
    with:
      azureKeyVaultName: ${{ vars.KEY_VAULT_NAME }}
```

The following GitHub Action secrets are required:

- `AZURE_CREDENTIALS`: The Azure service principal credentials.
  See [Creating a Service Principal](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure#use-the-azure-login-action-with-a-service-principal-secret)
  for details on creating a service principal and creating the secret.

The following [GitHub Variables](./github-variables.md) are required:

- `KEY_VAULT_NAME`: The name of the Azure Key Vault

After integrating the `load-secrets` action into the GitHub Actions workflow, **all**
secrets from the given Azure Key Vault will be available for use in the workflow (
replacing '-' with '_'):

```yaml
  - name: Print Secrets
    run: |
      echo "AOAI_API_BASE=$AOAI_API_BASE"
      echo "AOAI_API_KEY=$AOAI_API_KEY"
```

## Managing Multiple Environments

AIGA
uses [GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/managing-environments-for-deployment)
to supports multiple deployment environments (e.g., `dev`, `test`, `prod`).

When creating a new environment, it is important to ensure that the necessary secrets
and variables are provisioned for the environment. For more details, see:

- [Environment secrets](https://docs.github.com/en/actions/deployment/targeting-different-environments/managing-environments-for-deployment#environment-secrets)
- [Environment variables](https://docs.github.com/en/actions/deployment/targeting-different-environments/managing-environments-for-deployment#environment-variables)
