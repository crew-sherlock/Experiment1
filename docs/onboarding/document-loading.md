# Running `aml_pipeline.py` locally

Follow these steps to set up and run the `aml_pipeline.py` script. This script sets up and runs an Azure Machine Learning pipeline that loads documents from Azure Blob Storage, processes them with Azure AI Document Intelligence, chunks the documents, generates embeddings and creates a search index in Azure AI Search.

## Prerequisites

1. **Create a `.env` file**:
   - Create a `.env` file in your project root directory.
   - Populate it with the necessary values as specified in the [`.env.example`](https://github.com/gsk-tech/AIGA/blob/main/config/.env.example) file.

1. **Modify the `.aml_pipeline_config.json` file**:
   - Modify the [`.aml_pipeline_config.json`](https://github.com/gsk-tech/AIGA/blob/main/src/document_loading/aml_pipeline_config.json) file located in the `src/document_loading` folder.

   ```json
   {
    "path_to_script": "<PATH_TO_SCRIPT>",
    "compute_name": "<COMPUTE_CLUSTER_NAME>",
    "vm_size": "<VM_SIZE>",
    "max_nodes": "<MAX_NODES>",
    "experiment_name": "<EXPERIMENT_NAME>",
    "storage_account_name": "<STORAGE_ACCOUNT_NAME>",
    "container_name": "<CONTAINER_NAME>",
    "datastore_name": "<DATASTORE_NAME>",
    "data_path": "<DATA_PATH>",
    "chunking_strategy": "<CHUNKING_STRATEGY>",
    "chunk_size": "<CHUNK_SIZE>",
    "chunk_overlap": "<CHUNK_OVERLAP>",
    "index_name": "<INDEX_NAME>"
   }
   ```

   | Field | Description | Example | Required |
   | --- | --- | --- | --- |
   | `path_to_script` | Path to the step scripts in your repository | `src/document_loading` | Yes |
   | `compute_name` | Name of the compute cluster to use or create | `aml-cluster` | Yes |
   | `vm_size` | Size of the virtual machine | `STANDARD_D2_V2` | Yes |
   | `max_nodes` | Maximum number of nodes in the cluster | `4` | Yes |
   | `experiment_name` | Name of the experiment to create | `document-loading` | Yes |
   | `storage_account_name` | Name of the storage account | `storageaccount` | Yes |
   | `container_name` | Name of the container in the storage account | `container` | Yes |
   | `datastore_name` | Name of the datastore to use or create | `datastore` | Yes |
   | `data_path` | Path to the relevant data within the container | `data/` | Yes |
   | `chunking_strategy` | Strategy for chunking data (headers, characters) | `headers` | Yes |
   | `chunk_size` | Size of each chunk | `1000` | Only if `chunking_strategy` is `characters` |
   | `chunk_overlap` | Overlap between chunks | `100` | Only if `chunking_strategy` is `characters` |
   | `index_name` | Name of the index to be created | `document-index` | Yes |
   | `fields` | Fields to be included in the index | Azure AI Search fields formatted as json, see [documentation](https://learn.microsoft.com/en-us/azure/search/search-how-to-create-search-index?tabs=index-rest#create-an-index) for examples. | No |
   | `vector_search` | Vector search algorithms and profiles | Vector search configuration with algorithms and profiles formatted as json, see [documentation](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-create-index?tabs=config-2024-07-01%2Crest-2024-07-01%2Cpush%2Cportal-check-index#add-a-vector-search-configuration) for examples. | No |
   | `cors_options` | CORS options for the index | CORS options formatted as json, see [documentation](https://learn.microsoft.com/en-us/azure/search/search-how-to-create-search-index?tabs=index-rest#set-corsoptions-for-cross-origin-queries) for examples. | No |
   | `scoring_profiles` | Scoring profiles for the index | Scoring profiles formatted as json, see [documentation](https://learn.microsoft.com/en-us/azure/search/index-add-scoring-profiles#scoring-profile-definition) for examples. | No |

   > **Note:** Make sure that the field which contains the text data/chunk is not sortable, filterable, or facetable. This is because the text data is too large to be processed as a single term. In general, when filtering, sorting, and/or faceting are enabled on a field, it causes the entire field value to be indexed as a single term and causes document upload errors. Please avoid the use of these options for large fields.

1. **Install dependencies**:
   - Run the following command to install the required dependencies:

     ```sh
     poetry install --with aml
     ```

      > **Note:**
      >
      > For ARM processors, if this command is failing due to the `azure-dataprep-rslex` dependency, create a new environment using [conda](https://formulae.brew.sh/cask/anaconda):
      >
      > ```bash
      > conda create -n intel_env
      > conda activate intel_env
      > conda config --env --set subdir osx-64
      > conda install python=3.10
      > ```
      >
      > Or
      >
      > ```bash
      > CONDA_SUBDIR=osx-64 conda create -n intel_env python=3.10
      > conda activate intel_env
      > conda config --env --set subdir osx-64
      > ```
      >
      > Now install the dependencies as described above.

1. **Login to Azure**:
   - Use the Azure CLI to login to your Azure account:

     ```sh
     az login
     ```

## Running the Script

1. **Execute the script**:
   - Run the following command to execute the `aml_pipeline.py` script:

     ```sh
     poetry run python -m src.document_loading.aml_pipeline
     ```

This will run the Azure Machine Learning pipeline as defined in the `aml_pipeline.py` script.
