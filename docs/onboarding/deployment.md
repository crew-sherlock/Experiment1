# Deployment

One of the key deployable artifacts for an AIGA Project is an OCI-compliant container
image. This repository uses `pf` to build an image that can be deployed to many
platforms, including Azure App Services, Azure Machine Learning, and more.

The flow container image is built during Continuous Integration and is pushed to Azure
Container Registry.

## Choosing a Deployment Option

The decision on which deployment option to use should be based on the specific
requirements of the project, considering factors such as reliability, security, cost,
performance, and existing skills.

The following table presents key factors to consider when choosing a deployment option:

| Deployment Option                          | AIGA Support        | Availability                      | Cost                                                                | Deployment density                                          | Scalability                                                                                                                                                                            | Auto-scale             | Security Features                                           | Troubleshooting      |
|--------------------------------------------|---------------------|-----------------------------------|---------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|-------------------------------------------------------------|----------------------|
| Azure App Service                          | 🟢 Build and Deploy | 🟢 99.99% with Availability Zones | App Service SKU x Instances [[ref](#pricing-for-azure-app-service)] | 🟠 One flow, per app. Multiple apps per plan.               | 🟢 [Quotas and Limits](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#app-service-limits)                                 | 🟢 Metrics or Schedule | 🟢 [Security Features](#security-in-azure-app-service)      | 🟢 Extensive Tooling |
| Managed endpoint in Azure Machine Learning | 🟢 Build and Deploy | 🟠 99.9%                          | VM SKU x Instances                                                  | 🔴 One flow, per endpoint. One endpoint is one or more VMs. | 🟠 [Quotas and Limits](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-quotas?view=azureml-api-2#azure-machine-learning-online-endpoints-and-batch-endpoints)\* | 🟢 Metrics or Schedule | 🟠 [Security Features](#security-in-azure-machine-learning) | 🟠 Primitive Tooling |

\* We have noted that Azure App Service can achieve greater scalability than Azure
Machine Learning. This is largely due
to [resource limits](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-quotas?view=azureml-api-2#azure-machine-learning-online-endpoints-and-batch-endpoints)
in Azure Machine Learning. However, it's expected that all services will be capable of
handling the load of a typical AIGA Project.

In all deployment options, it is recommended to maintain a one-to-one mapping between a
flow and a container image. This simplifies the deployment process and ensures that each
flow is isolated from others.

### Security

#### Security in Azure App Service

Azure App Service can further secure your app with the built-in security-focused
features. These features include:

- TLS/SSL certificates
- Static IP restrictions
- Client authentication and authorization
- Service-to-service authentication, including Azure Managed Identity
- Connectivity to Azure resources, Azure Virtual Network, and on-premises resources
- Integration with Azure Key Vault
- Network isolation options, including Private Endpoints and VNet Integration

For further information,
see [Security in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/overview-security).

#### Security in Azure Machine Learning

Azure Machine Learning provides a secure environment hosting managed endpoints. The
security features include:

- Client authentication
- Network isolation using Private Endpoints
- Connectivity to Azure resources using Azure Managed Identity
- Integration with Azure Key Vault (in Preview)

![Endpoint Network Isolation](../assets/endpoint-network-isolation-with-workspace-managed-vnet.png)

For further information,
see [Azure Machine Learning Security Baseline](https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/machine-learning-service-security-baseline).

### Pricing

#### Pricing for Azure App Service

An app service always runs in an *App Service plan*. An App Service plan defines a set
of compute resources for a web app to run. You pay for the computing resources your App
Service plan allocates. Therefore, you can potentially save money by putting multiple
apps into one App Service plan.

It is completely viable to run multiple flows in a single App Service plan, as long as
the plan can handle the load. However, you should isolate your app into a new App
Service plan when:

- The app is resource-intensive.
- You want to scale the app independently from the other apps.
- The app needs resource in a different geographical region.

An App Service plan is billed regardless of the number of apps running in it. Including
when the apps are stopped. The only exception is
the [Consumption plan](https://learn.microsoft.com/en-us/azure/azure-functions/consumption-plan),
which provides a fully serverless hosting option for Azure Functions. A consumption plan
bills for compute resources only when your functions are running.

> It is possible to run a flow as part of an Azure Function to take advantage of the
> Consumption plan. However, the AIGA Template does not support this deployment option
> out-of-the-box.

For further information,
see [Azure App Service plan overview](https://learn.microsoft.com/en-us/azure/app-service/overview-hosting-plans)
and [Azure App Service pricing](https://azure.microsoft.com/en-us/pricing/details/app-service/linux/).

### Configuration

To configure the type of deployment set the `DEPLOYMENT_TARGET` variable. See [GitHub Variables](./github-variables.md) for more information. Please ensure that the [deployment_config.json](https://github.com/gsk-tech/AIGA/blob/main/config/deployment_config.json) file is updated with the correct configuration.

### Additional Resources

- [Choose an Azure compute service](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree)
- [Choose an Azure container service](https://learn.microsoft.com/en-us/azure/architecture/guide/choose-azure-container-service)
