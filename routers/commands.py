from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import get_menu_keyboard
from search_filters import SearchFilters

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(search_filters=SearchFilters())
    await message.answer(f"Добро пожаловать! Я бот для поиска фильмов и сериалов!",
                         reply_markup=get_menu_keyboard())