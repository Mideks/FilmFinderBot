from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from callback_buttons import NavigateButton, NavigateButtonLocation
from keyboards import get_search_film_filters_menu_keyboard

router = Router()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.Search))
async def search_film_filters_menu_handler(message: Message) -> None:
    await message.message.answer(
        "Введите фильм, который хотите найти, или выберите по критериям ниже",
        reply_markup=get_search_film_filters_menu_keyboard()
    )
