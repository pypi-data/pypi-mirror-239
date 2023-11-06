import abc
import asyncio
import logging
import time
from asyncio import AbstractEventLoop
from typing import Optional

from prometheus_client import REGISTRY, CollectorRegistry

from prometheus_client_utils.collectors.push_clients import PushClientsCollector

logger = logging.getLogger('prometheus_client_utils')


class BasePushClient(abc.ABC):
    address: str
    job: str
    registry: CollectorRegistry

    _schedule_task: asyncio.Task

    def __init__(self, address: str, job: str, registry: CollectorRegistry = REGISTRY) -> None:
        self.address = address
        self.job = job
        self.registry = registry

        self.collector = PushClientsCollector()

        registry.register(self.collector)

    @abc.abstractmethod
    async def push(self):
        pass

    async def __schedule_push(self, on_time: int = 15):
        _on_time_original = on_time
        while True:
            await asyncio.sleep(on_time)

            _start_time = time.time()

            try:
                await self.push()

            except BaseException as ex:
                logger.debug(ex)

                if isinstance(ex, asyncio.CancelledError):
                    break

                self.collector.was_fail_push()
                on_time += _on_time_original

            else:
                on_time = _on_time_original

            self.collector.was_push(time.time() - _start_time)

    def schedule_push(self, on_time: int = 15, loop: Optional[AbstractEventLoop] = None):
        """Отправка метрик раз в on_time секунд

        Args:
            on_time (int, optional): Seconds

        """

        if loop is None:
            loop = asyncio.get_event_loop()

        self._schedule_task = loop.create_task(self.__schedule_push(on_time))
