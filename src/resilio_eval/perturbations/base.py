from abc import ABC, abstractmethod
from ..core.schemas import EvalCase, PerturbationRecord
from .utils import stable_seed

class Perturbation(ABC):
    family = "base"
    semantics_preserving: bool | None = None
    @abstractmethod
    def apply(self, text: str, rng): ...
    def generate(self, case: EvalCase, severity: int = 1, variant: int = 1, seed: int | None = None):
        import random
        actual_seed = seed if seed is not None else stable_seed(case.id, self.family, severity, variant)
        rng = random.Random(actual_seed)
        changed = self.apply(case.input, rng)
        return PerturbationRecord(f"{case.id}__{self.family}__s{severity}__v{variant}", case.id, self.family, severity, variant, changed, self.semantics_preserving, actual_seed, self.parameters())
    def parameters(self): return {}
