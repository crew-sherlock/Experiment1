import numpy as np
from src.tools.metrics.concat_scores import concat_scores


def test_concat_scores_maps_metrics_when_provided_in_dicts():
    scores = concat_scores(
        gpt_relevance={"score": 2},
        gpt_groundedness={"score": 3},
        gpt_retrieval_score={"score": 4}
    )

    assert scores == {
        "gpt_relevance": 2,
        "gpt_groundedness": 3,
        "gpt_retrieval_score": 4
    }


def test_concat_scores_uses_default_value_when_score_is_not_provided_in_dicts():
    scores = concat_scores(
        gpt_relevance={"score": 2},
        gpt_groundedness={"score-ish": 3},
        gpt_retrieval_score={"score": 4}
    )

    assert scores == {
        "gpt_relevance": 2,
        "gpt_groundedness": np.nan,
        "gpt_retrieval_score": 4
    }


def test_concat_scores_uses_default_value_when_score_is_none_in_dicts():
    scores = concat_scores(
        gpt_relevance={"score": 2},
        gpt_groundedness={"score-ish": None},
        gpt_retrieval_score={"score": 4}
    )

    assert scores == {
        "gpt_relevance": 2,
        "gpt_groundedness": np.nan,
        "gpt_retrieval_score": 4
    }
