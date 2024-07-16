# GitHub Actions

## Workflows

Workflows are a feature of GitHub Actions that allow you to automate your software
development lifecycle in your repository. AIGA leverages workflows to automate various
tasks, such as build verification, testing, and deployment. Because AIGA comprises
multiple components, such as AIGA Template, AIGA Starter, and AIGA Projects, it is
important to understand the scope of each workflow, and when and where they are
triggered.

| Workflow                                                                                          | Description                                                                                                                           | Repository    | Trigger                  |
|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|---------------|--------------------------|
| [template-pr.yaml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/template-pr.yaml) | Build verification and testing for components in the AIGA Template. Including spell checking, linting, and unit testing.              | AIGA Template | *PR* to *main*           |
| [template-ci.yaml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/template-ci.yaml) | Build verification and testing for components in the AIGA Template.                                                                   | AIGA Template | *Push*/*merge* to *main* |
| [build_validation_workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/template-build-verification.yaml)         | Validating code and structure, connect to subscription and run unit tests                                                             | AIGA Template | *PR* to *main*           |
| [platform_pr_dev_workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/platform_pr_dev_workflow.yml)              | PR pipeline template triggered from the experiment triggers build validation -> register data assets -> executes prompt flow bulk run | AIGA Template | *PR* to *main*           |
| [chat_with_pdf_pr_dev_workflow.yml](https://github.com/gsk-tech/AIGA/blob/main/.github/workflows/chat_with_pdf_pr_dev_workflow.yml)    | Experiment specific workflow invokes platform_pr_dev_workflow.yml                                                                     | AIGA Template | *PR* to *main*           |
