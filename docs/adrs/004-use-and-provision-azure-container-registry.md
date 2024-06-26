# 1. Use and provision Azure Container Registry

Date: 2024-06-20

## Status

Proposed

## Context

Azure Machine Learning workspace can be provisioned with an Azure Container Registry, which is used to register and host models. This ADR is to decide whether to use the default Azure Container Registry created with the workspace or to provision one that is used across all AIGA services.

## Decision

We will provision an Azure Container Registry per AIGA environment, for the three environments (dev, uat, prod), and will use the single registry across all services (e.g. app services, functions, AML).
This will allow for better management of the container images used across the services and will allow for better control of the images used in an AIGA environment across the different stages (Dev, UAT, Prod) and the AIGA services cost.

## Consequences

A single Azure Container Registry is provisioned with AIGA reference architecture, and configuration is updated to use it for the Azure Machine Learning workspaces in all stages (Dev, UAT, Prod) and all the other AIGA services that are using containers.
