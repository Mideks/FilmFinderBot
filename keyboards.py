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

    builder.adjust(2, 2, 2, 1)

    return builder.as_markup()


def get_select_genre_keyboard(selected_genres: Set[str]) -> InlineKeyboardMarkup:

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


def get_age_restriction_keyboard(selected_age_restriction: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    age_restrictions = ["0", "6", "12", "16", "18"]

    for age_restriction in age_restrictions:
        if age_restriction == selected_age_restriction:
            button_text = f"✅ {age_restriction}+"
        else:
            button_text = f"{age_restriction}+"

        builder.button(
            text=button_text,
            callback_data=DataButton(type=DataType.AgeRestriction, data=age_restriction)
        )

    builder.button(text="◀️ Назад к фильтрам",
                   callback_data=NavigateButton(location=NavigateButtonLocation.Search))

    builder.adjust(5, 1)

    return builder.as_markup()


def get_quality_keyboard(selected_quality: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    qualities = ["144", "240", "360", "480", "720", "1080", "1440", "2160"]

    for quality in qualities:
        if quality == selected_quality:
            button_text = f"✅ {quality}p"
        else:
            button_text = f"{quality}p"

        builder.button(
            text=button_text,
            callback_data=DataButton(type=DataType.Quality, data=quality)
        )

    builder.button(text="◀️ Назад к фильтрам",
                   callback_data=NavigateButton(location=NavigateButtonLocation.Search))

    builder.adjust(4, 4, 1)

    return builder.as_markup()