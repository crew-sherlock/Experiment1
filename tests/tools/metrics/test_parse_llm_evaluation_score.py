import numpy as np
from src.tools.metrics.parse_llm_evaluation_score import parse_llm_evaluation_score


def test_parse_llm_evaluation_score_returns_mapped_dict_when_given_str():
    llm_evaluation_score = '{"score": 2, "reason": "Reason."}'

    result = parse_llm_evaluation_score(llm_evaluation_score)

    assert result == {
        "score": 2,
        "reason": "Reason."
    }


def test_parse_llm_evaluation_score_uses_default_score():
    llm_evaluation_score = '{"score-ish": 2, "reason": "Reason."}'

    result = parse_llm_evaluation_score(llm_evaluation_score)

    assert result == {
        "score": np.nan,
        "reason": "Reason."
    }


def test_parse_llm_evaluation_score_uses_default_reason():
    llm_evaluation_score = '{"score": 2, "reason-ish": "Reason."}'

    result = parse_llm_evaluation_score(llm_evaluation_score)

    assert result == {
        "score": 2,
        "reason": "Reason not found."
    }


def test_parse_llm_evaluation_score_handles_error():
    invalid_json = '{"score": 2, "reason-ish": "Reason."]'

    result = parse_llm_evaluation_score(invalid_json)

    assert result == {
        "score": np.nan,
        "reason": "Error parsing metric output."
    }
