from abc import ABC, abstractmethod
from ..core.schemas import MetricResult
class Metric(ABC):
    name = "metric"
    @abstractmethod
    def compute(self, case, response, **kwargs) -> MetricResult: ...
