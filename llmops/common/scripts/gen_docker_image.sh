#!/bin/bash

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --USE_CASE_BASE_PATH)
            USE_CASE_BASE_PATH="$2"
            shift 2
            ;;
        --DEPLOY_ENVIRONMENT)
            DEPLOY_ENVIRONMENT="$2"
            shift 2
            ;;
        --build_id)
            build_id="$2"
            shift 2
            ;;
        --REGISTRY_NAME)
            REGISTRY_NAME="$2"
            shift 2
            ;;
        --REGISTRY_SECRET)
            REGISTRY_SECRET="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Description:
# This script generates docker image for Prompt flow deployment
set -e # fail on error

source .env
. .env


# read values from experiment.yaml related to given environment
config_path="./$USE_CASE_BASE_PATH/experiment.yaml"
env_var_file_path="./$USE_CASE_BASE_PATH/environment/env.yaml"

REGISTRY_ENDPOINT="$REGISTRY_NAME.azurecr.io"
echo "Build ID: $build_id"
echo "Deploy environment: $DEPLOY_ENVIRONMENT"
echo "Registry: $REGISTRY_ENDPOINT"
echo "PWD: $(pwd)"
echo "ls: $(ls -la)"
echo "STANDARD_FLOW: $STANDARD_FLOW"
echo "USE_CASE_BASE_PATH: $USE_CASE_BASE_PATH"

if [[ -e "$config_path" ]]; then
    STANDARD_FLOW=$(yq '.flow' "$config_path" |  sed 's/"//g')

    init_file_path="./$USE_CASE_BASE_PATH/$STANDARD_FLOW/flow.flex.yaml"

    init_output=""

    if [ -e "$init_file_path" ]; then
        init_output=$(python llmops/common/deployment/generate_config.py "$init_file_path" "true")
    fi
    echo "$init_output"

    env_output=""
    if [ -e "$env_var_file_path" ]; then
        echo "$env_var_file_path"
        env_output=$(poetry run python llmops/common/deployment/generate_env_vars.py "$env_var_file_path" "true")
    fi
    echo "$env_output"

    pip install -r ./$USE_CASE_BASE_PATH/$STANDARD_FLOW/requirements.txt
    pf flow build --source "./$USE_CASE_BASE_PATH/$STANDARD_FLOW" --output "./$USE_CASE_BASE_PATH/$STANDARD_FLOW/docker"  --format docker

    cp "./docker/promptflow/Dockerfile" "./$USE_CASE_BASE_PATH/$STANDARD_FLOW/docker/Dockerfile"

    poetry run python -m llmops.common.deployment.migrate_connections --base_path "$USE_CASE_BASE_PATH" --env_name $DEPLOY_ENVIRONMENT
    # docker build the prompt flow based image

    docker build --platform=linux/amd64 -t localpf "./$USE_CASE_BASE_PATH/$STANDARD_FLOW/docker"

    docker images

    deploy_config="./config/deployment_config.json"
    con_object=$(jq ".webapp_endpoint[] | select(.ENV_NAME == \"$DEPLOY_ENVIRONMENT\")" "$deploy_config")

    read -r -a CONNECTION_NAMES <<< "$(echo "$con_object" | jq -r '.CONNECTION_NAMES | join(" ")')"
    result_string=""
    printenv
    for name in "${CONNECTION_NAMES[@]}"; do
        uppercase_name=$(echo "$name" | tr '[:lower:]' '[:upper:]')
        env_var_key="${uppercase_name}_API_KEY"
        api_key=${!env_var_key}
        result_string+=$(printf " -e %s=%s" "$env_var_key" "$api_key")
    done
    echo "$result_string"
    docker_args=$result_string

    if [ -n "$init_output" ]; then
        docker_args+=" $init_output"
    fi

    if [ -n "$env_output" ]; then
        docker_args+=" $env_output"
    fi

    docker_args+=" -e PROMPTFLOW_SERVING_ENGINE=fastapi "
    docker_args+=" -m 512m --memory-reservation=256m --cpus=2 -dp 8080:8080 localpf:latest"
    echo "$docker_args"

    docker run $(echo "$docker_args")

    sleep 20

    docker ps -a

    chmod +x "./$USE_CASE_BASE_PATH/sample-request.json"

    file_contents=$(<./$USE_CASE_BASE_PATH/sample-request.json)
    echo "$file_contents"

    poetry run python -m llmops.common.deployment.test_local_flow \
            --base_path "$USE_CASE_BASE_PATH"

    docker login "$REGISTRY_ENDPOINT" -u "$REGISTRY_NAME" --password-stdin <<< "$REGISTRY_SECRET"
    docker tag localpf "$REGISTRY_ENDPOINT"/"$USE_CASE_BASE_PATH"/"$STANDARD_FLOW"_"$DEPLOY_ENVIRONMENT":"$build_id"
    docker tag localpf "$REGISTRY_ENDPOINT"/"$USE_CASE_BASE_PATH"/"$STANDARD_FLOW"_"$DEPLOY_ENVIRONMENT":"latest"
    docker push "$REGISTRY_ENDPOINT"/"$USE_CASE_BASE_PATH"/"$STANDARD_FLOW"_"$DEPLOY_ENVIRONMENT":"$build_id"
    docker push "$REGISTRY_ENDPOINT"/"$USE_CASE_BASE_PATH"/"$STANDARD_FLOW"_"$DEPLOY_ENVIRONMENT":"latest"

else
    echo "$config_path" "not found"
fi
