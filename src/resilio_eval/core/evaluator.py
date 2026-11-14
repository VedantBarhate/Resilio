from dataclasses import dataclass, field
from uuid import uuid4
from ..core.schemas import ExperimentResult
from ..perturbations.utils import stable_seed
from ..aggregation.robustness import aggregate_by_severity, robustness_summary

@dataclass
class ExperimentConfig:
    perturbations: list = field(default_factory=list)
    variants_per_perturbation: int = 2
    repetitions: int = 1
    seed: int = 42
    metrics: list = field(default_factory=list)
    generation_config: dict = field(default_factory=dict)

class Evaluator:
    def __init__(self, adapter): self.adapter = adapter
    def run(self, cases, config: ExperimentConfig):
        if config.variants_per_perturbation < 1 or config.repetitions < 1: raise ValueError("variants_per_perturbation and repetitions must be >= 1")
        run_id = str(uuid4())
        records = []
        for case in cases:
            baseline = self.adapter.generate(case.input, **config.generation_config)
            baseline_metrics = [m.compute(case, baseline) for m in config.metrics]
            base_row = {"case_id": case.id, "task": case.task, "family": "clean", "severity": 0, "variant": 0, "repetition": 0, "prompt": case.input, "response": baseline.text, "model_id": baseline.model_id, "latency_seconds": baseline.latency_seconds}
            for metric in baseline_metrics:
                base_row[metric.metric] = metric.value
            base_row["task_score"] = next((m.value for m in baseline_metrics if m.value is not None), None)
            records.append(base_row)
            for perturbation in config.perturbations:
                for variant in range(1, config.variants_per_perturbation + 1):
                    p = perturbation.generate(case, severity=variant, variant=variant, seed=stable_seed(case.id, perturbation.family, variant, config.seed))
                    for repetition in range(config.repetitions):
                        response = self.adapter.generate(p.input, **config.generation_config)
                        row = {"case_id": case.id, "task": case.task, "family": p.family, "severity": p.severity, "variant": p.variant, "repetition": repetition, "prompt": p.input, "response": response.text, "model_id": response.model_id, "latency_seconds": response.latency_seconds, "semantics_preserving": p.semantics_preserving, "seed": p.seed}
                        results = [m.compute(case, response, baseline=baseline) for m in config.metrics]
                        for metric in results: row[metric.metric] = metric.value
                        row["task_score"] = next((m.value for m in results if m.value is not None), None)
                        records.append(row)
        grouped = aggregate_by_severity(records, "task_score")
        aggregates = {"task_score": robustness_summary(grouped), "by_severity": grouped}
        return ExperimentResult(run_id, records, aggregates, {"model_id": getattr(self.adapter, "model_id", "unknown"), "variants_per_perturbation": config.variants_per_perturbation, "repetitions": config.repetitions, "seed": config.seed})
