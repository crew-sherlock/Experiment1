from aml_config import AMLConfig
import sys
import os
import logging

from azureml.core import Experiment, Dataset, Datastore, Workspace
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.core.compute_target import ComputeTargetException
from azureml.core.authentication import ServicePrincipalAuthentication

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AMLApi:
    def __init__(self,
                 aml_config: AMLConfig,
                 sp: ServicePrincipalAuthentication) -> None:
        self.aml_config = aml_config
        self.sp = sp

    def get_workspace(self):
        return Workspace(subscription_id=self.aml_config.subscription_id,
                         resource_group=self.aml_config.resource_group,
                         workspace_name=self.aml_config.workspace_name, auth=self.sp)

    def create_experiment(self, ws: Workspace):
        experiment = Experiment(workspace=ws, name=self.aml_config.experiment_name)
        logger.info(f'Experiment created with name: {experiment.name}')
        return experiment

    def create_compute_target(self, workspace: Workspace):
        logger.info(f'Creating new compute target: {self.aml_config.compute_name}')

        compute_config = AmlCompute.provisioning_configuration(
            vm_size=self.aml_config.vm_size,
            max_nodes=self.aml_config.max_nodes
        )

        compute_target = ComputeTarget.create(workspace=workspace,
                                              name=self.aml_config.compute_name,
                                              compute_config=compute_config)
        compute_target.wait_for_completion(show_output=True)
        logger.info(f'Compute target created: {self.aml_config.compute_name}')
        return compute_target

    def get_or_create_compute_target(self, workspace: Workspace):
        try:
            compute_target = ComputeTarget(workspace=workspace,
                                           name=self.aml_config.compute_name)
            logger.info(
                f'Found existing compute target: {self.aml_config.compute_name}')
            return compute_target
        except ComputeTargetException:
            return self.create_compute_target(workspace)

    def create_datastore(self, workspace: Workspace):
        logger.info(f'Creating new datastore: {self.aml_config.datastore_name}')

        datastore = Datastore.register_azure_blob_container(
            workspace=workspace,
            datastore_name=self.aml_config.datastore_name,
            account_name=self.aml_config.storage_account_name,
            container_name=self.aml_config.container_name
        )
        logger.info(f'Datastore created: {self.aml_config.datastore_name}')
        return datastore

    def get_or_create_datastore(self, workspace: Workspace):
        try:
            datastore = Datastore.get(workspace=workspace,
                                      datastore_name=self.aml_config.datastore_name)
            logger.info(f'Found existing datastore: {self.aml_config.datastore_name}')
            return datastore
        except Exception:
            return self.create_datastore(workspace)

    def create_dataset(self, datastore: Datastore):
        dataset = Dataset.File.from_files(path=(datastore, self.aml_config.data_path))
        file_paths = dataset.to_path()
        num_files_to_print = min(5, len(file_paths))
        logger.info(f"First {num_files_to_print} files in the dataset:")
        for file_path in file_paths[:num_files_to_print]:
            logger.info(file_path)
        logger.info(f'Total number of files in the dataset: {len(file_paths)}')
        return dataset
