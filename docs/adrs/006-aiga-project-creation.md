# 6. AIGA Project Creation

Date: 2024-06-21

## Status

In Review

## Context

One of the key components of AIGA is the *Starter*. A tool, or collection of processes, that will capture key project information and orchestrate the creation of an *AIGA Project*, based on an *AIGA Template*.

The orchestration would involve, but is not be limited to:

- Creating a new repository
- Setting up the necessary CI/CD pipelines
- Submitting the necessary requests for infrastructure provisioning
- Configuring access to the necessary services
- Producing documentation

This ADR is intended to capture the options available and the decision made for orchestrating the creation of an *AIGA Project*. The UI/UX of the *Starter* is out of scope for this ADR.

## Orchestration Options

> **Note:** The following options do not address the specifics of the *Starter* tool, but rather options for the underlying process for creating an *AIGA Project*. It is also possible that a combination of these options could be used.

1. **Manual**: The *Starter* could document a set of instructions for creating an *AIGA Project* manually. These instructions could be distributed across multiple teams in Global Supply Chain, and could be integrated into existing processes. However, this would be error-prone and time-consuming. The process could be triggered via a ServiceNow ticket.

    ![Manual](../assets/starter/manual.svg)

1. **Standalone**: A standalone *Project Repository* could be created from a [template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository). Alternatively, requesters could [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the template repository. This would lack the orchestration capabilities of the other options and put the onus on the team to configure the repository and necessary services. Documentation, scripts, and workflows could be provided in the template repository to ease setup.

    > The option of using [Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) was considered. This would allow for the inclusion of shared resources. However, Project extensibility and update patterns were deemed out of scope for this ADR. The focus of ADR 006 is on the initial creation of an *AIGA Project*.

    ![Standalone](../assets/starter/standalone.svg)

1. **GitOps**: The *Starter* could be a GitOps process. Project information could be captured in a configuration file, managed in a central Git repository. A GitOps process would then orchestrate the creation of an *AIGA Project*. The process itself could be a standalone service or a series of workflows in GitHub Actions. This approach would allow for centralised state management, iterative updates, and benefit from close integration with the Git toolchain (e.g. pull requests, approvals, etc.). This approach could reduce central access requirements, as requesters could [fork the repo](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) and contribute back a 'request' using a pull request.

    ![GitOps](../assets/starter/gitops.svg)

1. **GitHub Action**: The *Starter* could be a collection of GitHub Actions workflows, that are triggered on the `workflow_dispatch` event. These workflows would be managed in a central Git repository (e.g. `AIGA-Starter`) responsible for orchestration. They could be triggered using the Actions tab on GitHub, GitHub CLI, or the REST API. This approach could leverage capabilities of GitHub Actions, such as secrets management, approvals, and pre-built *actions*. It would require minimal effort in the future to build an application layer over the GitHub API, to trigger the `workflow_dispatch` event. While similar to GitOps, this approach is expected to require less upfront development. However, it would lack centralised state management and could result in environment drift. Furthermore, it should be considered that users would require repository 'contribute' permission to trigger the workflows manually.

    > Where existing Actions are not sufficient, [custom actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions) could be developed and maintained in the `AIGA-Starter` repository.

    ![GitHub Action](../assets/starter/github-actions.svg)

1. **Application:** It is likely that an application layer would sit in front of the options presented so far. For example, a *web app* that can invoke a GitHub Actions workflow. However, it is also feasible for the application to handle orchestration independently. This could be local or server side. Both options would require "custom" development and lack the benefits of an existing toolchain.

    1. **Local**: The *Starter* could be a local application (e.g. CLI tool or Jupyter Notebook) that would guide the user through a wizard-based form and then create an *AIGA Project*. This would be more user-friendly than manual creation. However, given it would run locally, it would require the user to have access and necessary permissions to create the required resources.

        ![Local App](../assets/starter/local-app.svg)

    1. **Server**: The *Starter* could be a server application (e.g. Web App) that would capture relevant project information and then create an *AIGA Project*. This could be more user-friendly than a local application, and would allow state and permissions to be managed centrally. However, it would require additional development effort. Furthermore, dedicated infrastructure would be required to host the application.

        ![Server App](../assets/starter/server-app.svg)

## Decision

We will orchestrate the creation and management of an *AIGA Project* using **GitHub Actions** workflows. The workflows will be triggered using the `workflow_dispatch` event, from the GitHub UI. Future development will include the creation of an application that leverages the GitHub REST API.

![GitHub Action](../assets/starter/github-actions-decision.svg)

This will reside in a central Git repository, `AIGA-Starter`, responsible for orchestration.

This decision was made based on the following factors:

- **Ease of Development**: GitHub Actions provides a low barrier to entry for development. It is likely that the existing capabilities of GitHub Actions will be sufficient for the initial implementation.
- **Integration**: GitHub Actions will allow for close integration with the existing tools, such as approvals, built-in actions, and secrets management.
- **Minimal Infrastructure**: GitHub Actions does not require dedicated infrastructure. This will reduce the operational overhead of the *Starter*.
- **Extensibility**: GitHub Actions can be extended with [custom actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions). This will allow for additional capabilities to be added in the future.
- **REST Integration**: GitHub provides a [REST API](https://docs.github.com/en/rest) that can be used to trigger workflows. This will allow for the development of an application layer in the future.
- **Use of GitHub Script**: [actions/github-script](https://github.com/actions/github-script) makes it easy to quickly write a script in your workflow that uses the GitHub API and the workflow run context. These scripts can invoke a JavaScript file which can be built and tested locally.

> Workflow [inputs](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onworkflow_dispatchinputs) will be used to capture project information.

## Consequences

The following consequences are expected as a result of this decision:

- GitHub Actions are limited to "Allow enterprise, and select non-enterprise, actions and reusable workflows" in the GSK organisation.
- Although unlikely, it may be necessary to develop custom actions to support the creation of an *AIGA Project*.
- *AIGA Project* requests will require the requester to have 'contribute' permissions on the `AIGA-Starter` repository.
- Consideration should be made for portability of the orchestration, and where possible, avoid locking into GitHub Actions specific features.
