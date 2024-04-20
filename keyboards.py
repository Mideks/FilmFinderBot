from typing import Set, Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_buttons import *


def get_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🔍 Искать!",
                   callback_data=NavigateButton(location=NavigateButtonLocation.Search))
    builder.button(text="🖼 Поиск по кадру",
                   callback_data=NavigateButton(location=NavigateButtonLocation.SearchByFrame))

    return builder.as_markup()


def get_search_film_filters_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🎭 Жанр",
                   callback_data=NavigateButton(location=NavigateButtonLocation.SelectGenre))
    builder.button(text="⭐️ Рейтинг",
                   callback_data=NavigateButton(location=NavigateButtonLocation.SelectRating))
    builder.button(text="🔞 Возрастное ограничение",
                   callback_data=NavigateButton(location=NavigateButtonLocation.SelectAgeRestriction))
    builder.button(text="🙎 Актёры",
                   callback_data=NavigateButton(location=NavigateButtonLocation.SelectActor))
    builder.button(text="⌛️ Продолжительность",
                   callback_data=NavigateButton(location=NavigateButtonLocation.SelectDuration))
    builder.button(text="⌛ Качество",
                   callback_data=NavigateButton(location=NavigateButtonLocation.SelectQuality))
    builder.button(text="🔍 Искать!",
                   callback_data=NavigateButton(location=NavigateButtonLocation.StartSearch))

    builder.adjust(2,2,2,1)

    return builder.as_markup()


def get_select_genre_keyboard(
        selected_genres: Optional[Set[str]] = None) -> InlineKeyboardMarkup:
    if selected_genres is None:
        selected_genres = set()

    builder = InlineKeyboardBuilder()

    # todo: добавить реальные жанры
    genres = ["Боевик", "Драма", "..."]

    for genre in genres:
        if genre in selected_genres:
            button_text = f"✅ {genre}"
        else:
            button_text = f"{genre}"

        builder.button(
            text=button_text,
            callback_data=DataButton(type=DataType.Genre, data=genre)
        )

    builder.button(text="◀️ Назад к фильтрам",
                   callback_data=NavigateButton(location=NavigateButtonLocation.Search))

    builder.adjust(1)

    return builder.as_markup()
