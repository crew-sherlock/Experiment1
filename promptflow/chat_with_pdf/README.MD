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
pf create create -f <path-to-azure-open-ai-connection> --set api_key=<your-api-key>
```

### Running Locally

To run in interactive mode, you can use the following command:
```shell
pf flow test --flow promptflow\chat_with_pdf\flows\standard --interactive
```
This command will enable the flow to run in a chatbot fashion inside the terminal.

## Creating a docker container

The docker files will be created in the CI pipeline, the reference for which can be seen [here](https://github.com/microsoft/llmops-promptflow-template/blob/main/llmops/common/scripts/gen_docker_image.sh).
