import os
import random

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message
from tinydb.table import Document

import db_functions
import keyboards
import states
from callback_buttons import NavigateButton, NavigateButtonLocation, DataButton, DataType
from db_functions import search_films_by_filters, get_film_by_title, get_film_by_id
from search_filters import SearchFilters

router = Router()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.StartSearch))
async def start_search_menu_handler(
        callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    films: list[Document] = data.get("search_result", None)

    is_first_search_result = False
    if films is None:
        films = search_films_by_filters(data["search_filters"])
        if len(films) == 0:
            await callback.answer("Ничего не найдено, извините(")
            return

        await state.update_data(search_result=films)
        is_first_search_result = True

    selected_film = random.choice(films)
    await state.update_data(selected_film=selected_film)
    await state.set_state(None)
    await send_film_message(callback.message, selected_film, state, is_first_search_result)


@router.message(states.SelectingFilm.waiting_for_film_title)
async def enter_film_title_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    query = message.text
    films = db_functions.search_film_by_party_title(query)

    bot_message = data["bot_message"]
    if len(films) == 0:
        text = (f"😞 По вашему запросу <b>{query}</b> ничего не найдено.\n"
                "Попробуйте задать запрос по-другому или поискать по фильтрам.")
    else:
        text = f"🔍 По вашему запросу <b>{query}</b> были найдены следующие фильмы:"

    await bot_message.edit_text(
        text, reply_markup=keyboards.get_search_by_title_result_keyboard(films))
    await message.delete()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.ShowMovieLinks))
async def show_movie_links_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    film: Document = data.get("selected_film", None)
    if film is None:
        await callback.answer("Произошла ошибка...")
        return

    links = '\n'.join(film['links'])
    text = (
        f"👀 Вот некоторые места, где можно посмотреть <b>{film['title']}</b>:\n"
        f"{links}"
    )

    path = "films/" + film["image"]
    photo = FSInputFile(path)
    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo, caption=text),
        reply_markup=keyboards.get_show_movie_links_keyboard(film.doc_id)
    )

    await callback.answer()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.ShowRelatedMovies))
async def show_related_movies_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    film: Document = data.get("selected_film", None)
    if film is None:
        await callback.answer("Произошла ошибка...")
        return

    related_movies = film['relatedMovies']
    text = (f"<b>{film['title']}</b>, {film['ageRestriction']}+\n\n"
            f"Есть некоторые фильмы, которые связаны с текущим. Нажмите на кнопку, чтобы перейти к нем.")

    path = "films/" + film["image"]
    photo = FSInputFile(path)
    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo, caption=text),
        reply_markup=keyboards.get_show_related_movies_keyboard(film.doc_id, related_movies)
    )

    await callback.answer()


async def send_film_message(message: Message, film: dict, state: FSMContext, send_as_new: bool = False):
    # todo: сделать что-то с выходом за лимит количества символов
    text = generate_film_card_text(film)[:1024]

    path = "films/" + film["image"]
    if not os.path.exists(path):
        # todo: исправить все ошибки с ненайденными файлами
        await message.answer("Извините, не удалось отправить картинку")
        print(f"photo_path = {path} не существует")
        return

    photo = FSInputFile(path)
    if send_as_new:
        bot_message = await message.answer_photo(
            photo=photo, caption=text,
            reply_markup=keyboards.get_film_card_keyboard(film)
        )
        await message.delete()
        await state.update_data(bot_message=bot_message)
    else:
        await message.edit_media(
            media=InputMediaPhoto(media=photo, caption=text),
            reply_markup=keyboards.get_film_card_keyboard(film)
        )


@router.callback_query(DataButton.filter(F.type == DataType.FilmId))
async def navigate_to_film_handler(
        callback: CallbackQuery, callback_data: DataButton, state: FSMContext) -> None:
    data = await state.get_data()
    film_id = int(callback_data.data)
    film = get_film_by_id(film_id)
    if film is not None:
        await state.update_data(selected_film=film)
        await state.set_state(None)
        send_as_new = "bot_message" in data
        await send_film_message(callback.message, film, state, send_as_new)
        await callback.answer()
    else:
        await callback.answer('Фильм не найден...')


def generate_film_card_text(film):
    max_quality = max(film['availableQuality'])

    text = (
               "Мы нашли подходящий фильм по вашему запросу, приятного просмотра!\n\n"
               f"<b>{film['title']}</b>, {film['ageRestriction']}+\n"
               f"{film['rating']} ⭐️\n\n"
               f"<i>{film['description']}</i>\n\n"
               f"<b>Жанры</b>: {', '.join(film['genres'])}\n"
               f"<b>Продолжительность</b>: {film['duration']} мин.\n"
               f"<b>Доступное качество</b>: {max_quality}p\n"
               f"<b>Актёры</b>: {', '.join(film['actors'])}"
    )
    return text
