# Accountability Report Best practises

This document is a set of best practices captured across multiple GenAI projects and can be used as guidance towards compliance towards the AI SOP.

## Purpose of AI evaluation

The purpose of the evaluation framework is two fold:

- Ensure that the output generated by the AI is meeting the business expectations
- Comply with regulatory necessity to validate and monitor the AI systems.

As part of this article, we explain the evaluation strategy set in place to meet both above requirements.

## Success criteria

At the beginning of each project, it is very important to agree on the success criteria for the project. This will determine the validation metrics and strategy to put in place.

In general, the business needs can usually be met by ensuring that the AI output is :

- Grounded: into the context provided (no hallucination or out of context information) - the context in this case refers to the data provided to the AI system (unstructured and structured sources and instructions)
- Complete (relevant): ie encompassing all the information mentioned in the context (data sources) to answer the question (not omitting any relevant information)
- Properly formatted (accuracy): following code of conduct (non violent, adequate language (based on the persona), grammatically correct, concise, ethical, etc).
- The retrieved context is correct and complete

Given the unbounded and unstructured nature of Generative AI, there does not exist quantitative metrics capable to technically translate the above success criteria. Even though blue and rouge score exists and are quantitative metrics, they are way too narrow for the purpose of evaluating our complex application and are never used in practice (outside the realm of GenAI model development).

The agreed way to evaluate the GenAI applications is to use another LLM to score the output of the first one. It is proven that evaluating is a much easier task than generating hence not creating an inception loops of LLMs. You can even use a smaller model to evaluate the output from bigger models.

## Training data used

Usually, it is more efficient to put in place RAG systems rather than fine tune the models themselves. So usually, besides for few shot learning, no data is used to train the model per se and we rely on commercial provider to train the Generative AI models.

## Validation process

The validation process ensures that the quality of the AI system is under control and that the system operates as intended. In other words, it ensures that the success criteria are met.

To fine tune the AI system and determine the score and the metrics, we will go through an iterative and thorough validation of the metrics, the scores and the generated AI output by means of expert scoring and validation.

For more information on the how the stakeholders are expected to score the LLM output, check our [guide](../design/model-evaluation-success-criteria.md).

More information of the development and evaluation iterations, check our [lifecycle guide](../design/lifecycle.md)

## Monitoring & Maintenance

In order to ensure that the AI system operates as intended, we implement monitoring and maintenance measures.

- The metrics that we have implemented to evaluate the systems are calculated for each answer generated. These metrics are used in the system to warn the user of the quality of the output: if the metrics are not >=4, the user should be warned of the poor quality of the output or no output should be given to the user.
- Furthermore, these metrics are logged into App Insights and AppInsights metrics are calculated over a rolling window of 100 answers generated (App Insights Metrics - AIM). Based on the AIM rolling windows, we do have alerts if they go below the threshold of 4. These alerts are sent to L3 support GenAI that then investigates and proactively takes action to resolve the content drift.
- Once a change is implemented, to ensure robustness of the new changes, we evaluate them over our Golden Dataset (this happens automatically in our CI pipeline). The change is then deployed to production ONLY if the evaluation of the change on the Golden Dataset has metrics  >=4. There is a human in the loop validating that the metrics are meeting expectations and then releasing the new code in production (CD pipeline  is implemented for automatic deployment).

## AI Risks and Mitigations

Below is a list of the main risks with GenAI applications and their mitigation strategies.

|Risk|Explanation|Mitigation(s)|
|-------|-------------|---------------|
| Model Migration | The models are quickly decommissioned since this is a fairly new landscape and models are being released often. This risk considers only the case of redeployment of the same code, with a new model. It does not cover the implementation of new features as this follows the entire validation process again. | The golden dataset collected serves to be able to run the offline evaluation and assess whether the tool can be deployed robustly. Indeed the evaluation is integrated in the CI pipeline so it should be quick to validate a new model release and make the appropriate changes |
| Data Migration | For example new documents and data are arising, and the previous data sources become obsolete | For each data source, there should be period refresh (decided upon the business needs). For each new data source, that wants to be added into the tool, this should be a change request (should be in PI planning). We will thoroughly document the process of adding a new data table |
|Usage of GenAI embedded into third party supplier: Genie Space | The usage of Genie space for example does not allow us to control their release lifecycle. This might have an impact on the performance of the system. | **Mitigations we have at an enterprise level (refer to CO accountability report)**:Attached is the security and architecture for DatabricksIQ (the backing behind Genie, AI Assistant, ect.). They use Azure OpenAI behind the scenes and not a custom developed model that they will be changing over time. We will receive updates before major model changes (i.e. GPT4 to GPT5 once it is released). **Additional mitigations you can do at a project level:** Follow the directions to curate a high quality Genie Space. Add Instructions and even more importantly example questions and corresponding, correct SQL queries. If it REALLY needs to get something right, add Trusted Assets which are basically predefined SQL Functions. This way Genie doesn't generate SQL at all but instead runs those predefined functions, and then it shows the user it is using a Trusted Asset to answer the question |
|Content / Data drift| The content of the data sources might drift (change over time) and the answer from the AI model would no longer be accurate | The metrics in App Insight will allow to detect this type of drift. Once this happens, the L3 support will investigate for root cause and take action in collaboration with the business stakeholders.|
| Human input|The system is not supposed to handle CSI data, nor PII data and this will be mentioned into the interface. Nevertheless, given that this is a chatbot, we can not control what the users input into the tool. The human could also input violent or inappropriate content. | We will implement content safety filters, to detect cases of violence, or inappropriate usage of the tool. The tool will then be prompted to refuse to answer to the question. These will be logged and abusive usage of the tool will be monitored and could be sanctioned. Implement a banner reminding people that the information they input into the chat will be used into AI |
| Model Maturity |An answer is generated however the content is incorrect due to AI inaccurate output. Even though we thoroughly test the system, we can never guarantee a 100% accuracy.| The human will be trained and warned to use critical thinking and not to take the output of the AI for granted. The Human is end responsible to use the output generated by the AI. A feedback button will be implemented to allow users to feedback improvements into the system. Furthermore, the assistant will cite its sources so that the user is aware of the extent of the knowledge of the assistant and can take an informed decision on the output |
|Data access | The model could output data for which the user doesn't have access| We need to follow an identification chain throughout the backend until the data layer, to ensure that only data that the users are supposed to access are forwarded to the LLM and that the answer to the question from the user is only grounded into the right data|

Within AIGA, you find a lot of the mitigation actions already embedded or the framework easy to extend.
