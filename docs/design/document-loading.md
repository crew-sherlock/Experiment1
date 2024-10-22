# Data processing and document loading

In order to implement a RAG system, we need to have a data processing pipeline in place. This pipeline will be responsible for ingesting the relevant documents, chunking them, enriching them with metadata, creating the necessary embeddings, and storing them in an index. Moreover, we should have the capability to process large volumes of documents in batch mode, as well as in real-time.

## Ingestion

The requirements for the ingestion component are as follows:

1. Authentication: The system should use the service principal to authenticate to Azure Blob Storage and Azure AI Document Intelligence.
1. Format: The system should be able to ingest documents in various formats, such as PDF, Word, text files and PowerPoint (these can be converted to PDF as part of the pipeline).*
1. Volume: The system should be able to ingest large volumes of documents.
1. Source: The system should be able to ingest documents from Azure Blob Storage.
1. Metadata: The system should be able to extract metadata from the documents e.g. last updated date. It should also fetch other related metadata from SQL database or Databricks e.g. when the document was first ingested, the original language, type.*
1. Filtering: The system should be able to filter out documents that are not relevant for the RAG system based on metadata.
1. Digitization: The system should be able to convert PDF into json and extract the structure of the documents based on document headers and sections using Azure AI Document Intelligence (this is being implemented in US#89845) as well as using a custom tool developed by the team which uses OpenAI's GPT model to extract the structure of the documents.* The system should be able to switch between the two tools based on configuration.

## Processing

The requirements for the processing component are as follows:

1. Chunking: The system should be able to chunk the documents into smaller units. The strategy for chunking should be configurable and include options such as sections (based on headers) and based on a specific length of text (the overlap between chunks should be configurable as well).
1. Enrichment: The system should be able to enrich the documents with metadata from SQL db/Databricks as well as captioning, summaries, key words.* An example of this is where we want to enrich each deviation chunk (e.g. root cause of deviation) with the summary of the deviation to improve the search results.
1. Embeddings: The system should be able to vectorise documents chunks, or any other relevant information from the document, into embeddings using pre-trained embedding models. The strategy for creating embeddings should be configurable and use integrated vectorisation within Azure AI Search. It should allow for use of Azure OpenAI embedding models as well as custom embedding models.*
1. Indexing: The system should be able to store the documents and their embeddings in an index, specifically Azure AI Search. The schema index should include the fields from metadata and the properties of each field e.g. searchable, filterable, retrievable etc. Schema should be codified in a  configuration file, index should be rebuilt when the schema is updated.
1. Authentication: The system should use the service principal to authenticate to Azure AI Search and token-based authentication to the LLM Gateway.
1. Index Versioning: The system should be able to rebuild the index when the blob is updated - this includes when a document is added, removed or updated. This feature ensures that the index is always up-to-date with the source data.
1. Traceability: The system should be able to register the processed documents list and the methods used for processing them. Moreover, it should keep track of any unsuccessfully processed documents and the reasons for failure. This is for traceability and reproducibility purposes.
1. Evaluation: Once the index is rebuilt, it should trigger the evaluation pipeline and use the golden dataset to evaluate the quality of the embeddings.
1. Extensibility: The system should be able to easily add new steps and components to the process. This includes the ability to add new skills to the pipeline e.g. translation, summarisation, key word extraction.*
1. Consistency Across Pipelines: Whenever possible, the tools should be shared between the document loading pipelines and the PromptFlow flow. For example, if data is embedded in the document loading pipelines, the same embedding function should be used when querying the index to ensure consistent results and avoid discrepancies.

## Runtime

The requirements for the runtime component are as follows:

1. Real-time: The system should be triggered to process documents in real-time when they are uploaded to Azure Blob Storage.
1. Batch: The system should be able to process large volumes of documents in batch mode.

The real-time scenario uses Azure Event Grid to trigger an Azure Function when a new document is uploaded to Azure Blob Storage. This Azure Function is implemented in Python. The batch scenario uses Azure Machine Learning Pipelines to batch-process large volumes of documents from Azure Blob Storage. The pipeline uses the same python code as much as possible.

### Real-Time and Batch Processing Triggers

1. Real-time: The system should be triggered to process documents in real-time when they are uploaded to Azure Blob Storage.
1. Batch: The system will have a manual trigger, a scheduled trigger, and an event-based trigger. The manual trigger will be used for ad-hoc processing of documents. The scheduled trigger will be used for periodic processing of documents. The event-based trigger will be used when the queue of documents to be processed reaches a certain threshold or a bulk upload of documents is detected.*

## Minimal Viable Product (MVP)

MVP will NOT include (marked with * above):

- Support for Word, text and PowerPoint files (only PDFs will be supported).
- Metadata enrichment from SQL/Databricks.
- Custom tool for digitization.
- Enrichment with captioning, summaries, key words.
- Support for custom embedding models.
- Pluggable translation skill with Azure AI Translator.
- Event-based trigger for batch processing.

## Additional Resources

The following AML pipeline code can be used as a reference:
