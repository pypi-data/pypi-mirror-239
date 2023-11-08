from typing import Any, Awaitable, Callable, Coroutine, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class MetricsBaseMiddleware(BaseMiddleware):
    """Промежуточный слой для сборка метрик"""

    def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        return super().__call__(handler, event, data)
