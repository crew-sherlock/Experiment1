# AI Generation Accelerator (AIGA)

![Release Status](https://github.com/gsk-tech/AIGA/actions/workflows/create-release.yml/badge.svg?branch=main)
![Promptflow CI Status](https://github.com/gsk-tech/AIGA/actions/workflows/promptflow-ci-workflow.yml/badge.svg?branch=main)
![Promptflow CD Status](https://github.com/gsk-tech/AIGA/actions/workflows/promptflow-cd-workflow.yml/badge.svg?branch=main)

The **AI Generation Accelerator (AIGA)** provides a repeatable framework for building standardised LLM applications. It is intended to accelerate the delivery of value by:

1. Bootstrapping experimentation and evaluation
1. Implementing best practices for building and deploying Generative AI capabilities
1. Providing a pre-approved set of artefacts, processes, and tools to support industrialisation at scale

The AI Generation Accelerator (AIGA) will comprise a collection of artefacts, processes, and tools, each with a specific scope and purpose.

![AI Generation Accelerator (AIGA)](./docs/assets/AIGA.svg)

## Set up guide for AIGA

We have created the [AIGA Starter](https://github.com/gsk-tech/AIGA-Starter) to help you set up a new project using the AIGA template. The AIGA Starter will generate the necessary artefacts to get you started with your Generative AI project - this includes pre-approved architecture and code repositories. If you are looking to get started, check out the [setup guide](./docs/onboarding/setup-guide.md).

## AIGA Components

## AIGA Reference Architecture

A high-level repeatable blueprint for building the infrastructure of a Generative AI applications. The architecture and components described will be pre-approved as an *Architecture Pattern* within GSC (Global Supply Chain) to expedite ARB approval for new projects.

## AIGA Template

A Git repository template designed to bootstrap and facilitate building, evaluating, and deploying Generative AI capabilities - with a particular focus on Retrieval Augmented Generation (RAG) pattern.

- The template will be hosted on GitHub, and will be the starting point for new projects.
- The template will contain executable [flows](https://microsoft.github.io/promptflow/concepts/concept-flows.html), [tools](https://microsoft.github.io/promptflow/concepts/concept-tools.html), [skills](https://learn.microsoft.com/en-us/azure/search/cognitive-search-predefined-skills), and configuration.
- The template will contain documentation artefacts:
  - **Contribution Guides** [*(CONTRIBUTING.md)*](./CONTRIBUTING.md) - To support the contribution of code, documentation, and other artefacts to the **template**.
  - **Getting Started Guides** - To support the project team get up and running with their *AIGA Project*.
  - **Project Documentation** - To support the project lifecycle, along with artefacts to expedite ARB approval and infrastructure requests.
- The template will include [workspace settings](https://code.visualstudio.com/docs/getstarted/settings#_workspace-settings) for VSCode, support for [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers), and [pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/what-is-azure-pipelines) for CI/CD.

The template structure is defined in [ADR-002](./adrs/002-code-repository-structure.md).

### [AIGA Starter](https://github.com/gsk-tech/AIGA-Starter)

A tool, or collection of processes, that will capture key project information and orchestrate the creation of an *AIGA Project*, based on an *AIGA Template*.

### AIGA Project

A project-specific instance created by the *AIGA Starter*. An *AIGA Project* is scoped to a project and has a one-to-one relationship with a *CIID*. It encapsulates a project-owned repository, along with the necessary code, automation, and documentation to support the project. Once created the *AIGA Project* will be owned by the product team.

#### Environments

One, or more, deployed environments containing the infrastructure required to support the application - as described in the *AIGA Reference Architecture*.

#### Project Repository

A clone of the *AIGA Template* repository, with project-specific configuration, code, and documentation. This repository will be owned by the project team.

## Common Terminology

| Term | Definition |
| ---- | --- |
| Agents | A software entity used to augment, or orchestrate, the capabilities of an Large Language Model (LLM) to perform a complex task. |
| [DAG Flow](https://microsoft.github.io/promptflow/concepts/concept-flows.html#dag-flow) | A Directed Acyclic Graph (DAG) of function calls, expressed in YAML. These functions, or "tools", are connected via input/output dependencies and executed based on the topology. |
| Ground Truth | Well-established answers or knowledge document chunks in a dataset corresponding to a known input. |
| [RAG](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview) | An architecture that augments the capabilities of a Large Language Model (LLM) by adding an information retrieval system that provides grounding data. |
| [Skills](https://learn.microsoft.com/en-us/azure/search/cognitive-search-predefined-skills) | A concept of Azure AI Search. An atomic operation that transforms content, recognizes or extracts text, or reshapes a previous enrichment. It could be built-in, custom, or a utility. |
| [Tool](https://microsoft.github.io/promptflow/concepts/concept-tools.html) | The fundamental building block of a flow. An executable unit or function that can perform a task.|
| Golden Dataset| The trusted source of data used for evaluation of GenAI flows. It contains the ground truth and is approved by business.|

## Getting started with the project

To get started with AIGA, take a look at the [Getting Started](./docs/onboarding/getting-started.md) guide and the [Lifecycle of the project](/docs/design/lifecycle.md).
