# 11. Use the RAG experiment accelerator

Date: 2024-06-28

## Status

Accepted

## Context

The [RAG experiment accelerator](https://github.com/microsoft/rag-experiment-accelerator) is a repository that contains a set of pre-built components which enable for running standardised, retrieval-augmented generation (RAG) experiments using Azure OpenAI and Cognitive Search. The goal is to make it easier and faster to run experiments and evaluations of search queries and quality of response from OpenAI. It enables the user to:

- test the performance of different Search and OpenAI related hyperparameters,
- compare the effectiveness of various search strategies,
- fine-tune and optimize parameters,
- find the best combination of hyperparameters,
- generate detailed reports and visualizations from experiment results.

This aligns with the 'experimentation' component of AIGA. The goal of this ADR is to evaluate the feasibility of reusing the RAG experiment accelerator and to determine what modifications are needed to make it fit for purpose.

### Comparison of the RAG experiment accelerator features and their mapping to AIGA requirements

|Index| Feature | Description | Mapping to AIGA requirements | Proposed action | To do | Effort** |
|---| --- | --- | --- | --- | --- | --- |
|1| Technology stack | The accelerator uses Azure OpenAI, Cognitive Search, MLFlow and Azure Machine Learning (AML). | This aligns with the technology stack agreed upon in [architecture](../design/reference-architecture.md). | No action, `infra` folder can be ignored. | No anticipated changes needed - some effort to integrate with deployed services. | Low |
|2| Prompt Flow | The accelerator contains artefacts for running experiments on Prompt Flow. However, this is not up-to-date due to recent Prompt Flow changes. | We do not want to use Prompt Flow and have agreed on using AML. | Ignore `promptflow` code. | No anticipated changes needed. | Low |
|3| Experiment setup | You can define and configure experiments by specifying a range of search engine parameters, search types, query sets, and evaluation metrics. | This would standardize nd automate the experimentation process at the organisation which currently consists of a data scientist manually fine-tuning parameters and rerunning the evaluation. | Use `rag-experiment-accelerator` and `azureml` folders' code as is. | We need to determine if the parameters available in the accelerator are sufficient or if we need to add custom parameters. | Low |
|4| Rich search indexing | It creates multiple search indexes based on hyperparameter configurations available in the config file. | This would standardise and automate the experimentation process by allowing for a more comprehensive generation and evaluation of diverse search indexes. | Use `azureml/index.py` and dependencies as is. | We need to determine if the search indexes created by the accelerator are sufficient or if we need to broaden the diversity of search indexes. | Low |
|5| Document loading | The accelerator supports loading documents using Document Intelligence. These are loaded from a code repository. | Document Intelligence aligns with the technology stack agreed upon in [agreed architecture](../design/reference-architecture.md). However, the documents would have to be ingested from a Data Lake. | Determine if we need to modify or add to `rag-experiment-accelerator/ingest_data` component to fit requirements. | We would need to develop the ingestion pipeline to source documents from the Data Lake rather than the code repository. | High |
|6| Custom Document Intelligence loader | It has a custom Document Intelligence loader pre-built for initial pre-processing/cleaning of documents. | ??? | Use `rag-experiment-accelerator/doc_loader` as is. | We need to determine if the data requires any custom pre-processing/cleaning. | Low |
|7| Query generation | The tool can generate a variety of diverse and customizable query sets, which can be tailored for specific experimentation needs as `.json`. Note: this is only available locally. | This isn't currently standard, the query sets are generated and evaluated manually but this could potentially accelerate generating the 'golden dataset'. The 'golden dataset' is currently a `.csv`. | Use `02_qa_generation.py` and dependencies as it, where applicable. | We need to determine if query generation is something we want to recommend or if we want to keep the current manual process of generating and evaluating query sets. | Low |
|8| Metrics and evaluation |  It supports end-to-end metrics comparing the generated answers (actual) against the ground-truth answers (expected), including distance-based, cosine and semantic similarity metrics. It also includes component-based metrics to assess retrieval and generation performance using LLMs as judges, such as context recall or answer relevance, as well as retrieval metrics to assess search results (e.g. MAP@k). | This aligns with the current experimentation evaluation. However, this doesn't include groundedness which is an important metric to include for the team. | Add metrics to `rag-experiment-accelerator/evaluation` as needed. | The metrics are not sufficient e.g. lack of groundedness as a measure - this would have to be added. | Medium |
|9| Report generation/visualisations | The accelerator automates the process of report generation, complete with visualizations captured within AML that make it easy to analyze and share experiment findings. They are stored as `.csv` in AML. | This aligns with the current experimentation tooling. | No anticipated changes needed. | No action needed. | Low |
|10| Multi-lingual | The tool uses language analyzers within Azure AI Search for linguistic support on individual languages and specialized (language-agnostic) analyzers for user-defined patterns on search indexes. | This aligns with requirement for support of multiple languages within the data. | Use `rag-experiment-accelerator/nlp/language_evaluator.py` as is. | The current [architecture](../design/reference-architecture.md) also includes the use of Translator. We need to determine how this will be integrated with the accelerator. | Low |
|11| Configuration | The accelerator uses a config.json file to specify the parameters for an experiment (e.g. chunk size, overlap size, search types). | We have not made a decision so far on how to specify the configuration. | Use `rag-experiment-accelerator/config` as is. | Make sure that the config format received from the experimentation phase will be compatible with the AIGA Starter.  | Low |
|12| Hosting | The accelerator can be run locally or from AML. | This is in line with how experiments are currently run for GenAI solutions. | Use current code as is. Local scripts are in the root folder e.g. `01_index.py`,`02_qa_generation.py` etc. and AML pipeline can be found in the `azureml` folder. | No anticipated changes needed. | Low |
|13| Logging | The logging is done with the generic 'logging' python package. | We have agreed upon using OpenTelemetry for logging in the [observability ADR](../adrs/007-observability-prompt-flow.md). However, the logs from the experimentation phase will not necessarily be collected in App Insights. | No anticipated changes needed. | If we want to add more verbose logging, this will have to be added. | Low |
|14| Monitoring | The solution uses App Insights, Log Analytics. However, as of now, it does not collect detailed logging. | We have not agreed on the extent of logs collected in the experimentation phase. | No anticipated changes needed. | We need to make sure that if using App Insights, the data send is aligned with GDPR to protect PII. | Low |
|15| Security | The accelerator uses Key Vault for secret management. | This is in line with the agreed [architecture](../design/reference-architecture.md). | Use `rag-experiment-accelerator/config` and `rag-experiment-accelerator/utils/auth.py` as is. | No changes needed. | Low |
|16| Authentication | The solution uses DefaultAzureCredential for authentication. It uses .env or Key Vault values. | This allows us to use any identity to authenticate into Azure. | Use `rag-experiment-accelerator/config` and `rag-experiment-accelerator/utils/auth.py` as is. | No changes needed - identities have to be configured. | Low |
|17| Documentation | The accelerator has some documentation on configuration and usage. | Documentation on configuration will be required as well as further documentation on usage e.g. setup within organisational context, moving from experimentation to prompt tuning and deployment phase, integrating with AIGA Started. | Bring useful parts of `docs`. | More documentation should be generated to include experimentation guidance and setup as well as prompt fine tuning. | Medium |

** Effort is rated as low, medium or high based on the anticipated changes needed to adapt the accelerator to fit the requirements of AIGA. Any work that has to be done on top to build AIGA specific features is not included in this effort rating.

The image below maps the planned architecture of AIGA to the RAG experiment accelerator components:

![RAG experiment accelerator components](./assets/RAG-experiment-accelerator-mapping.drawio.svg)

Open questions:

- Are there other use cases that we want to include in AIGA that the RAG experiment accelerator needs to be adapted for?
- Does the accelerator use integrated vectorisation within Azure AI Search or custom vectorisation?

## Decision

We recommend the use of the RAG experiment accelerator for experimentation.

Where possible, the configuration file will be compatible with the RAG implementation in the AIGA Template. This will ease the transition from experimentation to inference flows.

The accelerator will be modified to fit the requirements of AIGA and any customizations needed will be implemented - major changes include integrating the document loading with Data Lake, adding groundedness as metrics, adapting the logging and App Insights integration. Where possible, these modifications will be directly contributed to the RAG Experiment Accelerator open source project.

This will significantly reduce the time and effort required to implement the experimentation component of AIGA.

## Consequences

The experimentation phase will not be part of the AIGA Template repository but rather guidance around how to use the RAG experiment accelerator open source project and how to use the configuration file generated by the accelerator within AIGA's RAG template. This can be as little as instructions on how to fork the open source project, guidance on how to integrate it within the environment and use the configuration file within AIGA or as much as forking the open source project as part of AIGA orchestration, including it as a submodule within the repository and providing an automated way to take the produced configuration file and use it within AIGA.

Because external repositories cannot be forked to GitHub Enterprise, the RAG experiment accelerator will be cloned to a separate repository (separate from the AIGA Project instance). This will be one of the optional components of the AIGA Starter that the user can choose to include in their project depending on their requirements.

This will require the team to make sure the AIGA Template is compatible with the configuration file generated by the accelerator.

Any gaps identified in the accelerator will have to be addressed by the team and directly contributed to the open source project.
