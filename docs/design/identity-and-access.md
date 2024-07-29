# Identity and Access

| Identity | Type | Description | Created By | Owned By |
| -------- | ---- | ----------- | ---------- | -------- |
| [GenAI DevKit](#genai-devkit) | Service Principal | Service Principal with access to resources within the GenAI DevKit | Code Orange | AIGA Project |
| [Endpoint Principal](#endpoint-principal) | Managed Identity (System) | System Assigned Managed Identity associated with the Azure ML managed endpoint | LLMOps | AIGA Project |

## GenAI DevKit

This Service Principal is created alongside the Code Orange GenAI DevKit. It is granted high-level access to the resources within the GenAI DevKit and is predominantly used the AIGA Project's GitHub Actions workflows.

### Azure Resources

| Role | Required Actions | Scope | Justification |
| ---- | ---------------- | ----- | ------------- |
| [AzureML Data Scientist](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/ai-machine-learning#azureml-data-scientist) | Microsoft.MachineLearningServices/workspaces/\*/\* |  Azure Machine Learning workspace | To create data assets, register experiments, execute and read prompt flows, deploy to endpoints etc. |
| [RBAC Admin](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/general#role-based-access-control-administrator) | Microsoft.Authorization/roleAssignments/write |  Azure Machine Learning workspace | To grant access to Endpoint Principals created by LLMOps. |
| RGAdmin | Microsoft.KeyVault/vaults/accessPolicies/write | Resource Group | To grant access to Endpoint Principals created by LLMOps. |

### Additional Access

- **Secret** (get, list) on the environment's Azure Key Vault

## Endpoint Principal

This System Assigned Managed Identity is configured alongside the Azure ML managed endpoint deployment.

### Azure Resources

| Role | Required Actions | Scope | Justification |
| ---- | ---------------- | ----- | ------------- |
| Azure Machine Learning Workspace Connection Secrets Reader | Microsoft.MachineLearningServices/workspaces/connections/listsecrets/action | Azure Machine Learning workspace | To access workspace's default secret store, including workspace connections, from the PromptFlow runtime. |

See additional details regarding the Endpoint Principal [here](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-online-endpoint-with-secret-injection?view=azureml-api-2&tabs=sai#create-an-endpoint).

### Additional Access

- **Secret** (get, list) on the environment's Azure Key Vault
