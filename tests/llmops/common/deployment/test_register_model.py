"""Tests for the register_model module."""
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from llmops.common.deployment.register_model import register_model, hash_folder
from azure.ai.ml.entities import Model

THIS_PATH = Path(__file__).parent
CWD_PATH = Path.cwd()
RESOURCE_PATH = CWD_PATH / "tests/llmops/resources"


@pytest.fixture(scope="module", autouse=True)
def _set_required_env_vars():
    """Set required environment variables."""
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("AML_AZURE_SUBSCRIPTION_ID", "TEST_SUBSCRIPTION_ID")
    monkeypatch.setenv("AML_RESOURCE_GROUP_NAME", "TEST_RESOURCE_GROUP_NAME")
    monkeypatch.setenv("AML_WORKSPACE_NAME", "TEST_WORKSPACE_NAME")


def test_register_model():
    """Test register_model."""
    model_path = str(RESOURCE_PATH / "flows/exp_flow")
    model_hash = hash_folder(model_path)
    with patch(
        "llmops.common.deployment.register_model.MLClient"
    ) as mock_ml_client:
        # Mock the MLClient
        ml_client_instance = Mock()
        mock_ml_client.return_value = ml_client_instance

        # Mock available model
        mock_model = Mock()
        mock_model.tags.return_value = {}
        ml_client_instance.models.get.return_value = mock_model

        # Register model
        register_model(base_path=str(RESOURCE_PATH), env_name="dev")

        # Assert that ml_client.models.create_or_update is called
        ml_client_instance.models.create_or_update.assert_called_once()

        # Assert that ml_client.models.create_or_update is called with
        # the correct argument
        created_model = (
            ml_client_instance.models.create_or_update.call_args.args[0]
        )
        assert isinstance(created_model, Model)
        assert created_model.name == "exp_dev"
        assert created_model.path == model_path
        assert (
            created_model.properties["azureml.promptflow.source_flow_id"] == (
                model_path
            )
        )
        assert created_model.tags["model_hash"] == model_hash


def test_register_existing_model():
    """Test register_model with an existing model."""
    model_path = str(RESOURCE_PATH / "flows/exp_flow")
    model_hash = hash_folder(model_path)
    with patch(
        "llmops.common.deployment.register_model.MLClient"
    ) as mock_ml_client:
        # Mock the MLClient
        ml_client_instance = Mock()
        mock_ml_client.return_value = ml_client_instance

        # Mock available model
        mock_model = Mock()
        mock_model.tags = {"model_hash": model_hash}
        ml_client_instance.models.get.return_value = mock_model

        # Register model
        register_model(base_path=str(RESOURCE_PATH), env_name="dev")

        # Assert that ml_client.models.create_or_update is not called
        ml_client_instance.models.create_or_update.assert_not_called()
