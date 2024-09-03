# 1. Document processing pipeline CI/CD

Date: 2024-08-28

## Status

Accepted

## Context

The AML document processing pipeline handles large volumes of documents in both batch and real-time modes. A reliable and efficient processing pipeline is key to the success of the RAG system.

Therefore, it is important to support the pipeline with CI/CD to automatically test codebase changes and ensure new updates do mot disrupt existing functionality. This approach allows for quick and consistent improvements to the document processing pipeline without compromising its integrity.

## Decision

### Should it be part of the existing CI/CD?

| Option | Pros/Cons |
|-|-|
| Integrating with Existing CI/CD | **Troubleshooting** (con): Debugging issues would become harder with a single CI which handles multiple workflows.  |
| Creating a Separate CI/CD | **Specific** (pro): A dedicated pipeline can be tailored specifically for the AML document processing needs. |
| | **Isolation** (pro): Issues in the AML pipeline won't affect other parts of the system, and vice versa. |

Decision:

- As the data and document processing pipeline is independent of other jobs/workflows, it can be triggered separately to the CI which will minimise noise in the run log and make debugging and troubleshooting easier.
- Note: In addition, there are other independent workflows in the CI that could also benefit from being separated out, e.g. `deploy-docs`.

> Create an `aml-ci-workflow` with jobs to build, test and validate the document processing pipeline code. This would have its own trigger defined, including branch and path rules.
> Create a `aml-cd-workflow` folder with an `action.yml` file with deployment steps necessary for the data and document processing.
> Create a `deploy-docs` workflow and move this out of CI as it should be in its own workflow with its own trigger.
> Rename `ci-workflow` to be `promptflow-ci-workflow` so that the naming and purpose is clear.

### What should the triggers be?

| Pipeline | Triggers |
|-|-|
| CI Pipeline | **Code changes**: When there are commits or pull requests to the `main` branch, which is what currently happens. |
| | **Manual runs**: The ability to manually trigger the CI workflow using changes from a specific branch for dev/test purposes. This is current behaviour. |
| CD Pipeline | **Successful CI Builds**: When the CI completes (on `main`), the CD pipeline is triggered. |
| | **Manual runs**: The ability to manually trigger the CI workflow using changes from a specific branch for dev/test purposes. This is current behaviour. |

In addition to the CI/CD triggers, we could also add additional path filters to the workflows.

GitHub allows you to specify path filters to trigger builds only when certain files or directories are modified, for example:

```yaml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - src/*
    exclude:
      - docs/*
```

In this example:

- The pipeline triggers on changes to the `main` branch.
- It includes changes in the `src` directory.
- It excludes changes in the `docs` directory.

We can implement filters to ensure the CI/CD components of the document loading pipeline are triggered only when there are code changes in the relevant folders.

This approach would prevent unnecessary extensions to the workflow runtime, where there is no additional benefit. However, this will only be effective if the document loading pipeline code is sufficiently isolated.

- **Manual**: We have found during development that it is useful to be able to manually trigger a workflow for dev/test purposes.
- **Automatic**: Our current pattern is that the CI runs when there are merges to `main`, and the CD runs when the CI has completed successfully (on `main`).

> Re-use existing CI/CD triggers, however add branch and path rules to the workflow, so that it is only run when there are code changes to that part of the codebase.
> Update the `promptflow-ci-workflow` to run when the `aml-ci-workflow` is triggered (but not vice versa). This is because if there are changes in how documents are ingested, it's important to ensure these changes do not affect the results of the metrics by running the `prompt_eval` script.

## What functionality will the CI/CD do?

The data processing and document loading pipeline consists of three components, **ingestion**, **processing** and **runtime**. Further details of those components can be found in [document-loading.md](../design/document-loading.md).

The table below shows how these components can be covered by CI/CD:

