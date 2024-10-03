# AIGA lifecycle

The process of developing a GenAI products goes like:

![cycle](./assets/Lifecycle_with_tech.svg)

- Once the business requirements (including the success criteria) have been captured, we need to collect a sample of data which should be placed on blob storage for safety and reusability.
- The basic document processing pipelines, prompts and flows can be built. Refer to [running promptflow](../onboarding/running-promptflow.md) & [document loading](../design/document-loading.md)
- Based on the payload from the flows, we create a test set (identified by the business as candidates for the golden dataset). The test set is a json file.
- With the test set, we run the pipeline and flows in order to generate the output *generated-ai-output.jsonl*
- The *generated-ai-output.jsonl* can be converted into an Excel sheet for easy sharing with business users. This can be accomplished by using the provided [script](https://github.com/gsk-tech/AIGA/blob/main/llmops/common/jsonl_converter.py), which ensures the data is presented in a user-friendly format, facilitating review and feedback. Please refer [convert-jsonl.MD](../onboarding/convert-jsonl.md) for more documentation.
- The metrics defined by the business are included in the inference flow and the generated AI output is evaluated against these. Check [how to add a metric](../onboarding/adding-metrics.md)
- If the metrics do not meet expectations, we will optimise the pipelines and flows
- If the metrics do meet expectations, we will collect feedback from the SME's, using an excel file. Check the [guide](./model-evaluation-success-criteria.md)
- With the feedback from the business, we will go back to optimising the pipelines, flows and prompts
- Once we have reached satisfactory level, we consider the validated output from business the Golden Dataset
- Before deploying a flow, the offline evaluation flow (comparing the AI generated output and the golden dataset) will always run
- Once the metrics and flows have been logged and validated, the flows and pipelines can be deployed with our [CI & CD pipelines](../onboarding/deployment.md), following  [LLMOPs](../onboarding/llmops.md)
- While running as usual, the online metrics are [captured into App Insights](../onboarding/observability.md) and [metrics and alerts](../onboarding/alerting.md) are implemented
- If an alert is triggered or if an incident is raised by the users, the Root Cause Analysis will start
- We will go back to optimising the pipelines and flows, and straight to the production flow, skipping the evaluation flow since we do already have a Golden Dataset

In practice, multiple rounds are necessary between Experimentation and Evaluation, to refine the metrics and fine tune the flows and pipelines to get the desired output. Also usually, the Golden Dataset is not built in one go, it will be iteratively built, as more features are added (for example translation could be added).
