# Chat with PDF Example

This is a simple flow that allow you to ask questions about the content of a PDF file and get answers. You can run the flow with a URL to a PDF file and question as argument. Once it's launched it will download the PDF and build an index of the content. Then when you ask a question, it will look up the index to retrieve relevant content and post the question with the relevant content to OpenAI chat model.

## Local Run
### Prerequisites
- Install Promptflow SDK and other dependencies
```shell
pip install  -r requirements.txt
```

- Create OpenAI Connection ([Reference Here](https://microsoft.github.io/promptflow/how-to-guides/manage-connections.html#create-a-connection))
```
pf connection create -f openai.yaml --set api_key=<your-api-key>
```
#### Deployment names

These are the models currently used in this repo

| Model	| Model deployment name	| Provider | Version | Environment |
|-------|---------------|----------|---------|-------------|
| text-embedding-ada-002 | psc-msat-us6-text-embedding-ada-002-01 | OpenAI |	2      |	dev |
| gpt-4o                 |	gpt-4o-2024-05-13               |	OpenAI | 5/13/2024 |	dev |
| text-embedding-3-large | text-embedding-3-large |	OpenAI |	1      |	dev |
| text-embedding-3-small | text-embedding-3-small |	OpenAI |    1      |    dev |

Make sure you change the models' deployment names. 

### Running Locally

To run in interactive mode, you can use the following command:
```shell
pf flow test --flow promptflow/inference --interactive
```
This command will enable the flow to run in a chatbot fashion inside the terminal.

## Creating a docker container

The docker files will be created in the CI pipeline, the reference for which can be seen [here](https://github.com/microsoft/llmops-promptflow-template/blob/main/llmops/common/scripts/gen_docker_image.sh).
