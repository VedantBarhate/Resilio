from .base import Metric
from ..core.schemas import MetricResult
class ExactMatchMetric(Metric):
    name = "exact_match"
    def __init__(self, case_sensitive=False): self.case_sensitive = case_sensitive
    def compute(self, case, response, **kwargs):
        reference = case.expected_output or case.expected_label
        if reference is None: return MetricResult(self.name, None, "0_to_1", True, {"reason": "no reference output or label"})
        a, b = response.text.strip(), reference.strip()
        if not self.case_sensitive: a, b = a.casefold(), b.casefold()
        value = float(a == b)
        return MetricResult(self.name, value, "0_to_1", True, {"match": bool(value), "reference": reference})
