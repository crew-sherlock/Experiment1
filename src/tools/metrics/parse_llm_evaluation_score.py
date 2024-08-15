import json
import numpy as np

from promptflow.core import tool


@tool
def parse_llm_evaluation_score(llm_evaluation_score: str) -> dict[str, str]:
    try:
        evaluation_score = json.loads(llm_evaluation_score)
        return {
            "score": evaluation_score.get("score", np.nan),
            "reason": evaluation_score.get("reason", "Reason not found.")
        }
    except Exception:
        return {
            "score": np.nan,
            "reason": "Error parsing metric output."
        }
