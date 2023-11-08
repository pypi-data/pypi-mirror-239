from typing import Iterable

from aiogram import Bot, Dispatcher
from prometheus_client.metrics_core import Metric
from prometheus_client.registry import Collector


class AiogramCollector(Collector):
    def __init__(self, bot: Bot, dp: Dispatcher, prefix: str = 'aiogram_') -> None:
        self.bot = bot
        self.dp = dp

    def collect(self) -> Iterable[Metric]:
        pass
