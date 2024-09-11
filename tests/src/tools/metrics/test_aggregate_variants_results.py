from unittest.mock import MagicMock, patch
from src.tools.metrics.aggregate_variants_results import aggregate_variants_results


METRICS = [['gpt_relevance', 'gpt_groundedness', 'gpt_retrieval_score']]


def test_aggregate_variants_results_returns_empty_array_with_no_results():
    result = aggregate_variants_results([], METRICS)

    assert result == {}


def test_aggregate_variants_results_returns_aggregate_when_given_one_variant():
    scores = [
        {"gpt_relevance": 3, "gpt_groundedness": 2, "gpt_retrieval_score": 5}
    ]

    result = aggregate_variants_results(scores, METRICS)

    assert result == {
        "gpt_relevance": 3.0,
        "gpt_groundedness": 2.0,
        "gpt_retrieval_score": 5.0
    }


def test_aggregate_variants_results_returns_aggregate_when_given_multiple_variants():
    scores = [
        {"gpt_relevance": 3, "gpt_groundedness": 2, "gpt_retrieval_score": 5},
        {"gpt_relevance": 4, "gpt_groundedness": 1, "gpt_retrieval_score": 4}
    ]

    result = aggregate_variants_results(scores, METRICS)

    assert result == {
        "gpt_relevance": 3.5,
        "gpt_groundedness": 1.5,
        "gpt_retrieval_score": 4.5
    }


@patch('src.tools.metrics.aggregate_variants_results.log_metric')
def test_aggregate_variants_results_calls_log_metric_when_given_multiple_variants(
    mock_log_metric: MagicMock
):
    scores = [
        {"gpt_relevance": 3, "gpt_groundedness": 2, "gpt_retrieval_score": 5},
        {"gpt_relevance": 4, "gpt_groundedness": 1, "gpt_retrieval_score": 4}
    ]

    aggregate_variants_results(scores, METRICS)

    expected_logged_metrics = {
        "gpt_relevance": 3.5,
        "gpt_groundedness": 1.5,
        "gpt_retrieval_score": 4.5
    }
    assert mock_log_metric.call_count == 3
    for metric_name, value in expected_logged_metrics.items():
        mock_log_metric.assert_any_call(metric_name, value)


def test_aggregate_variants_results_handles_nan_when_given_invalid_input():
    scores = [
        {"gpt_relevance": 3, "gpt_groundedness": 2, "gpt_retrieval_score": "testing"},
        {"gpt_relevance": 4, "gpt_groundedness": 1, "gpt_retrieval_score": 4}
    ]

    result = aggregate_variants_results(scores, METRICS)

    assert result == {
        "gpt_relevance": 3.5,
        "gpt_groundedness": 1.5,
        "gpt_retrieval_score": 4
    }


def test_aggregate_variants_results_handles_pass_rate_metrics():
    scores = [
        {"example_pass_rate": 0.345}
    ]

    result = aggregate_variants_results(scores, [['example_pass_rate']])

    assert result == {
        "example_pass_rate": 34.5
    }


@patch('src.tools.metrics.aggregate_variants_results.log_metric')
def test_aggregate_variants_results_calls_log_metric_when_given_pass_rate(
    mock_log_metric
):
    scores = [
        {"example_pass_rate": 0.345}
    ]

    aggregate_variants_results(scores, [['example_pass_rate']])

    mock_log_metric.assert_called_once_with("example_pass_rate(%)", 34.5)
