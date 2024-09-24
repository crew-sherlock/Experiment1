# GitHub Actions

Workflows are a feature of GitHub Actions that allow you to automate your software
development lifecycle in your repository. AIGA leverages workflows to automate various
tasks, such as build verification, testing, and deployment. Because AIGA comprises
multiple components, such as AIGA Template, AIGA Starter, and AIGA Projects, it is
important to understand the scope of each workflow, and when and where they are triggered.

## Workflows

|Workflow                                                                                        | Description                                                                         | Trigger           |
|-------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|-------------------|
| [pr-workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/pr-workflow.yml) | Experiment PR workflow, validates dev container, run unit tests and bulk experiment | *PR* to *main* or manually. When running manually you can specify the environment that the validation will use (playground, dev, uat, prod) using the `environment` variable. The default is set using the repository variable DEFAULT_ENVIRONMENT |
| [promptflow-ci-workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/promptflow-ci-workflow.yml) | Experiment CI workflow, runs bulk experiment and evaluation, see [LLMOps](./llmops.md) for further detail                         | *Merge* to *main* or manually. When running manually you can specify if you want the CD to run (using the `deployment` input parameter) and the environment that the validation will use (playground, dev, uat, prod) using the `environment` variable. The default is set using the repository variable DEFAULT_ENVIRONMENT|
| [promptflow-cd-workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/promptflow-ci-workflow.yml) | Runs prompts in flow and evaluates results, see [LLMOps](./llmops.md) for further detail | *Merge* to *main* or manually. When running manually you can specify the environment that the deployment will target (playground, dev, uat, prod) using the `environment` variable. The default is set using the repository variable DEFAULT_ENVIRONMENT|
| [pr-title-checker.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/pr-title-checker.yml) | Validates PR title conforms to [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) naming                         | *PR* created or edited |
| [create-release.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/create-release.yml) | Publishes a new release including determining the version number and release notes                     | *Merge* to *main* |

## Reusable Workflows

| Workflow                                                                                                    | Description                                                 | Triggered by        |
|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|---------------------|
| [run-workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/run-workflow.yml)           | Register experiment data assets and run experiment bulk run | ci and pr workflows |
| [evaluate-workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/evaluate-workflow.yml) | Register evaluation data assets and runs evaluations        | ci workflow         |
| [reusable-cd-workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/reusable-cd-workflow.yml) | The CD workflow. This is triggered either from the CI (promptflow-ci-workflow) when it completes successfully, or from the CD (promptflow-cd-workflow) when triggered manually. It will accept the environment variable from either of the triggering workflows as well as the checkout_sha_ref which controls the git commit that is deployed.         | cd workflow         |

## Custom Actions

| Action                                                                                                         | Description                                                                        | Triggered by                              |
|----------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-------------------------------------------|
| [execute-script](https://github.com/gsk-tech/AIGA/blob/main/.github/actions/execute-script/action.yml)         | Wrapper to use poetry when running python scripts so it will be in the environment | run and evaluate workflows                |
| [execute-unit-tests](https://github.com/gsk-tech/AIGA/blob/main/.github/actions/execute-unit-tests/action.yml) | Set us environment and runs unit tests                                             | pr workflow                               |
| [setup-environment](https://github.com/gsk-tech/AIGA/blob/main/.github/actions/setup-environment/action.yml)   | A script to set up the python environment with poetry                              | run and evaluate workflows and unit tests |

## GitHub Variables

Some workflows require specific values to be provided as inputs to the workflow. These input variables are:

- `use_case_base_path`: This is the path to the use case folder and is provided as an input to the workflow, otherwise a default is used.
- `MODEL_VERSION`: Once a flow has been registered, the CD workflow will read what the latest version of the flow is and this is what version is deployed.
- `DEPLOY_ENVIRONMENT`: This is environment to which the endpoint and model should be deployed and is provided as an input to the workflow, otherwise a default is used.
