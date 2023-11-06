from typing import Iterable

from prometheus_client import Counter, Histogram
from prometheus_client.metrics_core import Metric
from prometheus_client.registry import Collector


class PushClientsCollector(Collector):
    prefix: str = 'python_prometheus_push_'

    def __init__(self) -> None:
        super().__init__()

        self.m_requests = Counter(
            f'{self.prefix}requests',
            'Count of push requests',
            registry=None,
        )
        self.m_requests_time = Histogram(
            f'{self.prefix}requests_time',
            'Histogram about time push requests',
            registry=None,
        )
        self.m_failed_requests = Counter(
            f'{self.prefix}failed_requests',
            'Count of failed push requests',
            registry=None,
        )

    def was_push(self, execute_time: float):
        self.m_requests.inc()
        self.m_requests_time.observe(execute_time)

    def was_fail_push(self):
        self.m_failed_requests.inc()

    def collect(self) -> Iterable[Metric]:
        yield from self.m_requests.collect()
        yield from self.m_requests_time.collect()
        yield from self.m_failed_requests.collect()
