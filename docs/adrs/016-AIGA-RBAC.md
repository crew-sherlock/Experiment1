# 16. AIGA Role-Based Access Control

Date: 2024-08-28

## Status

Under Review

## Context

Working with AIGA components such as the starter, and extending AIGA components further requires the definition of Role-Based Access Control (RBAC) for developers and users. This will help in defining the access controls and to document the expected usage of the AIGA platform.

## Decision

Using GitHub built-in access control, we will define the following roles:

### AIGA Maintainer

**Description**: This role will have full access to the AIGA repository and will be able to manage code, actions and RBAC on the AIGA template repository.

**Implementation**: An AIGA Maintainer is added to the AIGA repository [Collaborators list](https://github.com/gsk-tech/AIGA/settings/access) with an admin role.
> Note: if the link above does not work, you can ask the project owner to add you to the repository.

### AIGA Contributor

**Description**: This role will have access to the AIGA repository and will be able to contribute to the codebase and actions.

**Implementation**: An AIGA Contributor is added to the AIGA repository [Collaborators list](https://github.com/gsk-tech/AIGA/settings/access) with a write role.
> Note: if the link above does not work, you can ask the project owner to add you to the repository.

### AIGA Starter Maintainer

**Description**: This role will have full access to the AIGA-Starter repository and will be able to manage code, actions and RBAC on the AIGA template repository.

**Implementation**: An AIGA-Starter Maintainer is added to the AIGA-Starter repository [Collaborators list](https://github.com/gsk-tech/AIGA-Starter/settings/access) with an admin role and to the AIGA-Users team [Members list](https://github.com/orgs/gsk-tech/teams/aiga-users) with a maintainer role.
> Note: if the link above does not work, you can ask the project owner to add you to the repository.

### AIGA Starter Contributor

**Description**: This role will have access to the AIGA repository and will be able to contribute to the codebase and actions.

**Implementation**: An AIGA-Starter Contributor is added to the AIGA-Starter repository [Collaborators list](https://github.com/gsk-tech/AIGA-Starter/settings/access) with a write role.
> Note: if the link above does not work, you can ask the project owner to add you to the repository.

### AIGA Starter User

**Description**: This role can trigger actions and use the AIGA-Starter repository.

**Implementation**: An AIGA-Starter User is added to the AIGA-Users team [Members list](https://github.com/orgs/gsk-tech/teams/aiga-users) with a member (default) role.
> Note: if the link above does not work, you can ask the project owner to add you to the repository.

## Consequences

By defining these roles, we will be able to manage access to the AIGA repositories and ensure that the right people have the right level of access to the AIGA components. This will help in ensuring that the AIGA components are maintained and used as intended.
