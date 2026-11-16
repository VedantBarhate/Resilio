# Resilio Eval implementation status

This repository preserves the original Resilio research pipeline and adds an initial executable `resilio_eval` package.

## Implemented in this starter release
- Typed evaluation case, perturbation, response and result records.
- Stable SHA-256-derived perturbation seeds.
- Typo, formatting and truncation perturbations.
- Callable model adapter protocol.
- Exact-match, simple classification accuracy and lexical response similarity metrics.
- Clean-baseline and perturbed inference orchestration.
- Severity aggregation, performance retention, absolute drop and normalized trapezoidal AUC.
- JSON result export, JSON dataset loading and dataset-validation CLI.
- Unit tests and a runnable quickstart example.

## Not implemented yet
- Hugging Face Transformers and OpenAI-compatible provider adapters.
- Embedding-based cosine similarity (installable optional dependency is reserved but implementation remains future work).
- LLM-as-a-Judge and human calibration workflows.
- RAG, agent-trace, safety and multilingual evaluation profiles.
- Robust statistical confidence intervals and bootstrap by base prompt.
- Full CLI experiment configuration and resume/caching.

The API is an MVP implementation, not a claim that every interface in `LIBRARY_DESIGN.md` is already available. Treat the original notebooks and exported results as the historical research experiment; use the package for the new reproducible evaluation workflow.
