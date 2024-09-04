# Experiment and Evaluate Locally

This guide will walk you through running a full E2E experiment and evaluation flow locally, from registering a dataset, through executing the promptflow runs to evaluating the results. The same evaluation flow runs automatically when you push a commit to the dev or main branches. However, you can also run the it locally to test your changes before pushing them.

## Setup environment

### Environment variables

Create a copy of the file [.env.example](https://github.com/gsk-tech/AIGA/blob/main/config/.env.example) as a .env file in the root.
Fill all the params in the .env file.

To run the environment, you can either use VSCode and the dev container supplied [in here](https://github.com/gsk-tech/AIGA/tree/main/.devcontainer)
or
install the environment [using poetry](https://python-poetry.org/docs/#installation) by running:

```bash
make setup
```

When the command finish successfully, you can perform:

```bash
poetry env list
```

and see the created environment:
![venv](assets/env.png)

To activate your environment, use one of the following:

- for Bash or Zsh (Linux, macOS, Windows Git Bash):

```bash
source .venv/bin/activate
```

- for PowerShell (Windows):

```powershell
.\.venv\Scripts\Activate.ps1
```

- for Command Prompt (Windows):

```bash
.venv\Scripts\activate.bat
```

Register the environment:

```bash
poetry run python -c "from dotenv import load_dotenv; load_dotenv()"
```

### Login to Azure

Login to Azure CLI:

```bash
az login --use-device-code
```

### Local or Remote Execution

Choose the execution mode by setting the EXECUTION_TYPE variable for the LLMOPS package.
The file [config.py](https://github.com/gsk-tech/AIGA/blob/main/llmops/config.py), located in the 'llmops' directory, has a single variable called EXECUTION_TYPE that can be set to either 'LOCAL' or 'AZURE'. The default value is 'AZURE'.

### Set trace configuration

Set the trace configuration for the experiment. The trace configuration is used to log the experiment execution and evaluation results.

```bash
pf config set trace.destination=azureml://subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP_NAME/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE_NAME
```

## Prepare the experiment

The next steps read appropriate field values from experiment.yaml or experiment.[env].yaml that are located in the promptflow directory that is indicated by the USE_CASE_BASE_PATH environment variable (e.g. promptflow directory).

Read the [Experiment Configuration Guide](../onboarding/experiment-configuration-guide.md) for more information on how to structure the YAML file for configuring an experiment and prepare the experiment configuration as per your requirements.
Set the base path for the directory where the experiment definitions are located. for example see the folder 'promptflow' in the root of the project.

```bash
export USE_CASE_BASE_PATH=<USE_CASE_BASE_PATH>
```

> Note that Prompt Flow connections should pre-exist and AML automatic (serverless) runtime is used by default.

## Register a dataset

Register experiment data asset in Azure ML as Data Asset.
This is a one-time setup that reads appropriate field values from experiment.yaml or experiment.[env].yaml.
Use the following command to register the dataset:

```bash
poetry run python -m llmops.common.register_data_asset \
            --subscription_id $AZURE_SUBSCRIPTION_ID \
            --base_path $USE_CASE_BASE_PATH \
            --env_name dev
```

## Execute Standard flow

Execute the standard flow for a scenario that is described in the experiment.yaml or experiment.[env].yaml. A new RUN will be executed for each unique variant combination (keeping default variant id for other nodes) and this will generate reports for each RUN as well as a consolidated one. The experiment data is loaded from Azure ML data asset that was loaded in the previous step.

Use the following command to execute the flows:

```bash

export BUILD_ID=<A_UNIQUE_IDENTIFIER>
poetry run python -m llmops.common.prompt_pipeline \
            --subscription_id $AZURE_SUBSCRIPTION_ID \
            --build_id $BUILD_ID \
            --base_path $USE_CASE_BASE_PATH \
            --env_name dev \
            --output_file run_id.txt
```

> Note: this command might take some time to run.

This will create a csv file in the folder `reports/` this csv file can be shared with SME's to collect feedback

## Evaluate the results

Executes all Evaluation flows available for a scenario that is described in the experiment.yaml or experiment.[env].yaml. This uses each RUN ID as input to run evaluation against. The experiment data and the evaluation data are loaded from Azure ML data assets that were loaded in the previous steps. The evaluation data is loaded from Azure ML data asset that was loaded in the previous step.

Use the following command to execute the evaluation:

```bash
# Read the run_id from the file
RUN_NAME=$(<run_id.txt)

poetry run python -m llmops.common.prompt_eval \
            --subscription_id $AZURE_SUBSCRIPTION_ID \
            --build_id $BUILD_ID \
            --base_path $USE_CASE_BASE_PATH \
            --env_name dev \
            --run_id "$RUN_NAME"
```

## See the results

Reports in HTML and in CSV are available in the reports directory under the root of execution directory.
