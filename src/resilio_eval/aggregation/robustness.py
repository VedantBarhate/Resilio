def aggregate_by_severity(records, metric="task_score"):
    grouped = {}
    for row in records:
        value = row.get(metric)
        if value is None: continue
        grouped.setdefault(int(row.get("severity", 0)), []).append(float(value))
    return {level: {"mean": sum(vals)/len(vals), "count": len(vals), "min": min(vals), "max": max(vals)} for level, vals in sorted(grouped.items()) if vals}

def robustness_summary(by_severity):
    if not by_severity: return {}
    levels = sorted(by_severity)
    baseline = by_severity.get(0, by_severity[levels[0]])["mean"]
    curve = []
    for level in levels:
        score = by_severity[level]["mean"]
        retention = score / baseline if baseline > 0 else None
        curve.append({"severity": level, "score": score, "absolute_drop": baseline-score, "retention": retention})
    # Trapezoidal AUC over observed severity, normalized by severity span.
    if len(curve) >= 2 and levels[-1] > levels[0]:
        xs = [float(x["severity"]) for x in curve]
        ys = [float(x["retention"]) if x["retention"] is not None else 0.0 for x in curve]
        area = sum((xs[i+1]-xs[i])*(ys[i]+ys[i+1])/2 for i in range(len(xs)-1)) / (xs[-1]-xs[0])
    else: area = None
    return {"baseline_score": baseline, "curve": curve, "normalized_robustness_auc": area, "worst_case_score": min(x["score"] for x in curve)}
