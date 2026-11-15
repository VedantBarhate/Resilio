from .base import Metric
from ..core.schemas import MetricResult
class ClassificationAccuracy(Metric):
    name = "classification_accuracy"
    def __init__(self, labels=None): self.labels = labels
    def compute(self, case, response, **kwargs):
        if case.expected_label is None: return MetricResult(self.name, None, "0_to_1", True, {"reason": "expected_label missing"})
        pred = response.text.strip().splitlines()[0].strip().strip(". ").casefold()
        gold = case.expected_label.strip().casefold()
        if self.labels:
            matches = [label for label in self.labels if label.casefold() in pred]
            pred = matches[0].casefold() if len(matches) == 1 else pred
        value = float(pred == gold)
        return MetricResult(self.name, value, "0_to_1", True, {"prediction": pred, "expected": gold})
