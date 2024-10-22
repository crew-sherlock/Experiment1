# 10. AIGA project structure

Date: 2024-07-01

## Status

Accepted

## Context

When designing the AIGA template we have several considerations we would like to tackle, there will be several modules the template will depend on and work with.
We need to understand the structure of the repository in order to develop a solution which will fit the template and different modules.
This ADR will refer to the following components:

- Building blocks - How to split the modules, packages and libs
- Github structure - one repository vs. multiple

## Building blocks

How to split the modules, packages and libs, this will help us in our decision for the repositories.

Following [this design](../assets/AIGA.svg), the main components of the AIGA repository are:

- AIGA template - The basis of the AIGA project.
- AIGA starter - A wizard to start working with AIGA.

When creating the AIGA template, we should make sure each component inside will be defined on its own folder and structure so if in the future it will need to be separated, it will be done easily, also see [ADR-002](002-code-repository-structure.md).

## Multi vs. single repository

### Single GitHub Repository

**Pros:**

- Easier Setup and Maintenance: Only one repository to configure with CI/CD pipelines, issue tracking, and other integrations.
- Unified History: All changes and history are contained in one place, making it easier to track progress and changes.
- Single Version Control: A single versioning scheme for the entire project, reducing complexity in managing dependencies and versions across multiple repos.
- Ease of Access: Contributors need to clone only one repository to access the entire project.
- Single Point of Reference: All issues, discussions, and pull requests are in one place, simplifying project management and collaboration.
- Cross-Module Changes: Easier to make changes that span multiple modules or components, as everything is in one place.
- Consistent Standards: Enforces a consistent coding standard and project structure.

**Cons:**

- Large Codebase: As the project grows, the repository can become large and unwieldy, making cloning and builds slower.
- Complex Merge Conflicts: More contributors working on the same repo can lead to more frequent and complex merge conflicts.
- Coupling: High coupling between different parts of the project can make it harder to isolate and resolve issues.
- Permission Management: Granular permission control is difficult, as all contributors have access to the entire codebase.
- Deployment Challenges: Deploying or updating parts of the project independently is more challenging.
- Technical Debt: Easier for technical debt to accumulate unnoticed in a large, monolithic repo.
- Template management: It will make it harder to customize the template each time to specific project requirements as they are all in the cloned repo.

### Multiple GitHub Repositories

**Pros:**

- Isolation: Each module or component can be developed, tested, and deployed independently.
- Clear Boundaries: Helps enforce clear boundaries and responsibilities between different parts of the project.
- Smaller Codebases: Smaller, more manageable repositories are easier to clone, build, and maintain.
- Parallel Development: Different teams can work on different repos in parallel without interfering with each other.
- Granular Permissions: More control over who can access and contribute to specific parts of the project.
- Security: Enhanced security by limiting access to sensitive parts of the project.
- Tailored Pipelines: Each repo can have its own CI/CD pipeline tailored to its specific needs.
- Independent Deployments: Easier to deploy and roll back individual components.

**Cons:**

- Repository Management: Managing multiple repositories can be complex and time-consuming.
- Dependency Management: More complex dependencies and versioning between repositories.
- Distributed History: History is spread across multiple repositories, making it harder to get a holistic view of the project's progress.
- Scattered Issues: Issues, pull requests, and discussions are distributed across multiple repositories, complicating project management.
- Cross-Repo Changes: Changes that span multiple repositories can be harder to coordinate and implement.
- Consistent Standards: Ensuring consistent coding standards and practices across multiple repositories requires more effort.

## Conclusions

We would like to have multiple repositories, for now, we will start with a repository for the AIGA template and AIGA starter.
As the project is still new and doesn't have much code yet, for easier and faster development, we would advise to start with the minimum repositories required for the first stage.
Having said that, each component should be in its own folder and have its own structure, for clear development and for ease of separation later on.

We would suggest starting with two repositories:

- Template repository - Artefact which forms the basis of an AIGA project.
- Starter repository - Artefacts related to the wizard and starting with the AIGA project.

Each repository should have [Branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule).

## Action items

- Create the two repositories and make sure they contain all the requirements.
- Make sure to structure the flows and experimentation in a way they can be transferred easily to another repository.
