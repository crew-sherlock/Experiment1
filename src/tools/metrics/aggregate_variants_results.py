from promptflow.core import tool, log_metric
import numpy as np


@tool
def aggregate_variants_results(scores: list[dict[str, int]], metrics: list[list[str]]):
    input_metrics = metrics[0]

    aggregate_results = {}
    for score in scores:
        for name, value in score.items():
            if name not in aggregate_results.keys():
                aggregate_results[name] = []
            try:
                float_val = float(value)
            except Exception:
                float_val = np.nan
            aggregate_results[name].append(float_val)

    for name, value in aggregate_results.items():
        if name in input_metrics:
            metric_name = name
            aggregate_results[name] = np.nanmean(value)
            if 'pass_rate' in metric_name:
                metric_name = metric_name + "(%)"
                aggregate_results[name] = aggregate_results[name] * 100.0
            aggregate_results[name] = round(aggregate_results[name], 2)
            log_metric(metric_name, aggregate_results[name])

    return aggregate_results
