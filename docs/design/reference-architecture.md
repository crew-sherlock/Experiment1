# Reference Architecture

## Context

An AIGA reference architecture is a blueprint for the design and implementation of a Gen AI product.
It is a set of Azure services and components and their interactions that are used to build a Gen AI product.
The reference architecture is a starting point for designing and implementing a Gen AI product and is pre-approved by the Architecture team to facilitate the acceleration of Gen AI product development through the review boards.

The reference architecture for a Gen AI product is based on the [Microsoft baseline architecture for GenAI products](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-openai-e2e-chat) and extends it to generalise it for any Gen AI product.

## Architecture Description

The following are two reference architectures for a Gen AI product that differ only in the serving layer. One uses Azure Machine Learning and the other uses Azure App Service:

![Image of Reference Architecture serving from AML](assets/AIGA%20Reference%20Architecture%20-%20AML%20Serving.svg)

![Image of Reference Architecture serving from App Service](assets/AIGA%20Reference%20Architecture%20-%20Webapp%20Serving.svg)

### Components

- **ADLS Azure Storage and Azure SQL:** Used for input data including doc-Store (ADLS), doc-store metadata (ADLS) and job metadata (SQL) originating from data sources through the data pipeline.

- **Azure Storage (Persistence):** Used as an AML Datastore for storing datasets and *optionally* for caching of intermediate artifacts.

- **Azure Machine Learning Workspace:** Manage the machine learning lifecycle of building, training, and deploying of machine learning models.

- **Azure Storage (AML Registry):** Azure Machine Learning registry for storing and versioning models, workflows and artifacts.

- **Azure Machine Learning Compute Instance:** Used for training, experimenting, running batch or trigger based compute tasks and optionally serving the model.

- ***[OPTIONAL]* Azure AI Services:** Provides various AI capabilities, including Content Safety, Translator, Document Intelligence

- ***[OPTIONAL]* Function (Skills):** Azure Functions used to execute agent based skills.

- **LLM Gateway:** Gateway for accessing large language models.

- **Azure AI Search:** AI-powered search service.

- **Azure App Service WebApp:** Front-end application interacting with users and optionally serving the model. The consumption layer is out of scope for this reference architecture, may contain additional layers except the App Service WebApp, and is considered an interface of the reference architecture by its own CI ID.

- **Azure Container Registry:** A stand alone registry for Docker container images used in all services, including the Azure ML registry.

- **Azure Monitor:** Monitoring service for collecting and analysing telemetry data.

- **Azure Application Insights:** Provides monitoring and diagnostic information for applications.

- **Azure Key Vault:** Manages all secrets, encryption keys, and certificates of the environment.

### Data Flow

- Interface: Data is ingested into ADLS Azure Storage (doc-store and doc-store metadata) and Azure SQL (job metadata) from data sources through the data pipeline.

1. Data is either batch or trigger-based processed in Azure Machine Learning Compute Instance.

1. *[OPTIONAL]* Data is transformed using Azure AI Services.

1. *[OPTIONAL]* Data is processed using Azure Functions (Skills).

1. Data is vectorised using Azure OpenAI service through LLM Gateway.

1. *[OPTIONAL]* Vectorised data is cached in Azure Storage (Persistence).

1. Vectorised data is indexed in Azure AI Search.

1. Data is served through the Serving Layer that searches the indexed data, leverages Azure AI and Open AI services, and optionally executes agent based skills.

1. Data is consumed by the Application running on Azure App Service WebApp.

## Multi-Environment Deployment

The following diagram shows the deployment of the reference architecture across different environments (dev, test, prod)

![Image of Multiple Environment Deployment](assets/AIGA%20Multiple%20environment.svg)

### Shared Services

- **Azure Container Registry:** A single Azure Container Registry is provisioned with AIGA reference architecture, and configuration is updated to use it for the Azure Machine Learning workspaces in all stages (Dev, Test, Prod).

- **GitHub Actions:** GitHub Actions is used for CI/CD across the different stages (Dev, Test, Prod).
