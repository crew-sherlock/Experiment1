# Template Components

The AIGA Template provides a **working** implementation of a Generative AI workload that can be used as a starting point for new projects. The template is designed to be modular and extensible, allowing developers to easily add new features and components to the end-to-end process.

The primary components of the AIGA Template are:

- [Document Loading](#document-loading) *(real-time and batch)*
- [Inference Flow](#inference-flow)
- [Evaluation Flow](#evaluation-flow)
- [Python Source](#python-source) *(shared code and utilities)*

## Components Overview

### Document Loading

Document Loading is a multistep data orchestration workflow that is responsible for:

- **Loading documents** from Azure Blob Storage
- **Extracting document** structure and contents using Azure AI Document Intelligence or [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
- **Chunking documents** using a built-in configurable chunking strategy
- **Embedding document** chunks using a configurable embedding strategy
- **Storage of document** chunks in an Azure AI Search Index

Document Loading supports real-time and batch scenarios. The real-time scenario uses Azure Event Grid to trigger an Azure Function when a new document is uploaded to Azure Blob Storage. This Azure Function is implemented in Python. The batch scenario uses Azure Machine Learning Pipelines to batch-process large volumes of documents from Azure Blob Storage. This Pipeline is a collection of Python-based [components](https://learn.microsoft.com/en-us/azure/machine-learning/concept-component).

Each of these scenarios will leverage a shared Python module to minimise code duplication and ensure consistency across the different implementations.

This implementation is designed to be modular and extensible, allowing developers to easily add new steps and components to the process.

> Data Ingestion into Azure Storage is out of scope for the AIGA Template. For real-time, the application layer is responsible for uploading documents to Azure Blob Storage. For batch, the central ingestion teams (in Code Orange and PCS) is responsible for ingesting documents into the foundation layer.

**Repository location:** `src/document-loading`

### Inference Flow

The Inference Flow is a chat-based inference pipeline that offers a chat-like experience, using a large language model. It is implemented as a [DAG Flow](https://microsoft.github.io/promptflow/concepts/concept-flows.html#dag-flow) in PromptFlow. The DAG flow is a Directed Acyclic Graph of functions, implemented as PromptFlow [tools](https://microsoft.github.io/promptflow/concepts/concept-tools.html) in Python. AIGA provides a collection of tools (located in the [Python Source](#python-source)) that can be configured via input parameters and replaced with custom implementations as needed by an AIGA Project.

The Inference Flow supports `chat_history`, `chat_input` and `chat_output`. It can be deployed to Azure App Service or as a Managed Online Endpoint in Azure Machine Learning (see [Deployment](../onboarding/deployment.md) for more details).

The Inference Flows sends all traces to Azure Application Insights for monitoring and logging, as well as metrics for groundedness, relevance, and retrieval (metrics that do not require ground truth).

> Note: This flow is renamed for each specific AIGA project to the format `[PROJECT_NAME]_inference`

**Repository location:**

- DAG Flow: `promptflow/inference` (or `promptflow/[PROJECT_NAME]_inference` for a specific project)
- PromptFlow Tools: `src/tools`
- Python Utilities: `src/utils`

AIGA deploys the Inference Flow from the CD workflow, as documented [here](../onboarding/github-actions.md).

### Evaluation Flow

The Evaluation Flow is used to evaluate the quality of the Inference Flow. It runs on the output the chat flow, and computes metrics that can be used to help determine accuracy, semantic similarity, and correctness (metrics that require ground truth). The Evaluation flow will also capture groundedness, relevance, and retrieval.

The Evaluation Flow leverages MLFlow to track experimentation. It is designed to publish each experiment and their respective metrics in [Azure Machine Learning](https://learn.microsoft.com/en-us/azure/machine-learning/concept-mlflow).

> Note: This flow is renamed for each specific AIGA project to the format `[PROJECT_NAME]_evaluation`

**Repository location:**

- DAG Flow: `promptflow/evaluation` (or `promptflow/[PROJECT_NAME]_evaluation` for a specific project)
- PromptFlow Tools: `src/tools/evaluation`

AIGA triggers the evaluation flow from the CI workflow, as documented [here](../onboarding/github-actions.md).

### Python Source

A collection of Python modules, including PromptFlow Tools, utilities, and scripts that are common across the project. This includes, but is not limited to:

- Document Loading: `src/document-loading`
- PromptFlow Tools: `src/tools`
- Utilities: `src/utils`
- Scripts: `src/scripts`

The code in this directory is linted using [flake8](https://flake8.pycqa.org/en/latest/) and supported by a suite of unit tests that are run as part of the PR workflow.

- Unit Tests: `tests`

#### `generate-golden-data` script

`generate-golden-data` is a executable Python script that automates the creation of a golden dataset for training and evaluation. The script is designed to be run from the command line and generates a set of input and output pairs from a list of documents using a language model. The generated dataset is exported to a JSON Lines file, which in turn can be used by the Evaluation Flow.

> **Note:** There is a requirement for business partners to review and iteratively improve the golden dataset. We are currently designing the user flow to facilitate this process.

It is intended that this script will be run manually by the data scientist as required and therefore is not included in the CI/CD workflow.
