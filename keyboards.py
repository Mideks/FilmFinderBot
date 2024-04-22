from typing import Set, Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import db_functions
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


def get_rating_keyboard(selected_rating: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    default_ratings = ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"]

    for rating in default_ratings:
        if rating == selected_rating:
            button_text = f"✅ от {rating}"
        else:
            button_text = f"от {rating}"

        builder.button(
            text=button_text,
            callback_data=DataButton(type=DataType.Rating, data=rating)
        )

    any_text = "Любой рейтинг"
    if float(selected_rating) == 0:
        any_text = f"✅ {any_text}"

    builder.button(
        text=any_text,
        callback_data=DataButton(type=DataType.Rating, data="0")
    )

    if selected_rating not in default_ratings and float(selected_rating) != 0:
        builder.button(
            text=f"✅ Ваш выбор: от {selected_rating:.2f} ⭐️",
            callback_data=DataButton(type=DataType.Rating, data=selected_rating)
        )

    builder.button(text="◀️ Назад к фильтрам",
                   callback_data=NavigateButton(location=NavigateButtonLocation.Search))

    builder.adjust(3, 3, 3, 1, 1)

    return builder.as_markup()


def get_duration_keyboard(selected_duration: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    default_durations = ["10", "15", "30", "45", "60", "90", "120", "150", "180"]

    for duration in default_durations:
        button_text = f"до {duration} мин"
        if duration == selected_duration:
            button_text = f"✅ {button_text}"

        builder.button(
            text=button_text,
            callback_data=DataButton(type=DataType.Duration, data=duration)
        )

    any_text = "Любая длительность"
    if int(selected_duration) == 0:
        any_text = f"✅ {any_text}"

    builder.button(
        text=any_text,
        callback_data=DataButton(type=DataType.Duration, data="0")
    )

    if selected_duration not in default_durations and int(selected_duration) != 0:
        builder.button(
            text=f"✅ Ваш выбор: до {selected_duration} мин ⏳",
            callback_data=DataButton(type=DataType.Duration, data=selected_duration)
        )

    builder.button(text="◀️ Назад к фильтрам",
                   callback_data=NavigateButton(location=NavigateButtonLocation.Search))

    builder.adjust(3, 3, 3, 1, 1)

    return builder.as_markup()


def get_film_card_keyboard(film: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    related_movies = film.get("relatedMovies", [])

    builder.button(text="🎲 Другой фильм",
                   callback_data=NavigateButton(location=NavigateButtonLocation.StartSearch))
    builder.button(text="👁 Где посмотреть",
                   callback_data=NavigateButton(location=NavigateButtonLocation.ShowMovieLinks))

    if len(related_movies) > 0:
        builder.button(text=f"🔗 Связанные фильмы ({len(related_movies)})",
                       callback_data=NavigateButton(location=NavigateButtonLocation.ShowRelatedMovies))

    builder.button(text="◀️ Поменять фильтры",
                   callback_data=NavigateButton(location=NavigateButtonLocation.BackToSearch))
    builder.adjust(1)

    return builder.as_markup()


def get_show_movie_links_keyboard(selected_film_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад к фильму",
                   callback_data=DataButton(type=DataType.FilmId, data=str(selected_film_id)))
    builder.adjust(1)

    return builder.as_markup()


def get_show_related_movies_keyboard(selected_film_id: int, related_movies: list[str]):
    builder = InlineKeyboardBuilder()
    # todo: add indicator, that will display, if film in our db
    for related_movie in related_movies:
        movie = db_functions.get_film_by_title(related_movie)

        if movie is not None:
            doc_id = movie.doc_id
            text = f"✔️ {related_movie}"
        else:
            doc_id = -1
            text = f"✖️ {related_movie}"

        builder.button(
            text=text,
            callback_data=DataButton(type=DataType.FilmId, data=str(doc_id))
        )

    builder.button(text="◀️ Назад к фильму",
                   callback_data=DataButton(type=DataType.FilmId, data=str(selected_film_id)))
    builder.adjust(1)

    return builder.as_markup()
