from promptflow.core import tool


@tool
def select_metrics(selected_metrics: list[str]) -> dict[str, bool]:
    supported_metrics = ['gpt_relevance', 'gpt_groundedness', 'gpt_retrieval_score']
    return {metric: metric in selected_metrics for metric in supported_metrics}
