#!/bin/bash

# Description:
# This script deploys prompt flow image to Public Azure Web App

# This is sample script to show the deployment process.
# Update it as necessary.

# Replace/Update the code here to provision webapps for
# private networks and/or use different means of provisioning
# using Terraform, Bicep or any other way.

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --build_id)
            build_id="$2"
            shift 2
            ;;
        --DOCKER_IMAGE_REGISTRY)
            DOCKER_IMAGE_REGISTRY="$2"
            shift 2
            ;;
        --WA_AZURE_SUBSCRIPTION_ID)
            WA_AZURE_SUBSCRIPTION_ID="$2"
            shift 2
            ;;
        --WA_RESOURCE_GROUP_NAME)
            WA_RESOURCE_GROUP_NAME="$2"
            shift 2
            ;;
        --WA_NAME)
            WA_NAME="$2"
            shift 2
            ;;
        --USE_CASE_BASE_PATH)
            USE_CASE_BASE_PATH="$2"
            shift 2
            ;;
        --DEPLOY_ENVIRONMENT)
            DEPLOY_ENVIRONMENT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

source .env
. .env
set -e # fail on error

REGISTRY_ENDPOINT="$DOCKER_IMAGE_REGISTRY.azurecr.io"
echo "Build ID: $build_id"
echo "Container registry endpoint: $REGISTRY_ENDPOINT"
echo "Webapp subscription ID: $WA_AZURE_SUBSCRIPTION_ID"
echo "Webapp rg name: $WA_RESOURCE_GROUP_NAME"
echo "App name: $WA_NAME"

# Set the Web App subscription
az account set --subscription "$WA_AZURE_SUBSCRIPTION_ID"

# read values from deployment_config.json related to `webapp_endpoint`
env_name=$DEPLOY_ENVIRONMENT
deploy_config="./config/deployment_config.json"
env_var_file_path="./$USE_CASE_BASE_PATH/environment/env.yaml"
con_object=$(jq ".webapp_endpoint[] | select(.ENV_NAME == \"$env_name\")" "$deploy_config")

config_path="./$USE_CASE_BASE_PATH/experiment.yaml"
STANDARD_FLOW=$(yq '.flow' "$config_path" |  sed 's/"//g')

env_output=()
if [ -e "$env_var_file_path" ]; then
    IFS=' ' read -r -a env_output <<< $(poetry run python llmops/common/deployment/generate_env_vars.py "$env_var_file_path" "false")
fi

read -r -a connection_names <<< "$(echo "$con_object" | jq -r '.CONNECTION_NAMES | join(" ")')"

# create/update Web App config settings
az webapp config appsettings set --resource-group "$WA_RESOURCE_GROUP_NAME" --name "$WA_NAME" \
    --settings WEBSITES_PORT=8080

for name in "${connection_names[@]}"; do
    uppercase_name=$(echo "$name" | tr '[:lower:]' '[:upper:]')

    api_base_env_name="${uppercase_name}_API_BASE"
    api_base=${!api_base_env_name}
    api_key_env_name="${uppercase_name}_API_KEY"
    api_key=${!api_key_env_name}

    az webapp config appsettings set \
        --resource-group $WA_RESOURCE_GROUP_NAME \
        --name $WA_NAME \
        --settings ${api_base_env_name}=${api_base} ${api_key_env_name}=${api_key}
done

for pair in "${env_output[@]}"; do
    echo "Key-value pair: $pair"
    key="${pair%%=*}"
    value="${pair#*=}"
    key=$(echo "$key" | tr '[:lower:]' '[:upper:]')
    pair="$key=$value"
    az webapp config appsettings set \
        --resource-group "$WA_RESOURCE_GROUP_NAME" \
        --name "$WA_NAME" \
        --settings "$key"="$value"
done

az webapp config appsettings set \
        --resource-group "$WA_RESOURCE_GROUP_NAME" \
        --name "$WA_NAME" \
        --settings PROMPTFLOW_SERVING_ENGINE=fastapi

# Configure the Web App to use container registry with service principal credentials
az webapp config container set --name "$WA_NAME" --resource-group "$WA_RESOURCE_GROUP_NAME" --docker-custom-image-name "$REGISTRY_ENDPOINT"/"$USE_CASE_BASE_PATH"/"$STANDARD_FLOW"_"$DEPLOY_ENVIRONMENT":"$build_id" --docker-registry-server-url https://"$REGISTRY_ENDPOINT"

# Restart the Web App to apply changes
az webapp restart --name "$WA_NAME" --resource-group "$WA_RESOURCE_GROUP_NAME"

echo "Deployment completed successfully."
