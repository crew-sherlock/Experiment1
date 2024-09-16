# GenAI models available

The models deployed are available through the gateway. When receiving the devkit, you will get an API and authentication to access the models deployed for you. The models deployed are shared across multiple projects. Hence you can access them from your API given that you are in the same environment.

## Deployment names for GSC

These are the models currently deployed for GSC.

| Model| Model deployment name| Provider | Version | Environment |
|-------|---------------|----------|---------|-------------|
| text-embedding-ada-002 | psc-msat-us6-text-embedding-ada-002-01 | OpenAI | 2 |dev |
|  gpt-4o | gpt-4o-2024-05-13| OpenAI | 2024-02-15-preview | dev |
| text-embedding-3-large | text-embedding-3-large| OpenAI |1|dev |
| text-embedding-3-small | text-embedding-3-small|OpenAI |1 |dev |
| gpt-4 | psc-msat-us6-gpt-4-01 | OpenAI  |1 |dev |
| gpt-35-turbo | gpt-35-turbo | OpenAI  |1 |dev |

Make sure you change the models' deployment names in your flows.
