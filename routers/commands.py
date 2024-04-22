from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import get_menu_keyboard
from search_filters import SearchFilters

router = Router()


# todo: delete old bot message, if we know it
@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.update_data(search_filters=SearchFilters())
    await message.answer(
        f"Добро пожаловать, пользователь!\n"
        f"Я бот для поиска фильмов и сериалов."
        f" Вы можете искать фильмы по различным фильтрам или даже по кадру.\n"
        f"Чтобы начать поиск, нажми на кнопку ниже.",
        reply_markup=get_menu_keyboard())
    await message.delete()
