import logging

from aiogram import Bot, Dispatcher
from prometheus_client import REGISTRY, CollectorRegistry

from aiogram_prometheus.collectors import AiogramCollector

logger = logging.getLogger('faust_prometheus')


class AiogramPrometheusExporter(object):
    bot: Bot
    dp: Dispatcher

    def __init__(
        self,
        bot: Bot,
        dp: Dispatcher,
        registry: CollectorRegistry = REGISTRY,
        prefix: str = 'aiogram_',
    ) -> None:
        self.bot = bot
        self.dp = dp
        self.registry = registry

        self.registry.register(AiogramCollector(bot, dp, prefix))
