from .base import Perturbation

class FormattingPerturbation(Perturbation):
    family = "formatting"
    semantics_preserving = True
    def __init__(self, lowercase: bool = True, remove_punctuation: bool = False, collapse_spaces: bool = True):
        self.lowercase, self.remove_punctuation, self.collapse_spaces = lowercase, remove_punctuation, collapse_spaces
    def parameters(self): return {"lowercase": self.lowercase, "remove_punctuation": self.remove_punctuation, "collapse_spaces": self.collapse_spaces}
    def apply(self, text, rng):
        import re, string
        if self.lowercase: text = text.lower()
        if self.remove_punctuation: text = text.translate(str.maketrans("", "", string.punctuation))
        if self.collapse_spaces: text = re.sub(r"\s+", " ", text).strip()
        return text
