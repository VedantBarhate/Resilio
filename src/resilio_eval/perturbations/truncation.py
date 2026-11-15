from .base import Perturbation

class TruncationPerturbation(Perturbation):
    family = "truncation"
    semantics_preserving = False
    def __init__(self, keep_fraction: float = 0.75):
        if not 0 < keep_fraction < 1: raise ValueError("keep_fraction must be between 0 and 1")
        self.keep_fraction = keep_fraction
    def parameters(self): return {"keep_fraction": self.keep_fraction}
    def apply(self, text, rng):
        words = text.split()
        if len(words) < 2: return text
        return " ".join(words[:max(1, int(len(words) * self.keep_fraction))])
