from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards import get_menu_keyboard

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Добро пожаловать! Я бот для поиска фильмов и сериалов!",
                         reply_markup=get_menu_keyboard())