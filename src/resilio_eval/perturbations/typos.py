from .base import Perturbation

class TypoPerturbation(Perturbation):
    family = "typo"
    semantics_preserving = True
    def __init__(self, rate: float = 0.05):
        if not 0 <= rate <= 1: raise ValueError("rate must be between 0 and 1")
        self.rate = rate
    def parameters(self): return {"rate": self.rate}
    def apply(self, text, rng):
        chars = list(text)
        candidates = [i for i, c in enumerate(chars) if c.isalpha()]
        count = min(len(candidates), round(len(candidates) * self.rate))
        for i in rng.sample(candidates, count):
            c = chars[i]
            alphabet = "abcdefghijklmnopqrstuvwxyz" if c.islower() else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            replacement = rng.choice(alphabet.replace(c, ""))
            chars[i] = replacement
        return "".join(chars)
