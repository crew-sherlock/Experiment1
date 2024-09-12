import logging
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.core.schedule import ScheduleRecurrence, Schedule

from aml_config import AMLConfig
from aml_api import AMLApi
from components.chunking_component import ChunkingComponent
from components.create_index_component import CreateIndexComponent
from components.generate_embeddings_component import GenerateEmbeddingsComponent
from components.index_documents_component import IndexDocumentsComponent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

aml_config = AMLConfig('aml_pipeline_config.json')

sp = ServicePrincipalAuthentication(
    aml_config.tenant_id, aml_config.service_principal_id,
    aml_config.service_principal_password,
    cloud='AzureCloud', _enable_caching=True
)

aml_api = AMLApi(aml_config, sp)

try:
    ws = aml_api.get_workspace()
    experiment = aml_api.create_experiment(ws)

    run_config = aml_config.convert_to_run_config(env_name="document-loading-env")

    compute_target = aml_api.get_or_create_compute_target(workspace=ws)

    datastore = aml_api.get_or_create_datastore(workspace=ws)
    dataset = aml_api.create_dataset(datastore)

    chunking_output_dir = PipelineData(name="output_dir",
                                       datastore=ws.get_default_datastore())
    logger.info(f"Chunking output directory: {chunking_output_dir._datastore}")

    embedding_output_dir = PipelineData(name="output_dir",
                                        datastore=ws.get_default_datastore())
    logger.info(f"Embedding output directory: {embedding_output_dir._datastore}")

    chunk_step = ChunkingComponent.build_step(
        aml_config=aml_config, compute_target=compute_target, dataset=dataset,
        chunking_output_dir=chunking_output_dir, run_config=run_config)

    create_index_step = CreateIndexComponent.build_step(
        aml_config=aml_config, compute_target=compute_target, run_config=run_config)

    generate_embedding_step = GenerateEmbeddingsComponent.build_step(
        aml_config=aml_config, compute_target=compute_target,
        embedding_output_dir=embedding_output_dir,
        chunking_output_dir=chunking_output_dir, run_config=run_config)

    index_documents_step = IndexDocumentsComponent.build_step(
        aml_config=aml_config, compute_target=compute_target,
        embedding_output_dir=embedding_output_dir, run_config=run_config)

    pipeline = Pipeline(workspace=ws, steps=[
        chunk_step, create_index_step, generate_embedding_step,
        index_documents_step
    ])

    pipeline_run = experiment.submit(pipeline)
    pipeline_run.wait_for_completion(show_output=True)

    published_pipeline = pipeline.publish(
        name="Document_Loading_Pipeline",
        description="Pipeline to load documents into Azure Search",
        version="1.0")
    recurrence = ScheduleRecurrence(frequency="Day", interval=1)
    recurring_schedule = Schedule.create(ws, name="MyRecurringSchedule",
                                         description="Based on time",
                                         pipeline_id=published_pipeline.id,
                                         experiment_name=aml_config.experiment_name,
                                         recurrence=recurrence)

except Exception as e:
    logger.error(f'AML Pipeline Failed: {e}')
