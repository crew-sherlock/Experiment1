# 3. Use and provision storage account for AML Datastore

Date: 2024-06-20

## Status

Proposed

## Context

An Azure Machine Learning workspace is provisioned with a default storage account, which is used as the default datastore for the workspace.
This ADR is to decide whether to use the default storage account or provision a new storage account for the workspace.

## Decision

We will provision a new storage account for the Azure Machine Learning workspace to be used for datastores.
The default storage account is not recommended for production workloads, as it is shared with other resources in the workspace and does not have the necessary performance and security configurations.
Each stage (dev, uat, prod) of the Azure Machine Learning workspace will have its own storage account to be used for datastores.

## Consequences

An additional storage account will be provisioned with the AIGA reference architecture, for each stage (dev, uat, prod) and the instance configuration is updated to use the new storage account as the datastore for the Azure Machine Learning workspace.
