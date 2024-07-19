# Map AIGA Reference Architecture to Gen AI DevKit

Date: 2024-07-10

## Status

Proposed

## Context

As a Gen AI Architect, there is a need to have the AIGA Reference Architecture map to the Gen AI DevKit so that after ARB1, Gen AI projects can simply request that reference architecture to be provisioned. The Code Orange Gen AI DevKit should support the optional flows and resources.

## Decision

We will map the AIGA Reference Architecture to the [Code Orange GenAI DevKit](https://gsk.service-now.com/home?id=sc_cat_item&table=sc_cat_item&sys_id=17c151861bc98254269687b8e34bcb40), ensuring that the necessary components are provisioned. The following components have been identified based on the architecture needs:

### Components already provisioned by the [Code Orange GenAI DevKit](https://gsk.service-now.com/home?id=sc_cat_item&table=sc_cat_item&sys_id=17c151861bc98254269687b8e34bcb40)

- AML Compute Instance (Out Of The Box with AML)
- LLM Gateway
- Azure AI Search
- Content Safety (included in the latest DevKit release)
- Translator (included in the latest DevKit release)
- Document Intelligence (included in the latest DevKit release)
- Azure Machine Workspace (Out Of The Box with AML)
- Azure Monitor (available at node level)
- Application Insights (Out Of The Box with AML)
- Azure Key Vault

### Components currently not provisioned through the [Code Orange GenAI DevKit](https://gsk.service-now.com/home?id=sc_cat_item&table=sc_cat_item&sys_id=17c151861bc98254269687b8e34bcb40) but will be incorporated in future releases (already included in the PI plan, ETA to be provided by CO C4I PM Gandhar Juvekar)

- Azure Storage - Doc Store and Doc Store Metadata
- Azure SQL - Job Metadata
- Azure Blob Storage (aka Azure Storage)

### Components not to be included in the Gen AI DevKit

- GitHub Actions
- Azure Functions
- Azure Container Registry (managed by BUs and can be attached to AML)
- Web App
- Azure Storage AML Registry: the AML instance will have the Out Of The Box/default version, but according to Avishay Balter, the architecture will require an external registry to be attached to AML. Code Orange currently does not provision any non-Out Of The Box registry. Based on the information gathered, these are managed by the GP&T organization (contact Kummy Doraiswamy).

## Consequences

By mapping the AIGA Reference Architecture to the Gen AI DevKit and incorporating the necessary components, Gen AI projects will be able to request the reference architecture to be provisioned efficiently mostly through the Code Orange Dev Kit. This will streamline the deployment process and ensure that all required components are available to support the projects. Future releases of the Gen AI DevKit will include additional components as planned, and any components not managed by the Code Orange Dev Kit will be handled by the appropriate routes/sources/organizations.
