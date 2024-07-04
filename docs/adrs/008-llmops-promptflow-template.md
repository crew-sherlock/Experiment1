# 8. LLMOps Prompt Flow Template repository

Date: 2024-06-26

## Status

Accepted

## Context

The repository contains example of several different prompt flow use cases. Each use case has an example evaluation flow and the following structure:

- .azure-pipelines : It contains the CI and PR related pipelines for Azure DevOps and specific to a use-case.
- configs          : It contains the configuration files for the use-case deployment.
- data             : This folder contains data files related to Prompt flow standard and evaluation flow.
- environment      : It contains a dockerfile used for running containers with flows for inferencing on Azure webapps and env.yml for declaring app specific environment variables.
- flows            : It should contain minimally two folder - one for standard Prompt flow related files and another for Evaluation flow related file. There can be multiple evaluation flow related folders.
- tests            : contains unit tests for the flows.
- data-pipelines   : It contains the data pipelines to generate the datasets (experimentation, evaluation etc.) necessary for the flows. This folder will have sub-folders specific to the data engineering tool - Microsoft Fabric, Azure ML etc.

Additionally, there is a `experiment.yaml` file that configures the use-case.

**The project includes 6 examples demonstrating different scenarios:**

- Web Classification (YAML-based)

Location: ./web_classification
Importance: Demonstrates website content summarization with multiple variants, showcasing the flexibility and customization options available in the template.

- Named Entity Recognition (YAML-based)

Location: ./named_entity_recognition
Importance: Showcases the extraction of named entities from text, which is valuable for various natural language processing tasks and information extraction.

- Math Coding (YAML-based)

Location: ./math_coding
Importance: Showcases the ability to perform mathematical calculations and generate code snippets, highlighting the versatility of the template in handling computational tasks.

- Chat with PDF (YAML-based, RAG-based)

Location: ./chat_with_pdf
Importance: Demonstrates a conversational interface for interacting with PDF documents, leveraging the power of retrieval-augmented generation (RAG) to provide accurate and relevant responses.

- Code Generation (Function-based flows)

Location: ./function_flows
Importance: Demonstrates the generation of code snippets based on user prompts, showcasing the potential for automating code generation tasks.

- Chat Application (Class-based flows)

Location: ./class_flows
Importance: Showcases a chat application built using class-based flows, illustrating the structuring and organization of more complex conversational interfaces.

It also allows to integrate with different pipeline tools.

**The project also contains the following folders:**

- The '.azure-pipelines' folder contains the common Azure DevOps pipelines for the platform and any changes to them will impact execution of all the flows.

- The '.github' folder contains the Github workflows for the platform as well as the use-cases. This is bit different than Azure DevOps because all Github workflows should be within this single folder for execution.

- The '.jenkins' folder contains the Jenkins declarative pipelines for the platform as well as the use-cases and individual jobs.

- The 'docs' folder contains documentation for step-by-step guides for both Azure DevOps, Github Workflow and Jenkins related configuration.

- The 'llmops' folder contains all the code related to flow execution, evaluation and deployment.

- The 'dataops' folder contains all the code related to data pipeline deployment.

- The 'local_execution' folder contains python scripts for executing both the standard and evaluation flow locally.

## Decision

We will need to defer two aspects of the repository:

- Ops - the ops part of the repository to run the templates and examples.
- Templates - different templates to solve different problems.

### Ops

We need to verify the pipelines, which ones are relevant, and we would like to take and change.

Can be ignored:

- .jenkins - Jenkins flows.
- .azure-pipelines - Azure pipelines.

To be done:

- Structure the way we want each experiment to look like.
- Go through the pipelines and check which part are relevant for us.
- Have a template for a pipeline we can re-use per example.
- Replace Anaconda with Poetry.
- Generic, reusable configuration for any experiment.
- Have configuration per experiment.
- Verify dependencies and packages are on the latest versions.
- Docker issues:
  - Previously the examples were not working with the dockers per folder and only with one docker for all, so need to test that (the issue was with adding helpers).
  - Docker should use promptflow latest image.
- Deployment to Azure ML did not work.

### Templates

It will save us a lot of time and effort to use these code samples in the AIGA repository with the following changes:

Can be removed:

- Web-classification.
- Code Generation.
- Named Entity Recognition.

To be done:

- Replace Math Coding example with example using flowchart and matrices developed by Virginie's GSK team.
- Docs folder needs to be organized with relevant content for us.
- Create concrete use-case/example from existing templates.
- Add tests to the specific example.
- Rename data-pipeline as it can be a confusing name.
- The script to deploy the flow on AML endpoint is not working, need to verify it.
- Replace Anaconda with Poetry.
- Match the examples structure to the AIGA repository structure.
- Update examples with changes that Virginie and GSK team already made to make them GSK ready.
- Verify the existing monitoring and logging which exists in the examples and that they match our [Observability ADR](007-observability-prompt-flow.md).
- Examples were missing on helpers such as SQL helper blob helper etc. They should be used across evaluations.
  - We need to understand how we are going to manage and maintain those helpers in internal or external, a lib? package? etc.

> Note: there is a GSK example for an experiment: MSAT-Quality-LOC-PPR-Promptflow see develop branch -> src

## Consequences

Need to build our own echo system for the experiments using the repository.
The AIGA Template will be built using the code and assets from [Microsoft llmops promptflow template](https://github.com/microsoft/llmops-promptflow-template) which will expedite the process of creating prompt flow examples.
However, it will require some customizations to match the code to the AIGA template repository.
