# Decision Log

This document is used to track key decisions that are made during the course of the project. This can be used at a later
stage to understand why decisions were made and by whom.
| **Decision**             | **Date**    | **Alternatives Considered** | **Reasoning** | **Detailed doc**                                                             | **Made By** | **Work Required** |
|--------------------------|-------------|-----------------------------|---------------|------------------------------------------------------------------------------|-------------|------------------|
| Use Architecture Decision Records| 19-Jun-2024 | Standard Design Docs | An easy and low cost solution of tracking architecture decisions over the lifetime of a project | [Record Architecture Decisions](./adrs/001-record-architecture-decisions.md) | Dev Team | NA |
| Code repository structure | 19-Jun-2024 | Independent package structure  for each repository | A standardized code repository structure for an AIGA instance | [Code repository structure](./adrs/002-code-repository-structure.md) | Arpit Gaur, Bhavana Rao | NA |
| Use Storage Account for AML Datastore | 20-Jun-2024 | Use the default storage account | Easier to provide and manage access to the storage and more scalable and reliable solution | [Use Storage Account for AML Datastore](./adrs/003-use-and-provision-storage-account.md) | Avishay Balter | NA |
| Use Storage Account for AML | 20-Jun-2024 | Use the default storage account | Easier to provide and manage access to the storage | [Use Storage Account for AML Datastore](./adrs/003-use-and-provision-storage-account.md) | Avishay Balter | NA |
| Use single Azure Container Registry for all AIGA services across environments | 20-Jun-2024 | Use the default AML container registry | Easier to manage access and cost | [Use and provision Azure Container Registry](./adrs/004-use-and-provision-azure-container-registry.md) | Avishay Balter | NA |
| An Azure Machine Learning workspace per environment | 21-Jun-2024 | Single Azure Machine Learning workspace for all environments in an AIGA Project, A single AML instance for all AIGA Projects | Based on Microsoft LLMOps best practices. | [An Azure Machine Learning workspace per AIGA environment](./adrs/005-single-aml-per-environment.md) | Avishay Balter | NA |
