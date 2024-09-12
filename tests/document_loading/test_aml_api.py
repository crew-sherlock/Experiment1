import unittest
from unittest.mock import patch, MagicMock
from azureml.core.authentication import ServicePrincipalAuthentication
from src.document_loading.aml_api import AMLApi
from src.document_loading.aml_config import AMLConfig


class TestAMLApi(unittest.TestCase):

    def setUp(self):
        self.aml_config = MagicMock(spec=AMLConfig)
        self.aml_config.subscription_id = "test-subscription-id"
        self.aml_config.resource_group = "test-resource-group"
        self.aml_config.workspace_name = "test-workspace-name"
        self.aml_config.experiment_name = "test-experiment-name"
        self.aml_config.compute_name = "test-compute-name"
        self.aml_config.vm_size = "STANDARD_D2_V2"
        self.aml_config.max_nodes = 4
        self.aml_config.datastore_name = "test-datastore-name"
        self.aml_config.storage_account_name = "test-storage-account-name"
        self.aml_config.container_name = "test-container-name"
        self.aml_config.data_path = "test-data-path"
        self.sp = MagicMock(spec=ServicePrincipalAuthentication)
        self.aml_api = AMLApi(self.aml_config, self.sp)

    @patch('azureml.core.compute.AmlCompute.provisioning_configuration')
    @patch('azureml.core.compute.ComputeTarget.create')
    def test_create_compute_target(self, mock_compute_target_create,
                                   mock_provisioning_configuration):
        mock_workspace = MagicMock()
        mock_compute_target = MagicMock()
        mock_compute_target_create.return_value = mock_compute_target

        compute_target = self.aml_api.create_compute_target(mock_workspace)

        mock_provisioning_configuration.assert_called_once_with(
            vm_size=self.aml_config.vm_size,
            max_nodes=self.aml_config.max_nodes
        )
        mock_compute_target_create.assert_called_once_with(
            workspace=mock_workspace,
            name=self.aml_config.compute_name,
            compute_config=mock_provisioning_configuration.return_value
        )
        self.assertEqual(compute_target, mock_compute_target)

    @patch('azureml.core.Datastore.register_azure_blob_container')
    def test_create_datastore(self, mock_register_azure_blob_container):
        mock_workspace = MagicMock()
        mock_datastore = MagicMock()
        mock_register_azure_blob_container.return_value = mock_datastore

        datastore = self.aml_api.create_datastore(mock_workspace)

        mock_register_azure_blob_container.assert_called_once_with(
            workspace=mock_workspace,
            datastore_name=self.aml_config.datastore_name,
            account_name=self.aml_config.storage_account_name,
            container_name=self.aml_config.container_name
        )
        self.assertEqual(datastore, mock_datastore)

    @patch('azureml.core.Datastore.get')
    def test_get_or_create_datastore_existing(self, mock_datastore_get):
        mock_workspace = MagicMock()
        mock_datastore = MagicMock()
        mock_datastore_get.return_value = mock_datastore

        datastore = self.aml_api.get_or_create_datastore(mock_workspace)

        mock_datastore_get.assert_called_once_with(
            workspace=mock_workspace,
            datastore_name=self.aml_config.datastore_name
        )
        self.assertEqual(datastore, mock_datastore)

    @patch('azureml.core.Datastore.register_azure_blob_container')
    @patch('azureml.core.Datastore.get')
    def test_get_or_create_datastore_new(self, mock_datastore_get,
                                         mock_register_azure_blob_container):
        mock_workspace = MagicMock()
        mock_datastore_get.side_effect = Exception("Datastore not found")
        mock_datastore = MagicMock()
        mock_register_azure_blob_container.return_value = mock_datastore

        datastore = self.aml_api.get_or_create_datastore(mock_workspace)

        mock_datastore_get.assert_called_once_with(
            workspace=mock_workspace,
            datastore_name=self.aml_config.datastore_name
        )
        mock_register_azure_blob_container.assert_called_once_with(
            workspace=mock_workspace,
            datastore_name=self.aml_config.datastore_name,
            account_name=self.aml_config.storage_account_name,
            container_name=self.aml_config.container_name
        )
        self.assertEqual(datastore, mock_datastore)

    @patch('azureml.core.Dataset.File.from_files')
    def test_create_dataset(self, mock_from_files):
        mock_datastore = MagicMock()
        mock_dataset = MagicMock()
        mock_from_files.return_value = mock_dataset
        mock_dataset.to_path.return_value = ["file1", "file2", "file3"]

        dataset = self.aml_api.create_dataset(mock_datastore)

        mock_from_files.assert_called_once_with(
            path=(mock_datastore, self.aml_config.data_path)
        )
        self.assertEqual(dataset, mock_dataset)


if __name__ == '__main__':
    unittest.main()
