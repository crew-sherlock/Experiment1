# LLMOps

The AIGA Template leverages [llmops-promptflow-template](https://github.com/microsoft/llmops-promptflow-template/tree/main) to support Azure Machine Learning (ML) as a platform for LLMOps, and Github workflows as a platform to operationalize Flows. LLMOps with Prompt flow provides automation of the following:

- Experimentation by executing flows
- Evaluation of prompts along with their variants
- Registration of prompt flow 'flows'
- Deployment of prompt flow 'flows'
- Generation of Docker Image
- Deployment to Azure Web Apps and Azure ML compute
- A/B deployments
- Role based access control (RBAC) permissions to deployment system managed id to key vault and Azure ML workspace
- Endpoint testing
- Report generation

## Configuration

For detailed instructions on how the Github Workflows were configured, see [How to setup the repo with Github Workflows](https://github.com/microsoft/llmops-promptflow-template/blob/main/docs/github_workflows_how_to_setup.md).

## Continuous Integration (CI) pipeline

The Github CI workflow contains the following steps:

### Run Prompts in Flow

- Upload bulk run dataset
- Bulk run prompt flow based on dataset
- Bulk run each prompt variant
- Evaluate Results

### Upload ground test dataset

- Evaluation of the bulk run result using single evaluation flow

## Continuous Deployment (CD) pipeline

The Github CD workflow contains the following steps:

### Register Prompt flow LLM App

- Register Prompt flow as a Model in Azure Machine Learning Model Registry

### Deploy and Test LLM App

- Deploy the Flow as a model to the development environment Azure ML Compute endpoint
- Assign RBAC permissions to the newly deployed endpoint to Key Vault and Azure ML workspace
- Test the model/promptflow realtime endpoint

### Run post production deployment evaluation

- Upload the sampled production log dataset
- Execute the evaluation flow on the production log dataset
- Generate the evaluation report

## Deployment configuration

Both the CI and CD workflows expect the variables `RESOURCE_GROUP_NAME`, `WORKSPACE_NAME` and `KEY_VAULT_NAME`. These variables should contain the values of the Azure resources in the dev environment.

The rest of the workflow configurations will be read from the `experiment.yaml` file and from the `config/deployment_config.json` file for the deployment.

Before running the deployment workflows, you need to make changes to `config/deployment_config.json`:

- Update the `ENDPOINT_NAME` and `CURRENT_DEPLOYMENT_NAME` if you want to deploy to Azure Machine Learning compute
- Or update the `CONNECTION_NAMES`, `REGISTRY_NAME`, `APP_PLAN_NAME`, `WEB_APP_NAME`, `WEB_APP_RG_NAME`, `WEB_APP_SKU`, and `USER_MANAGED_ID`if you want to deploy to Azure Web App.

### Update deployment_config.json in config folder

Modify the configuration values in the `deployment_config.json` file for each environment. These are required for deploying Prompt flows in Azure ML. Ensure the values for `ENDPOINT_NAME` and `CURRENT_DEPLOYMENT_NAME` are changed before pushing the changes to remote repository.

- `ENV_NAME`: This indicates the environment name, referring to the "development" or "production" or any other environment where the prompt will be deployed and used in real-world scenarios.
- `TEST_FILE_PATH`: The value represents the file path containing sample input used for testing the deployed model.
- `ENDPOINT_NAME`: The value represents the name or identifier of the deployed endpoint for the prompt flow.
- `ENDPOINT_DESC`: It provides a description of the endpoint. It describes the purpose of the endpoint, which is to serve a prompt flow online.
- `DEPLOYMENT_DESC`: It provides a description of the deployment itself.
- `PRIOR_DEPLOYMENT_NAME`: The name of prior deployment. Used during A/B deployment. The value is "" if there is only a single deployment. Refer to CURRENT_DEPLOYMENT_NAME property for the first deployment.
- `PRIOR_DEPLOYMENT_TRAFFIC_ALLOCATION`:  The traffic allocation of prior deployment. Used during A/B deployment. The value is "" if there is only a single deployment. Refer to CURRENT_DEPLOYMENT_TRAFFIC_ALLOCATION property for the first deployment.
- `CURRENT_DEPLOYMENT_NAME`: The name of current deployment.
- `CURRENT_DEPLOYMENT_TRAFFIC_ALLOCATION`: The traffic allocation of current deployment. A value of 100 indicates that all traffic is directed to this deployment.
- `DEPLOYMENT_VM_SIZE`: This parameter specifies the size or configuration of the virtual machine instances used for the deployment.
- `DEPLOYMENT_INSTANCE_COUNT`:This parameter specifies the number of instances (virtual machines) that should be deployed for this particular configuration.
- `ENVIRONMENT_VARIABLES`: This parameter represents a set of environment variables that can be passed to the deployment.
