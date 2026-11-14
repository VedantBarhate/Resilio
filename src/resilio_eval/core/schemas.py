from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass(slots=True)
class EvalCase:
    id: str
    task: str
    input: str
    expected_output: str | None = None
    expected_label: str | None = None
    context: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.id.strip() or not self.task.strip() or not self.input.strip():
            raise ValueError("EvalCase id, task and input must be non-empty")

@dataclass(slots=True)
class PerturbationRecord:
    id: str
    base_case_id: str
    family: str
    severity: int
    variant: int
    input: str
    semantics_preserving: bool | None
    seed: int
    parameters: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class ModelResponse:
    text: str
    model_id: str = "unknown"
    provider: str = "custom"
    input_tokens: int | None = None
    output_tokens: int | None = None
    latency_seconds: float | None = None
    time_to_first_token_seconds: float | None = None
    finish_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class MetricResult:
    metric: str
    value: float | None
    scale: str
    higher_is_better: bool | None
    details: dict[str, Any] = field(default_factory=dict)
    metric_version: str = "0.1.0"

@dataclass(slots=True)
class ExperimentResult:
    run_id: str
    records: list[dict[str, Any]]
    aggregates: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)

    def save(self, directory: str):
        import json
        from pathlib import Path
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        (path / "records.json").write_text(json.dumps(self.records, indent=2, ensure_ascii=False), encoding="utf-8")
        (path / "aggregates.json").write_text(json.dumps(self.aggregates, indent=2, ensure_ascii=False), encoding="utf-8")
        (path / "manifest.json").write_text(json.dumps({"run_id": self.run_id, **self.metadata}, indent=2), encoding="utf-8")
