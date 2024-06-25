# Decision Log

This document is used to track key decisions that are made during the course of the project. This can be used at a later stage to understand why decisions were made and by whom.

| **Decision**             | **Date**    | **Alternatives Considered** | **Reasoning** | **Detailed doc**                                                             | **Made By** | **Work Required** |
|--------------------------|-------------|-----------------------------|---------------|------------------------------------------------------------------------------|-------------|------------------|
| Use Architecture Decision Records| 19-Jun-2024 | Standard Design Docs | An easy and low cost solution of tracking architecture decisions over the lifetime of a project | [Record Architecture Decisions](./adrs/001-record-architecture-decisions.md) | Dev Team | NA |
| Use Storage Account for AML Datastore | 20-Jun-2024 | Use the default storage account | Easier to provide and manage access to the storage and more scalable and reliable solution | [Use Storage Account for AML Datastore](./adrs/003-use-and-provision-storage-account.md) | Avishay Balter | NA |
| Use Storage Account for AML | 20-Jun-2024 | Use the default storage account | Easier to provide and manage access to the storage | [Use Storage Account for AML Datastore](./adrs/003-use-and-provision-storage-account.md) | Avishay Balter | NA |
| Use single Azure Container Registry for all AIGA services across environments | 20-Jun-2024 | Use the default AML container registry | Easier to manage access and cost | [Use and provision Azure Container Registry](./adrs/004-use-and-provision-azure-container-registry.md) | Avishay Balter | NA |
