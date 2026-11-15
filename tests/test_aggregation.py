from resilio_eval.aggregation import aggregate_by_severity, robustness_summary

def test_robustness_summary():
    rows = [{"severity":0,"task_score":1.0},{"severity":1,"task_score":0.8},{"severity":2,"task_score":0.6}]
    summary = robustness_summary(aggregate_by_severity(rows))
    assert summary["baseline_score"] == 1.0
    assert abs(summary["normalized_robustness_auc"] - 0.8) < 1e-9
