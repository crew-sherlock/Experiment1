from src.tools.metrics.select_metrics import select_metrics


def test_select_metrics_returns_filtered_map_when_given_selection():
    selected_metrics = ["gpt_relevance"]

    result = select_metrics(selected_metrics)

    assert result == {
        "gpt_relevance": True,
        "gpt_groundedness": False,
        "gpt_retrieval_score": False
    }


def test_select_metrics_ignores_invalid_selection():
    selected_metrics = ["gpt_groundedness", "invalid_metric"]

    result = select_metrics(selected_metrics)

    assert result == {
        "gpt_relevance": False,
        "gpt_groundedness": True,
        "gpt_retrieval_score": False
    }
