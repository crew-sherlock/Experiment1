# GitHub Variables

AIGA uses GitHub Variables to store project-specific configuration settings. These variables are primarily used in GitHub Action workflows to control the behaviour of LLMOps.

> **Note:** By default, variables render unmasked in build outputs. Do not use variables to store sensitive information like API keys, secrets, or passwords. Instead, use [GitHub Secrets](./github-secrets.md).

## Repository Variables

An AIGA Project can configure the behaviour of the repository workflows by setting the following variables:

- `DEPLOYMENT_TARGET` - The Azure service to target for inference deployment - "aml", "webapp" or "both"
- `PROMPTFLOW_BASE_PATH` - The base path for the PromptFlow directory. E.g. "promptflow"
- `TMP_ENV` - The environment to target. **Note:** This variable will be deprecated in future releases.

## Environment Variables

Environment Variables are used within AIGA to control which resources are used based on the environment (e.g. `pr`, `dev`, `prod`).

The following Environment Variables are required as a pre-requisite for AIGA:

- `KEY_VAULT_NAME` - should point to the Azure Key Vault associated with Code Orange GenAI Dev Kit.
