from .base import Metric
from ..core.schemas import MetricResult

class LexicalSimilarity(Metric):
    """Dependency-free token-set Jaccard similarity; not a correctness metric."""
    name = "response_lexical_similarity"
    def compute(self, case, response, baseline=None, **kwargs):
        if baseline is None: return MetricResult(self.name, None, "0_to_1", True, {"reason": "baseline response missing"})
        a, b = set(case_tokens(response.text)), set(case_tokens(baseline.text))
        value = len(a & b) / len(a | b) if a | b else 1.0
        return MetricResult(self.name, value, "0_to_1", True, {"interpretation": "lexical overlap only; not correctness"})

def case_tokens(text): return [x.casefold() for x in text.split() if x.strip()]
