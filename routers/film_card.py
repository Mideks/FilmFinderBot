import os
import random

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message
from tinydb.table import Document

import keyboards
from callback_buttons import NavigateButton, NavigateButtonLocation, DataButton, DataType
from db_functions import search_films_by_filters, get_film_by_title, get_film_by_id

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
    await send_film_message(callback.message, selected_film, is_first_search_result)


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.ShowMovieLinks))
async def show_movie_links_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    film: Document = data.get("selected_film", None)
    if film is None:
        await callback.answer("Произошла ошибка...")
        return

    links = '\n'.join(film['links'])
    text = (
        f"Где посмотреть:\n"
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


async def send_film_message(message: Message, film: dict, send_as_new: bool = False):
    text = await generate_film_card_text(film)

    path = "films/" + film["image"]
    if not os.path.exists(path):
        # todo: исправить все ошибки с ненайденными файлами
        await message.answer("Извините, не удалось отправить картинку")
        print(f"photo_path = {path} не существует")
        return

    photo = FSInputFile(path)
    if send_as_new:
        await message.answer_photo(
            photo=photo, caption=text,
            reply_markup=keyboards.get_film_card_keyboard(film)
        )
        await message.delete()
    else:
        await message.edit_media(
            media=InputMediaPhoto(media=photo, caption=text),
            reply_markup=keyboards.get_film_card_keyboard(film)
        )


@router.callback_query(DataButton.filter(F.type == DataType.FilmId))
async def navigate_to_film_handler(
        callback: CallbackQuery, callback_data: DataButton, state: FSMContext) -> None:
    film_id = int(callback_data.data)
    film = get_film_by_id(film_id)
    if film is not None:
        await state.update_data(selected_film=film)
        await send_film_message(callback.message, film)
        await callback.answer()
    else:
        await callback.answer('Фильм не найден...')


async def generate_film_card_text(film):
    max_quality = max(film['availableQuality'])

    text = (
               "Мы нашли подходящий фильм по вашему запросу, приятного просмотра!\n\n"
               f"{film['rating']} ⭐️\n"
               f"<b>{film['title']}</b>, {film['ageRestriction']}+\n"
               f"{film['description']}\n\n"
               f"Жанры: {', '.join(film['genres'])}\n"
               f"Продолжительность: {film['duration']} мин.\n"
               f"Доступное качество: {max_quality}p\n"
               f"Актёры: {', '.join(film['actors'])}"
           )[:1024]  # todo: сделать что-то с выходом за лимит количества символов
    return text
