from resilio_eval.core.schemas import EvalCase
from resilio_eval.perturbations import TypoPerturbation, FormattingPerturbation, TruncationPerturbation

def test_seed_is_reproducible():
    case = EvalCase("x", "qa", "Explain reliable electricity grids.")
    a = TypoPerturbation(0.3).generate(case, severity=1, variant=1)
    b = TypoPerturbation(0.3).generate(case, severity=1, variant=1)
    assert a.input == b.input
    assert a.seed == b.seed

def test_truncation_marks_intent_not_preserved():
    case = EvalCase("x", "qa", "Explain how solar energy improves grid reliability.")
    record = TruncationPerturbation(0.5).generate(case)
    assert record.semantics_preserving is False

def test_formatting():
    p = FormattingPerturbation()
    assert p.apply("HELLO   World", __import__('random').Random(1)) == "hello world"
