# Infrastructure Component to Component Access Strategy

Date: 2024-07-29

## Status

Accepted

## Context

As a GenAI Platform Engineer, we would like to standardize the component to component
access plan for GenAI applications. This will help in standardizing the access and will
act as an input for automated infra provisioning.

## Decision

Below are the list of access details that are reviewed and accepted by SCDT D&A
Architecture Team, PSC Platform Team and Code Orange Team. The following access details
would be captured as standard access mechanism during the infra provisioning which will
reduce the discussions on the access provisioning.

| Access To                       | Access From           | Access Method                          | Permission Level                                                                                                                                                             |
|---------------------------------|-----------------------|----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ingestion: ADLS (FND)           | AzureML               | Service Principal (Platform)           | Read                                                                                                                                                                         |
| Ingestion: SQL Server           | AzureML               | Service Principal (Platform)           | Read                                                                                                                                                                         |
| Azure Blob Storage              | AzureML               | Service Principal 1                    | Read and Write                                                                                                                                                               |
| SQL Server (Application)        | AzureML               | Service Principal 1                    | Read and Write                                                                                                                                                               |
| Azure Functions (Event Trigger) | Azure ML              | Managed Identity / Service Principal 1 | Submit                                                                                                                                                                       |
| Azure Translator                | AzureML               | Service Principal 1                    | NA                                                                                                                                                                           |
| Azure Content Safety            | AzureML               | Service Principal 1                    | NA                                                                                                                                                                           |
| Azure Doc Intelligence          | AzureML               | Service Principal 1                    | NA                                                                                                                                                                           |
| LLM Gateway                     | AzureML               | Keys and Gateway                       | Submit                                                                                                                                                                       |
| Azure AI Search                 | AzureML               | Service Principal 1                    | Read and Write                                                                                                                                                               |
| Keyvault                        | AzureML               | Service Principal 1                    | RGContributor + Key Vault Contributor                                                                                                                                        |
| Azure Blob Storage              | Azure AI Search       | Service Principal 1                    | Read and Write                                                                                                                                                               |
| Azure ML Inference Endpoints    | HTTP Request          | AD Token                               | [AzureML Data Scientist](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-authenticate-online-endpoint?view=azureml-api-2&tabs=azure-cli#use-a-built-in-role) |
| All Resources                   | Azure Monitor         | Managed Identity / Service Principal 1 | NA                                                                                                                                                                           |
| Azure Functions (HTTP Trigger)  | Any Resources         | Entra AD Token                         | Submit                                                                                                                                                                       |
| All Resources                   | Application Insights  | Managed Identity / Service Principal 1 |                                                                                                                                                                              |
| Keyvault                        | Github Actions        | Service Principal 2                    | Read and Write                                                                                                                                                               |
| AzureML End Point               | Github Actions        | Service Principal 2                    | [AzureML Data Scientist](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-authenticate-online-endpoint?view=azureml-api-2&tabs=azure-cli#use-a-built-in-role) |
| AzuremL Workspace               | Github Actions        | Service Principal 2                    | AzureML Compute Operator                                                                                                                                                     |
| Azure Web Apps                  | Github Actions        | Service Principal 2                    | Contributor                                                                                                                                                                  |
| AI Search                       | Azure WebApps         | Service Principal 1                    | Search Index Reader / Contributor                                                                                                                                            |
| Azure Functions (HTTP Trigger)  | Azure WebApps         | Managed Identity / Service Principal   | Submit                                                                                                                                                                       |
| LLM Gateway                     | Azure WebApps         | Keys and Gateway                       | Submit                                                                                                                                                                       |
| Azure Translator                | Azure WebApps         | Service Principal 1                    | NA                                                                                                                                                                           |
| Azure Content Safety            | Azure WebApps         | Service Principal 1                    | NA                                                                                                                                                                           |
| Azure Doc Intelligence          | Azure WebApps         | Service Principal 1                    | NA                                                                                                                                                                           |
| Keyvault                        | Azure WebApps         | Managed Identity / Service Principal   | RGContributor + KeyVault Contributor                                                                                                                                         |
| Azure Container Registry        | Github Actions        | Service Principal 2                    | Contributor                                                                                                                                                                  |
| Azure Container Registry        | WebApps               | Service Principal 1                    | Reader                                                                                                                                                                       |
| Azure Container Registry        | AzureML               | Service Principal 1                    | Contributor                                                                                                                                                                  |
| Azure AI Search                 | AzureML + Prompt Flow | API Key                                | AI Search Contributor                                                                                                                                                        |
| ML Registry                     | AzureML               | Managed Identity                       | Contributor                                                                                                                                                                  |
| Azure AI Search Indexing        | AzureML               | Service Principal                      | Search Index Data Contributor                                                                                                                                                |
|                                 |                       |                                        | Connector in promptflow cannot do AD token (ping token) - we are using keys at the moment as temp approach                                                                   |

## Consequences

By standardizing the access method between components, it will ensure all the GenAI
application teams follow a standard access pattern. This will also help in ensuring the
access pattern is predefined in the infrastructure request form and access is
provisioned along with the infra provisioning.
