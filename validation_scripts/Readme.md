# How to validate that the resources and accesses have been provisioned properly

After your resources have been provisioned, make sure that you fill your .env file and run the following in order ot validate that everything has been provisioned properly, with the right permissions

In AIGA folder, run the following commands (with the service principal)

## ML flow and Promptflow via AML (for registry)

- Create the connection
- Checks that we can use promptflow from AML to run an experiment
- Checks that we can use AML to register data assets
- Checks that we can use AML to register a flow
- Checks that we can use PF on AML to run an experiment

```bash
poetry run python -m validation_scripts.pf_aml
poetry run python -m validation_scripts.mlflow_aml
```

Once running the above, you might encounter this warning

```bash
[promptflow][WARNING] - The trace Cosmos DB for current workspace/project is not ready yet, your traces might not be logged and stored properly.
To enable it, please run `pf config set trace.destination=azureml://subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-or-project-name>`, prompt flow will help to get everything ready.
```

Run the above `pf config set trace.destination=azureml://subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-or-project-name>` command to setup the tracing in AML. This is a one time operation.

## AI Search as Vector Database

- creates an index, update

```bash
poetry run python -m validation_scripts.aisearch
```

## Deployment from ACR to webapp

In order to make sure that we can push the docker image to the ACR and then to the webapp, just run the following command

```bash
./llmops/common/scripts/az_webapp_deploy.sh
```
