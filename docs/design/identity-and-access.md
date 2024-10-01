# Identity and Access

| Identity                                  | Type                      | Description                                                                    | Created By  | Owned By     |
|-------------------------------------------|---------------------------|--------------------------------------------------------------------------------|-------------|--------------|
| [GenAI DevKit](#genai-devkit)             | Service Principal         | Service Principal with access to resources within the GenAI DevKit             | Code Orange | AIGA Project |
| [Endpoint Principal](#endpoint-principal) | Managed Identity (System) | System Assigned Managed Identity associated with the Azure ML managed endpoint | LLMOps      | AIGA Project |

## GenAI DevKit

This Service Principal is created with the resource group (once the CIID is created) and
is provided to the Code Orange GenAI DevKit. It is granted high-level access to the
resources within the GenAI DevKit and is predominantly used the AIGA Project's GitHub
Actions workflows.

### Azure Resources

| Role                                                                                                                                                  | Required Actions                                       | Scope                            | Justification                                                                                        |
|-------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|----------------------------------|------------------------------------------------------------------------------------------------------|
| [AzureML Data Scientist](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/ai-machine-learning#azureml-data-scientist) | Microsoft.MachineLearningServices/workspaces/\*/\*     | Azure Machine Learning workspace | To create data assets, register experiments, execute and read prompt flows, deploy to endpoints etc. |
| [RBAC Admin](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/general#role-based-access-control-administrator)        | Microsoft.Authorization/roleAssignments/write          | Azure Machine Learning workspace | To grant access to Endpoint Principals created by LLMOps.                                            |
| RGAdmin (GSK Custom Role)                                                                                                                             | Microsoft.KeyVault/vaults/accessPolicies/write         | Resource Group                   | To create an access policy in Azure Key Vault.                                                       |
| [AcrPush](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/containers#acrpush)                                        | Microsoft.ContainerRegistry/registries/push/write      | Azure Container Registry         | To push container images to the registry.                                                            |
| [Website Contributor](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/web-and-mobile#website-contributor)            | Microsoft.Web/sites/*                                  | Azure App Service                | To update deployment configuration for the Web App.                                                  |

### Additional Access

- **Secret** (get, list) on the environment's Azure Key Vault

## Endpoint Principal

This System Assigned Managed Identity is configured alongside the Azure ML managed
endpoint deployment.

### Azure Resources

| Role                                                       | Required Actions                                                            | Scope                            | Justification                                                                                             |
|------------------------------------------------------------|-----------------------------------------------------------------------------|----------------------------------|-----------------------------------------------------------------------------------------------------------|
| Azure Machine Learning Workspace Connection Secrets Reader | Microsoft.MachineLearningServices/workspaces/connections/listsecrets/action | Azure Machine Learning workspace | To access workspace's default secret store, including workspace connections, from the PromptFlow runtime. |

See additional details regarding the Endpoint
Principal [here](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-online-endpoint-with-secret-injection?view=azureml-api-2&tabs=sai#create-an-endpoint).

### Additional Access

- **Secret** (get, list) on the environment's Azure Key Vault

### AIGA Azure resources required permissions

This document is to describe the resources we have been defining and using so far with
managed identity, service principal and AD token.
Each resource is used by one or more resources and requires a specific permission in
order to work in Azure.

| Access To                    | Access From                    | Access Method                        | Permission Level (In Azure)                                                                                                                                                  |
|------------------------------|--------------------------------|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ingestion: SQL Server        | AzureML                        | Service Principal                    | Read and Write                                                                                                                                                               |
| SQL Server (Application)     | AzureML                        | Service Principal                    | Read and Write                                                                                                                                                               |
| Azure AI Search              | AzureML                        | Service Principal                    | AI Search Contributor                                                                                                                                                        |
| Azure AI Search Indexing     | AzureML                        | Service Principal                    | Search Index Data Contributor                                                                                                                                                |
| Keyvault                     | AzureML                        | Service Principal                    | RGContributor + Key Vault Contributor                                                                                                                                        |
| All Resources                | Azure Monitor                  | Managed Identity / Service Principal | NA                                                                                                                                                                           |
| All Resources                | Application Insights           | Managed Identity / Service Principal |                                                                                                                                                                              |
| Azure ML Inference Endpoints | HTTP Request                   | AD Token                             | [AzureML Data Scientist](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-authenticate-online-endpoint?view=azureml-api-2&tabs=azure-cli#use-a-built-in-role) |
| AzureML End Point            | Github Actions                 | Service Principal                    | [AzureML Data Scientist](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-authenticate-online-endpoint?view=azureml-api-2&tabs=azure-cli#use-a-built-in-role) |
| AzureML Workspace            | Github Actions                 | Service Principal                    | AzureML Compute Operator                                                                                                                                                     |
| Azure Web Apps               | Github Actions                 | Service Principal                    | Contributor                                                                                                                                                                  |
| AI Search                    | Azure WebApps                  | Service Principal                    | Search Index Reader / Contributor                                                                                                                                            |
| Keyvault                     | Azure WebApps                  | Managed Identity / Service Principal | RGContributor + Key Vault Contributor                                                                                                                                        |
| Azure Container Registry     | Github Actions                 | Service Principal                    | Contributor                                                                                                                                                                  |
| Azure Container Registry     | WebApp and Webapp service plan | Service Principal                    | Reader                                                                                                                                                                       |
| Azure Container Registry     | AzureML                        | Service Principal                    | Contributor                                                                                                                                                                  |
| Azure AI Search              | AzureML + Prompt Flow          | API Key                              | AI Search Contributor                                                                                                                                                        |
| ML Registry                  | AzureML                        | Managed Identity                     | Contributor                                                                                                                                                                  |
