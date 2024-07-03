# 2. Code Repository Structure

Date: 2024-06-19

## Status

Proposed

## Context

The goal is to establish a well-defined, modular, and self-scaffolding code repository structure that can be used to bootstrap GenAI experimentation, CI/CD, and other related processes. This decision is motivated by the need for a standardized and efficient way to manage and organize code in our projects. It is influenced by factors such as the complexity of the projects, the need for scalability, and the desire for a streamlined CI/CD process.

This repository will be templated and used as a starting point for new projects using the `AIGA Starter`. More info about `AIGA Starter` can be found at the [ADR-006](./006-aiga-project-creation.md).

## Decision

Our proposed folder structure would look like this:

```text

.azure # For azure pipelines
│
├── pipelines
├── templates
│
.github
│
├── workflows # For github actions
│
docs
│
├── adrs
├── design
├── onboarding
│   └── GETTING_STARTED.md
├── experiments
│   └── template.md
│
promptflow
│
├── tools
│   ├── ingestion_tool.py
│   ├── intelligence_tool.py
│   └── README.md
│
├── example-flow
│   └── example-flow.dag.yaml
│
├── datasets
│   └── sample_golden_dataset.csv
│
├── setup
│   ├── env_setup.py
│   └── setup.md

├── prompt-flow.dag.yaml
│
notebooks
│
├── examples
│   └── example_01.ipynb
│
src
│
├── skills
│   └── skill_01.py
│
├── utils
│   └── config
│
├── chunking
│   ├── config
│   ├── strategies
│   │   ├── strategy.py # abstract/interface
│   │   ├── strategy_01.py
│   ├── tests
│   │   └── test_strategy_01.py
│
├── doc_intelligence
│   ├── config
│   ├── /strategies
│   │   ├── doc_intelligence.py # abstract/interface
│   │   └── doc_intelligence_01.py
│   ├── tests
│   │   └── test_strategy_01.py
│
├── ingestion
│   ├── config
│   ├── strategies
│   │   ├── strategy.py  # abstract/interface
│   │   └── strategy_01.py
│   ├── tests
│   │   └── test_strategy_01.py
│
├── evaluation
│   ├── config
│   ├── strategies
│   │   ├── strategy.py  # abstract/interface
│   │   └── strategy_01.py
│   ├── tests
│   │   └── test_strategy_01.py
│
├── pre-processing
│   ├── config
│   ├── strategies
│   │   ├── strategy.py  # abstract/interface
│   │   └── strategy_01.py
│   ├── tests
│   │   └── test_strategy_01.py
│
├── search
│   ├── config
│   ├── strategies
│   │   ├── strategy.py  # abstract/interface
│   │   └── strategy_01.py
│   ├── tests
│   │   └── test_strategy_01.py
config
│
├── config-sample.yaml
├── config.scheme.json
│
containerization
│
├── Dockerfile # an example Dockerfile
│
CONTRIBUTING.md
SECURITY.md
README.md
LICENSE
CODE_OF_CONDUCT.md
.env_template # This contains template for environment variables.
│

```

### Project Folder Structure Documentation

This documentation provides an overview of the project's folder structure, detailing the purpose and contents of each folder and file. This will help in navigating the project and understanding the organization of files.

#### Root Level

- **.env_template**: Contains template for environment variables.
- **CONTRIBUTING.md**: Guidelines for contributing to the project.
- **SECURITY.md**: Information about security policies and procedures.
- **README.md**: Overview and information about the project.
- **LICENSE**: Licensing information for the project.
- **CODE_OF_CONDUCT.md**: Code of conduct for contributors.

### Folder Structure

#### 1. .azure

This folder contains configurations for Azure pipelines.

- **pipelines**: Azure pipeline configurations.
- **templates**: Templates for Azure pipelines.

#### 2. .github

This folder contains configurations for GitHub Actions.

- **workflows**: GitHub Actions workflows.

#### 3. docs

This folder contains documentation files.

