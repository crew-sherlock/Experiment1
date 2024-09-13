"""Tests for the create_aml_endpoint module."""
from unittest.mock import Mock, patch

import pytest
from pathlib import Path
from llmops.common.deployment.provision_endpoint import (
    create_endpoint
)

THIS_PATH = Path(__file__).parent
CWD_PATH = Path.cwd()
RESOURCE_PATH = CWD_PATH / "tests/llmops/resources"
DEPLOYMENT_CONFIG = RESOURCE_PATH / "config/deployment_config.json"


@pytest.fixture(scope="module", autouse=True)
def _set_required_env_vars():
    """Set required environment variables."""
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("AML_AZURE_SUBSCRIPTION_ID", "TEST_SUBSCRIPTION_ID")
    monkeypatch.setenv("AML_RESOURCE_GROUP_NAME", "TEST_RESOURCE_GROUP_NAME")
    monkeypatch.setenv("AML_WORKSPACE_NAME", "TEST_WORKSPACE_NAME")


def test_create_provision_endpoint_when_not_exists():
    """Test create_provision_endpoint."""
    env_name = "dev"
    endpoint_name = "test-endpoint"
    endpoint_description = "test-endpoint-description"
    with patch(
        "llmops.common.deployment.provision_endpoint.MLClient"
    ) as mock_ml_client:
        # Mock the MLClient
        ml_client_instance = Mock()
        mock_ml_client.return_value = ml_client_instance
        ml_client_instance.online_endpoints.list.return_value = []

        # Create the endpoint
        create_endpoint(env_name, str(RESOURCE_PATH),
                        deployment_config=DEPLOYMENT_CONFIG)

        # Assert online_endpoints.begin_create_or_update is called once
        create_endpoint_calls = (
            ml_client_instance.online_endpoints.begin_create_or_update
        )
        assert create_endpoint_calls.call_count == 1

        # Assert that ml_client.online_endpoints.begin_create_or_update
        # is called with the correct argument

        # create_endpoint_calls.call_args_list is triple nested,
        # first index: select the call of
        # ml_client.online_endpoints.begin_create_or_update [0]
        # second index: select the argument of
        # ml_client.online_endpoints.begin_create_or_update
        # [1 (named_argument)]
        # third index: select the named argument ["endpoint"]
        created_endpoint = (
            create_endpoint_calls.call_args_list[0][1]["endpoint"]
        )
        assert created_endpoint.name == endpoint_name
        assert created_endpoint.description == endpoint_description
        assert created_endpoint.auth_mode == "key"


def test_create_provision_endpoint_when_exists():
    """Test create_provision_endpoint."""
    env_name = "dev"
    endpoint_name = "test-endpoint"
    with patch(
        "llmops.common.deployment.provision_endpoint.MLClient"
    ) as mock_ml_client:
        # Mock the MLClient
        ml_client_instance = Mock()
        mock_ml_client.return_value = ml_client_instance

        mock_endpoint = Mock()
        mock_endpoint.name = endpoint_name
        ml_client_instance.online_endpoints.list.return_value = [
            mock_endpoint
        ]

        # Create the endpoint
        create_endpoint(env_name,
                        str(RESOURCE_PATH),
                        deployment_config=DEPLOYMENT_CONFIG)

        assert (ml_client_instance.online_endpoints.begin_create_or_update.call_count
                == 1)
