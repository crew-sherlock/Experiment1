# 5. An Azure Machine Learning workspace per AIGA environment

Date: 2024-06-21

## Status

Proposed

## Context

An Azure Machine Learning workspace is used to manage machine learning models, data, and compute resources. The workspace is used to train, deploy, and manage machine learning models.
For the purpose of the AIGA reference architecture, we need to decide whether to use a single Azure Machine Learning workspace for all the AIGA Projects or to provision a separate workspace for each AIGA Project or to provision one for each Project's environment (dev, uat, prod).

## Decision

Based on the [Microsoft recommendations for implementing LLMOps](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/how-to-end-to-end-llmops-with-prompt-flow?view=azureml-api-2) we will provision a separate Azure Machine Learning workspace for each environment (dev, uat, prod) per AIGA Project. This may change later when we have a better understanding of the requirements and constraints of the AIGA Projects and the features of the Azure Machine Learning workspace in regards to user-specific authorisation and resource management when we may switch to have a single AML instance per dev environments across all AIGA Projects.

## Consequences

The AIGA AI architect will not have a single view of all the AIGA Projects and the models trained and deployed in all Projects. The AIGA AI architect will need to manage the Azure Machine Learning workspaces for each AIGA Project separately, and will need to manage the resources and permissions for each workspace separately.
