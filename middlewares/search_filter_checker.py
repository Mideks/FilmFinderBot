from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from search_filters import SearchFilters


class SearchFilterChecker(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        state: FSMContext = data["state"]
        state_data = await state.get_data()
        if "search_filters" not in state_data:
            await state.update_data(search_filters=SearchFilters())

        return await handler(event, data)