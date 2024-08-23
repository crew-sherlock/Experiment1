# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/azureml/promptflow/promptflow-runtime:latest

ARG USE_CASE_BASE_PATH=promptflow
ARG FLOW_NAME=inference

WORKDIR /

COPY ./$USE_CASE_BASE_PATH/inference/requirements.txt /flow/requirements.txt

# gcc is for build psutil in MacOS
RUN apt-get update && apt-get install -y runit gcc

# install pip dependencies
RUN pip install -r /flow/requirements.txt

COPY ./$USE_CASE_BASE_PATH/$FLOW_NAME /flow
COPY ./$USE_CASE_BASE_PATH/prompts /flow/prompts
COPY ./src /flow/src

EXPOSE 8080

# reset runsvdir
RUN rm -rf /var/runit
COPY ./docker/runit /var/runit
# grant permission
RUN chmod -R +x /var/runit

COPY ./docker/start.sh /
CMD ["bash", "./start.sh"]