| Component | Feature | CI | CD |
|-|-|-|-|
| Ingestion | Authentication | Automate the testing of authentication mechanisms to ensure the service principal can access Azure Blob Storage and Azure AI Document Intelligence |  Deploy updates to authentication configurations securely and consistently. |
| | Format | Implement automated tests to verify the system's ability to ingest and convert various document formats (initially just PDF). | Deploy new format handling capabilities and conversion tools as they are developed. |
| | Volume handling | Test the system’s performance and scalability with large volumes of documents using automated load testing. |  Deploy optimizations and scaling configurations to handle increased document volumes. |
| | Source integration | Automate tests to ensure the system can reliably ingest documents from Azure Blob Storage. | Deploy updates to source integration logic and configurations. |
| | Metadata extraction* | Implement automated tests to verify metadata extraction from documents and integration with SQL databases or Databricks. | Deploy updates to metadata extraction logic and configurations. |
| | Filtering | Automate tests to ensure the filtering logic correctly identifies and excludes irrelevant documents based on metadata. | Deploy updates to filtering criteria and logic. |
| | Digitization | Implement automated tests to verify the conversion of PDFs to JSON and the extraction of document structure using both Azure AI Document Intelligence and the custom tool. | Deploy updates to digitization tools and configurations, allowing for seamless switching between tools based on configuration. |
| Processing | Chunking | Automate tests to verify the chunking strategy, ensuring it correctly divides documents based on headers or specific text lengths, including configurable overlaps. | Deploy updates to chunking strategies and configurations seamlessly. |
| | Enrichment* | Implement automated tests to verify the enrichment process, ensuring metadata, captions, summaries, and keywords are correctly added from SQL databases or Databricks. | Deploy updates to enrichment logic and configurations. |
| | Embeddings* | Automate tests to ensure the system correctly vectorizes document chunks using pre-trained embedding models, including Azure OpenAI and custom models. | Deploy updates to embedding strategies and configurations. |
| | Indexing | Implement automated tests to verify the indexing process, ensuring documents and their embeddings are correctly stored in Azure AI Search with the appropriate schema. | Deploy updates to the index schema and configurations, ensuring the index is rebuilt when the schema is updated. |
| | Authentication | Automate tests to verify authentication mechanisms using service principals for Azure AI Search and token-based authentication for the LLM Gateway. | Deploy updates to authentication configurations securely. |
| | Index Versioning | Implement automated tests to ensure the index is correctly rebuilt when documents are added, removed, or updated. | Deploy updates to index versioning logic and configurations. |
| | Traceability | Automate tests to verify the registration of processed documents and tracking of unsuccessfully processed documents, including reasons for failure. | Deploy updates to traceability logic and configurations. |
| | Evaluation | Implement automated tests to verify the evaluation pipeline, ensuring it correctly uses the golden dataset to evaluate the quality of embeddings. | Deploy updates to the evaluation pipeline and configurations. |
| | Extensibility* | Automate tests to ensure new steps and components can be easily added to the process, including new skills like translation, summarization, and keyword extraction. | Deploy updates to the pipeline to incorporate new steps and components. |
| | Consistency Across Pipelines | Implement automated tests to ensure tools are shared consistently between document loading pipelines and the PromptFlow flow. | Deploy updates to ensure consistent use of embedding functions and other tools across pipelines. |
| Runtime | Real-time processing | Automate tests to verify that Azure Event Grid correctly triggers the Azure Function when a new document is uploaded to Azure Blob Storage. | Deploy updates to the Azure Function code and configurations, ensuring seamless real-time processing. |
| | Batch processing* | Implement automated tests to verify the batch processing logic using Azure Machine Learning Pipelines, ensuring it can handle large volumes of documents. | Deploy updates to the batch processing pipeline and configurations. |
| | Shared python code* | Automate tests to ensure the Python code used in both real-time and batch scenarios is functioning correctly and consistently. | Deploy updates to the shared Python code, ensuring changes are reflected in both real-time and batch processing scenarios. |
| | Trigger mechanisms | Implement automated tests to verify the integration between Azure Event Grid and Azure Functions, ensuring reliable triggering mechanisms. | Deploy updates to the trigger configurations and ensure they are correctly integrated with the processing logic. |

Note: MVP will NOT include those marked with an asterisk (*) above.

## Consequences

In summary, we will:

> Create an `aml-ci-workflow` with jobs to build, test and validate the document processing pipeline code. This would have its own trigger defined, including branch and path rules.
> Create a `aml-cd-workflow` folder with an `action.yml` file with deployment steps necessary for the data and document processing.
> Create a `deploy-docs` workflow and move this out of CI as it should be in its own workflow with its own trigger.
> Rename `ci-workflow` to be `promptflow-ci-workflow` so that the naming and purpose is clear.
> Re-use existing CI/CD triggers, however add branch and path rules to the workflow, so that it is only run when there are code changes to that part of the codebase.
> Update the `promptflow-ci-workflow` to run when the `aml-ci-workflow` is triggered (but not vice versa). This is because if there are changes in how documents are ingested, it's important to ensure these changes do not affect the results of the metrics by running the `prompt_eval` script.

As a consequence, there could be increased activity from triggering CI/CD workflows due to pull requests, merges, or development. This could cause a bottleneck  if:

1. **Agents are limited**: If the number of available agents is insufficient to handle the increased workload, it can cause delays.
2. **Concurrent workflow limitations**: If the system cannot run multiple workflows concurrently, it can create a queue, slowing down the overall process.

To mitigate this, we may need to:

- **Scale up agents**: Ensuring there are enough agents to handle peak loads.
- **Optimise workflow triggers**: Fine-tuning when and how workflows are triggered to avoid unnecessary runs. We would be applying this mitigation in our approach.
- **Prioritising critical workflows**: Setting priorities for different workflows to ensure critical ones are not delayed, e.g. merges to `main` take precedence over `dev`.
