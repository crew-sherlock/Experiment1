# 12. Flow Deployment Options

Date: 2024-07-03

## Status

Accepted

## Context

The deployable artifact for a Prompt flow is a container image. `pf` can be used to build an OCI-compliant container image that can be deployed to many platforms, including Azure Machine Learning, Azure AI Studio, App Service, and Kubernetes.

```bash
pf flow build --source <path-to-your-flow-folder> --output <your-output-dir> --format docker
```

Without knowing the specific non-functional requirements of each project, it is difficult to recommend a preferred deployment option. The decision should be based on requirements such as cost, scalability, availability, networking, and existing skills.

The purpose of this ADR is to document the most commonly available deployment options in Azure and decide which options the AIGA Template will support out-of-the-box.

It is important to consider the [LLMOps Prompt Flow Template repository](./008-llmops-promptflow-template.md) as this will form the basis for the AIGA Template, and already provides support for many deployment options.

### Further Resources

- [Deploy a flow](https://microsoft.github.io/promptflow/how-to-guides/deploy-a-flow/index.html)
- [Deploy a managed endpoint in Azure Machine Learning](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/how-to-deploy-for-real-time-inference)
- [Deploy a flow in Azure AI Studio](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/flow-deploy)

## Decision

The AIGA Project will produce an OCI-compliant container image that will be published to Azure Container Registry. This will be the responsibility of the Continuous Integration pipeline, and will be based on the [ci_dev_workflow](https://github.com/microsoft/llmops-promptflow-template/blob/main/.github/workflows/chat_with_pdf_ci_dev_workflow.yml) and [gen_docker_image.sh](https://github.com/microsoft/llmops-promptflow-template/blob/main/llmops/common/scripts/gen_docker_image.sh) script provided in the LLMOps Prompt Flow Template.

Leveraging this container image, the AIGA Template will support the following deployment options out-of-the-box:

- **Managed endpoint in Azure Machine Learning** - Azure Machine Learning can be used to serve a flow as a managed online endpoint for real-time inference. Deployment to Azure Machine Learning will be based on LLMOps [provision_endpoint.py](https://github.com/microsoft/llmops-promptflow-template/blob/main/llmops/common/deployment/provision_endpoint.py)
- **Azure App Service** - Azure App Service is an HTTP-based service for hosting web applications, REST APIs, and mobile back ends. Deployment to Azure App Service will be based on Prompt Flow's [deploy.sh](https://github.com/microsoft/promptflow/blob/main/examples/tutorials/flow-deploy/azure-app-service/deploy.sh) and LLMOps's [az_webapp_deploy.sh](https://github.com/microsoft/llmops-promptflow-template/blob/main/llmops/common/scripts/az_webapp_deploy.sh)

> **Note:** The AIGA Template will not support Azure Functions as a target runtime out-of-the-box. Our focus will be a containerised deployment of flows on Azure App Service.

The templated LLMOps will allow for different deployment options to be selected for each flow and each environment. For example, Azure Machine Learning may be used for development, while Azure App Service may be used for production.

AIGA should provide relevant documentation, and links to existing resources, to help projects select a suitable deployment option.

At the present time, we have opted to not support Azure Kubernetes Service out-of-the-box. It is expected that App Service will serve the majority of production workloads. Furthermore, AIGA does not currently have the capacity to support the additional complexity of operating Kubernetes.

## Consequences

The AIGA Template will provide a solid foundation for deploying Prompt flows to Azure, with support for Azure Machine Learning and Azure App Service out-of-the-box.

The following artefacts will be required to provide support for both deployment options:

- The AIGA Reference Architecture will provide a variant for both Azure Machine Learning and Azure App Service.
- The Infrastructure Request document will need to be configurable to support these options.
- CI/CD workflows will have to cater for both deployment options, with configuration options to select the desired deployment target.

A project may present a unique set of requirements that are not met by the deployment options provided out-of-the-box. In such cases, the project team will need to extend the AIGA Template to support additional deployment options. Given the flexibility of a container image, this should be a relatively straightforward task.