- **adrs**: Architecture Decision Records.
- **design**: Detailed design documents.
- **onboarding**: Onboarding documentation.
  - **GETTING_STARTED.md**: Getting started guide.
- **experiments**: Experimental documentation will contain the context and details of the experiments to standardize the output and insights from the experiments.
  - **template.md**: Template for experiment documentation.

#### 4. promptflow

This folder contains tools and resources for prompt flow management.

- **tools**
  - **ingestion_tool.py**: Ingestion tool script.
  - **intelligence_tool.py**: Intelligence tool script.
  - **README.md**: Documentation for tools.
- **datasets**
  - **sample_golden_dataset.csv**: Sample golden dataset.
- **example-flow**
  - **example-flow.dag.yaml**: Example DAG flow configuration.
- **setup**
  - **env_setup.py**: Environment setup script.
  - **setup.md**: Documentation for environment setup.
- **prompt-flow.dag.yaml**: Main prompt-flow DAG configuration.

#### 5. notebooks

This folder contains Jupyter notebooks for examples and experimentation.

- **examples**
  - **example_01.ipynb**: Example Jupyter notebook.

#### 6. /src

This folder contains the source code for various modules and utilities.

- **skills** : This folder contains the skills implemented using Azure Function app.
  - **skill_01.py**: Function app to implement a custom skill.
- **utils**
  - **config**: Configuration files for utilities.
- **chunking**
  - **config**: Configuration files for chunking module.
  - **strategies**
    - **strategy.py**: Abstract/interface for chunking strategies.
    - **strategy_01.py**: Implementation of a chunking strategy.
  - **tests**
    - **test_strategy_01.py**: Tests for chunking strategy.
- **doc_intelligence**
  - **config**: Configuration files for document intelligence module.
  - **strategies**
    - **doc_intelligence.py**: Abstract/interface for document intelligence strategies.
    - **doc_intelligence_01.py**: Implementation of a document intelligence strategy.
  - **tests**
    - **test_strategy_01.py**: Tests for document intelligence strategy.
- **ingestion**
  - **config**: Configuration files for ingestion module.
  - **strategies**
    - **strategy.py**: Abstract/interface for ingestion strategies.
    - **strategy_01.py**: Implementation of an ingestion strategy.
  - **tests**
    - **test_strategy_01.py**: Tests for ingestion strategy.
- **evaluation**: Provides different strategies to do evaluation.
  - **config**: Configuration files for evaluation module.
  - **strategies**
    - **strategy.py**: Abstract/interface for evaluation strategies.
    - **strategy_01.py**: Implementation of an evaluation strategy.
  - **tests**
    - **test_strategy_01.py**: Tests for evaluation strategy.
- **pre-processing**: Custom ability to do pre-processing, e.g., synthetic data generation, data sanitization, etc.
  - **config**: Configuration files for pre-processing module.
  - **strategies**
    - **strategy.py**: Abstract/interface for pre-processing strategies.
    - **strategy_01.py**: Implementation of a pre-processing strategy.
  - **tests**
    - **test_strategy_01.py**: Tests for pre-processing strategy.
- **search**: Custom ability to do pre-processing, e.g., synthetic data generation, data sanitization, etc.
  - **config**: Configuration files for search module.
  - **strategies**
    - **strategy.py**: Abstract/interface for searching strategies.
    - **strategy_01.py**: Implementation of a searching strategy.
  - **tests**
    - **test_strategy_01.py**: Tests for searching strategy.

#### 7. config

This folder contains configuration files for the project.

- **config-sample.yaml**: Sample configuration file.

#### 8. containerization

This folder contains resources for containerizing the application.

- **Dockerfile**: Example Dockerfile for containerization.

## Conclusion

This documentation provides a detailed overview of the folder structure, explaining the purpose of each folder and file. It serves as a guide for navigating and understanding the organization of the project.

## Consequences

The proposed structure of the repository provides a template to create repositories for AIGA experiments. It also makes it easier to onboard new developers and maintain the codebase. The structure also makes it easier to integrate with CI/CD tools.
