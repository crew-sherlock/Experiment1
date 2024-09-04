# Experiment YAML Structure Guide

This guide explains how to structure the YAML file for configuring an experiment.
Each section of the YAML file is described with the necessary details to help you build it from scratch.
A [sample YAML](https://github.com/gsk-tech/AIGA/blob/main/promptflow/experiment.yaml) file is provided as part of the template for your reference.

## Experiment Name

```yaml
name: <experiment_name>
```

### Description

- **name**: Defines the experiment name which serves two purposes:
  1. It is used as the experiment name for Azure ML jobs, unless overridden by the `flow_name` parameter below.
  1. Is is used as the RUN name for the experiment.
  1. It becomes the model name when registered in Azure ML.

## Flow Definition

```yaml
flow: <flow_name>
```

### Description

- **flow**: Specifies the standard flow of the experiment.
  - If not provided, the experiment name will be used as the flow name.
  - If provided, it should be the path to the folder containing the Prompt Flow files, including `flow.dag.yaml`.

#### Notes

- It is recommended to keep all flow folders (standard and evaluators) within a common "flows" folder.
- If using this structure, you can reference the flow by its folder name, and the system will automatically check the "flows" directory (i.e., "flows/<flow_name>").

## Datasets

```yaml
datasets:
- name: <dataset_0_name>
  source: azureml:<dataset_name>:<dataset_version>
  mappings:
    <flow_input_name>: "${data.<column_name>}"
- name: <dataset_1_name>
  source: ./path/to/data.jsonl
  description: "dataset description"
  mappings:
    <flow_input_name>: "${data.<column_name>}"
```

### Description

- **datasets**: Lists the datasets used for the standard flow in this experiment. Each dataset listed will be used to run the standard flow; it can also be used to run one or more of the evaluation flows (see below).
  - **name**: A unique name for referencing the dataset.
  - **source**: Either a reference to an existing dataset in Azure ML (`azureml:$name:$version`) or a path to a local dataset.
  - **description**: An optional description for the dataset when uploaded to Azure ML. Only required if the source is a local path.
  - **mappings**: Maps the inputs of the Prompt Flow flow to the dataset columns, using the syntax `${data.<column_name>}`.

#### Note

- If the dataset is local, it will be uploaded to Azure ML.

## Connections

```yaml
connections:
- name: <connection_0_name>
  connection_type: <connection_type>
  api_base: <api_base>
  api_version: <api_version>
  api_key: ${api_key}
  api_type: <api_type>

- name: <connection_1_name>
  connection_type: <connection_type>
  api_base: <api_base>
  api_version: <api_version>
  api_key: ${api_key}
  api_type: <api_type>
```

### Description

- **connections**: Defines the connections used in the experiment, typically to authenticate API calls made by the Prompt Flow flows.
  - **name**: A unique name for referencing the connection.
  - **connection_type**: The type of connection. The supported type is `AzureOpenAIConnection`.
  - **api_base**: The endpoint of the API.
  - **api_version**: The version of the API.
  - **api_key**: The API key used for authentication.
  - **api_type**: Specifies the type of API, which determines the required authentication.

## Evaluators

```yaml
evaluators:
- name: <evaluator_0_name>
  datasets:
  - name: <dataset_0_name> # Note that "dataset_0_name" was already defined in the "datasets" block
    mappings:
      flow_input_0_name: "${data.<column_name>}"
      flow_input_1_name: "${run.outputs.<output_name>}"
- name: <evaluator_1_name>
  datasets:
  - name: <dataset_x_name> # Note that "dataset_x_name" is a new dataset
    source: azureml:<dataset_name>:<dataset_version> # or ./path/to/data.jsonl
    reference: <dataset_0_name> # Note that new datasets in the evaluation block must reference an already existing dataset
    mappings:
      flow_input_0_name: "${data.<column_name>}"
      flow_input_1_name: "${run.outputs.<output_name>}"
```

### Description

- **evaluators**: Lists the evaluators, each representing a Prompt Flow flow that requires a dataset. The dataset must already be defined above (meaning it was used to run the standard flow) OR it must contain a reference to a dataset from above. The result of the standard flow with the matching dataset is used as input to the evaluation flow.

  - **name**: A unique name for referencing the evaluator.
  - **flow**: Path to the evaluator flow folder. The system checks the "flows" directory  (i.e., "flows/<flow_name>") for the evaluator flow.
  - **datasets**: The dataset used for the evaluator, which must:
    - Match one of the datasets listed in the `datasets` section or,
    - Include a `source` and `reference` parameter that matches one of the previously defined datasets.
    - **name**: name of the dataset used. Must match the unique name of one of the datasets listed above, OR must have "source" and "reference" parameter and the "reference" parameter must match the unique name of one of the datasets listed above.
    - **source**: reference to an existing dataset in Azure ML <azureml:$name:$version> or path to local dataset. Optional, only required when the "name" parameter doesn't match any of the datasets listed above
    - **description**: description used for the dataset when uploaded to Azure ML. Optional, only used when "source" is set to a path of a local file.
    - **reference**: name of the reference dataset. Must match the unique name of one of the datasets listed above.  Optional, only required when the "name" parameter doesn't match any of the datasets listed above.
  - **mappings**: Maps the evaluator flow inputs to dataset columns or outputs of the standard run, using `${data.<column_name>}` or `${run.outputs.<output_name>}`.

## Runtime

```yaml
runtime: <runtime_name>
```

### Description

- **runtime**: Specifies the Prompt Flow runtime to be used. If not specified, an automatic runtime with serverless compute is used.
