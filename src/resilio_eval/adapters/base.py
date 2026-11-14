from abc import ABC, abstractmethod
from time import perf_counter
from ..core.schemas import ModelResponse

class ModelAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str, **generation_config) -> ModelResponse: ...

class CallableAdapter(ModelAdapter):
    """Wrap a user function as an adapter; useful for tests and custom runtimes."""
    def __init__(self, function, model_id="callable"):
        self.function, self.model_id = function, model_id
    def generate(self, prompt: str, **generation_config):
        start = perf_counter()
        output = self.function(prompt, **generation_config)
        elapsed = perf_counter() - start
        if isinstance(output, ModelResponse): return output
        return ModelResponse(text=str(output), model_id=self.model_id, latency_seconds=elapsed)
