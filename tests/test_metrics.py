from resilio_eval.core.schemas import EvalCase, ModelResponse
from resilio_eval.metrics import ExactMatchMetric, ClassificationAccuracy, LexicalSimilarity

def test_exact_match():
    case = EvalCase("1", "qa", "question", expected_output="42")
    assert ExactMatchMetric().compute(case, ModelResponse("42")).value == 1.0

def test_classification_accuracy():
    case = EvalCase("1", "classification", "classify", expected_label="B2B")
    assert ClassificationAccuracy().compute(case, ModelResponse("B2B")).value == 1.0

def test_similarity_is_separate_signal():
    case = EvalCase("1", "qa", "question")
    result = LexicalSimilarity().compute(case, ModelResponse("solar grid"), baseline=ModelResponse("solar grid"))
    assert result.value == 1.0
