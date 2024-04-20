from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_buttons import *


def get_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🔍 Искать!",
                   callback_data=NavigateButton(location=NavigateButtonLocation.Search))

    return builder.as_markup()