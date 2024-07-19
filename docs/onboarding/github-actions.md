# GitHub Actions

Workflows are a feature of GitHub Actions that allow you to automate your software
development lifecycle in your repository. AIGA leverages workflows to automate various
tasks, such as build verification, testing, and deployment. Because AIGA comprises
multiple components, such as AIGA Template, AIGA Starter, and AIGA Projects, it is
important to understand the scope of each workflow, and when and where they are
triggered.

## Workflows

| Workflow                                                                                        | Description                                                                         | Trigger           |
|-------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|-------------------|
| [pr-workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/pr-workflow.yml) | Experiment PR workflow, validates dev container, run unit tests and bulk experiment | *PR* to *main*    |
| [ci-workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/ci-workflow.yml) | Experiment CI workflow, runs bulk experiment and evaluation                         | *Merge* to *main* |

## Reusable Workflows

| Workflow                                                                                                    | Description                                                 | Triggered by        |
|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|---------------------|
| [run-workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/run-workflow.yml)           | Register experiment data assets and run experiment bulk run | ci and pr workflows |
| [evaluate-workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/evaluate-workflow.yml) | Register evaluation data assets and runs evaluations        | ci workflow         |

## Custom Actions

| Action                                                                                                         | Description                                                                        | Triggered by                              |
|----------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-------------------------------------------|
| [execute-script](https://github.com/gsk-tech/AIGA/blob/main/.github/actions/execute-script/action.yml)         | Wrapper to use poetry when running python scripts so it will be in the environment | run and evaluate workflows                |
| [execute-unit-tests](https://github.com/gsk-tech/AIGA/blob/main/.github/actions/execute-unit-tests/action.yml) | Set us environment and runs unit tests                                             | pr workflow                               |
| [setup-environment](https://github.com/gsk-tech/AIGA/blob/main/.github/actions/setup-environment/action.yml)   | A script to set up the python environment with poetry                              | run and evaluate workflows and unit tests |
