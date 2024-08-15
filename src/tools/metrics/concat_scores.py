import numpy as np

from promptflow.core import tool


@tool(enable_kwargs=True)
def concat_scores(**kwargs) -> dict[str, float]:
    return {metric: value.get("score", np.nan) for metric, value in kwargs.items()}
