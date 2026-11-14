import json
from pathlib import Path
from ..core.schemas import EvalCase

def load_json(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict): data = data.get("cases", data.get("prompts", []))
    if not isinstance(data, list): raise ValueError("Dataset JSON must be a list or contain a 'cases' list")
    cases = []
    for i, row in enumerate(data):
        prompt = row.get("input", row.get("prompt", row.get("ideal_prompt")))
        if prompt is None: raise ValueError(f"Record {i} has no input/prompt field")
        cases.append(EvalCase(id=str(row.get("id", row.get("prompt_id", i))), task=str(row.get("task", row.get("category", "general"))), input=str(prompt), expected_output=row.get("expected_output", row.get("ideal_response")), expected_label=row.get("expected_label", row.get("label")), context=row.get("context"), metadata={k:v for k,v in row.items() if k not in {"id","prompt_id","task","category","input","prompt","ideal_prompt","expected_output","ideal_response","expected_label","label","context"}}))
    return cases
