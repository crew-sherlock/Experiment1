# Registering data assets

There are several places we currently register data assets.

## Register inputs

Register experiment data asset in Azure ML as Data Asset.
This is a one-time setup that reads appropriate field values from experiment.yaml or
experiment.[env].yaml.
Use the following command to register the two datasets located
in experiment.yaml:

```bash
poetry run python -m llmops.common.register_data_asset \
            --subscription_id $AML_AZURE_SUBSCRIPTION_ID \
            --base_path $USE_CASE_BASE_PATH \
            --env_name dev
```

## Register evaluation data assets (output from the evaluation on the golden dataset)

The evaluation flow 'llmops.common.prompt_eval' is currently running the method:
`_register_final_results`.
This method takes the CSV files in the flow and register the files:
`
{experiment_name}_result.csv
`
in AML data.

The script is simple, this one uses the folder of the files but the file can be
registered on their own by changing the assetType and dir_path:

```python
from azure.ai.ml.entities import Data as AMLData
from azure.ai.ml.constants import AssetTypes as AMLAssetTypes

path = "reports"

result_data_asset = AMLData(
  path=path,
  type=AMLAssetTypes.URI_FILE,
  description="Experiment result data",
  name=f"{path.split('/')[1]}_result_data",
)

ml_client.data.create_or_update(result_data_asset)
```
