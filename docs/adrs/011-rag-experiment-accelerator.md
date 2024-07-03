# 11. Use the RAG experiment accelerator

Date: 2024-06-28

## Status

Proposed

## Context

The [RAG experiment accelerator](https://github.com/microsoft/rag-experiment-accelerator) is a repository that contains a set of pre-built components which enable for running standardised, retrieval-augmented generation (RAG) experiments using Azure OpenAI and Cognitive Search. The goal is to make it easier and faster to run experiments and evaluations of search queries and quality of response from OpenAI. It enables the user to:

- test the performance of different Search and OpenAI related hyperparameters,
- compare the effectiveness of various search strategies,
- fine-tune and optimize parameters,
- find the best combination of hyperparameters,
- generate detailed reports and visualizations from experiment results.

This aligns with the 'experimentation' component of AIGA. The goal of this ADR is to evaluate the feasibility of reusing the RAG experiment accelerator for AIGA and determine what modifications are needed to make it fit for purpose.

### Comparison of the RAG experiment accelerator features and their mapping to AIGA requirements

|Index| Feature | Description | Mapping to AIGA requirements | Proposed action | To do | Effort** |
|---| --- | --- | --- | --- | --- | --- |
|1| Technology stack | The accelerator uses Azure OpenAI, Cognitive Search, MLFlow and Azure Machine Learning (AML). | This aligns with the technology stack agreed upon in [architecture](../design/aiga-infrastructure.md). | No action, `infra` folder can be removed. | No anticipated changes needed - some effort to integrate with deployed services. | Low |
|2| Prompt Flow | The accelerator contains artefacts for running experiments on Prompt Flow. However, this is not up-to-date due to recent Prompt Flow changes. | We do not want to use Prompt Flow and have agreed on using AML. | Remove `promptflow` code. | No anticipated changes needed. | Low |
|3| Experiment setup | You can define and configure experiments by specifying a range of search engine parameters, search types, query sets, and evaluation metrics. | This would standardize nd automate the experimentation process at GSK which currently consists of a data scientist manually fine-tuning parameters and rerunning the evaluation. | Copy `rag-experiment-accelerator` code and other `azureml` folder as is. | We need to determine if the parameters available in the accelerator are sufficient or if we need to add custom parameters. | Low |
|4| Rich search indexing | It creates multiple search indexes based on hyperparameter configurations available in the config file. | This would standardise and automate the experimentation process at GSK by allowing for a more comprehensive generation and evaluation of diverse search indexes. | Copy `azureml/index.py` and dependencies as is. | We need to determine if the search indexes created by the accelerator are sufficient or if we need to broaden the diversity of search indexes. | Low |
|5| Document loading | The accelerator supports loading documents using Document Intelligence. These are loaded from a code repository. | Document Intelligence aligns with the technology stack agreed upon in [agreed architecture](../design/aiga-infrastructure.md). However, the documents would have to be ingested from the GSK Data Lake. | Modify `rag-experiment-accelerator/ingest_data` component to fit requirements. | We would need to develop the ingestion pipeline to source documents from the GSK Data Lake rather than the code repository. | High |
|6| Custom Document Intelligence loader | It has a custom Document Intelligence loader pre-built for initial pre-processing/cleaning of documents. | ??? | Copy `rag-experiment-accelerator/doc_loader` as is. | We need to determine if the GSK data requires any custom pre-processing/cleaning. | Low |
|7| Query generation | The tool can generate a variety of diverse and customizable query sets, which can be tailored for specific experimentation needs as `.json`. Note: this is only available locally. | This isn't currently standard at GSK, the query sets are generated and evaluated manually but this could potentially accelerate generating the 'golden dataset'. The 'golden dataset' is currently a `.csv`. | Copy `02_qa_generation.py` and dependencies as it. | We need to determine if query generation is something we want to automate or if we want to keep the current manual process of generating and evaluating query sets. | Low |
|8| Metrics and evaluation |  It supports end-to-end metrics comparing the generated answers (actual) against the ground-truth answers (expected), including distance-based, cosine and semantic similarity metrics. It also includes component-based metrics to assess retrieval and generation performance using LLMs as judges, such as context recall or answer relevance, as well as retrieval metrics to assess search results (e.g. MAP@k). | This aligns with the current experimentation evaluation at GSK. However, this doesn't include groundedness which is an important metric to include for the team. | Modify `rag-experiment-accelerator/evaluation` as needed. | The metrics are not sufficient for the GSK team e.g. lack of groundedness as a measure - this would have to be added. | Medium |
|9| Report generation/visualisations | The accelerator automates the process of report generation, complete with visualizations captured within AML that make it easy to analyze and share experiment findings.| This aligns with the current experimentation tooling at GSK. However, the reports are further converted into csv and stored in a storage account. | Modify artefact generation as needed. | We need to add the functionality to convert the reports into csv and store them in a storage account, if needed. | Medium |
|10| Multi-lingual | The tool uses language analyzers within Azure AI Search for linguistic support on individual languages and specialized (language-agnostic) analyzers for user-defined patterns on search indexes. | This aligns with requirement for support of multiple languages within the data. | Copy `rag-experiment-accelerator/nlp/language_evaluator.py` as is. | The current [architecture](../design/aiga-infrastructure.md) also includes the use of Translator. We need to determine how this will be integrated with the accelerator. | Low |
|11| Configuration | The accelerator uses a config.json file to specify the parameters for an experiment (e.g. chunk size, overlap size, search types). | We have not made a decision so far on how to specify the configuration. | Copy `rag-experiment-accelerator/config` as is. | We would need to adapt this to the chosen method or align with current process. | Low |
|12| Hosting | The accelerator can be run locally or from AML. | This is in line with how experiments are currently run for GenAI solutions. | Copy current code as is. Local scripts are in the root folder e.g. `01_index.py`,`02_qa_generation.py` etc. and AML pipeline can be found in the `azureml` folder. | No anticipated changes needed. | Low |
|13| Logging | The logging is done with the generic 'logging' python package. | We have agreed upon using OpenTelemetry for logging in the [observability ADR](../adrs/007-observability-prompt-flow.md). | Modify code throughout including `rag-experiment-accelerator/utils/logging.py`. | Logging with OpenTelemetry will have to be added. | High |
|14| Monitoring | The solution uses App Insights, Log Analytics. What data does it collect??? | ??? | Modify the code throughout. | We anticipate that data will have to filtered so that not all logs and traces are sent to App Insights - this needs to be aligned with GDPR and protect PII. | Medium |
|15| Security | The accelerator uses Key Vault for secret management. | This is in line with the agreed [architecture](../design/aiga-infrastructure.md). | Copy `rag-experiment-accelerator/config` and `rag-experiment-accelerator/utils/auth.py` as is. | No changes needed - further secrets will be added if necessary. | Low |
|16| Authentication | The solution uses DefaultAzureCredential for authentication. It uses .env or Key Vault values. | This allows us to use any identity to authenticate into Azure. | Copy `rag-experiment-accelerator/config` and `rag-experiment-accelerator/utils/auth.py` as is. | No changes needed - identities have to be configured. | Low |
|17| Documentation | The accelerator has some documentation on configuration and usage. | Documentation on configuration will be required as well as further documentation on usage e.g. prompt fine tuning, setup. | Bring useful parts of `docs`. | More documentation should be generated to include experimentation guidance and setup as well as prompt fine tuning. | Medium |

** Effort is rated as low, medium or high based on the anticipated changes needed to adapt the accelerator to fit the requirements of AIGA. Any work that has to be done on top to build AIGA specific features is not included in this effort rating.

The image below maps the planned architecture of AIGA to the RAG experiment accelerator components:

![RAG experiment accelerator components](./assets/RAG-experiment-accelerator-mapping.drawio.svg)

Open questions:

- Are there other use cases that we want to include in AIGA that the RAG experiment accelerator needs to be adapted for?
- Does the accelerator use integrated vectorisation within Azure AI Search or custom vectorisation?

## Decision

We will reuse the RAG experiment accelerator for AIGA. The accelerator will be modified to fit the requirements of AIGA and any customizations needed will be implemented - major changes include integrating the document loading with GSK Data Lake, adding groundedness as metrics, adapting the logging to use OpenTelemetry and making sure the filtered data is sent to App Insights. This will significantly reduce the time and effort required to implement the experimentation component of AIGA.

## Consequences

Each component of the accelerator will have to be investigated in depth and adapted to fit our requirements for the AIGA Template.
