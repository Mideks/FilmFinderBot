import os
import random

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile, InputMediaPhoto

import keyboards
import states
from callback_buttons import NavigateButton, NavigateButtonLocation, DataButton, DataType
from db_functions import search_films_by_filters
from search_filters import SearchFilters

router = Router()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.StartSearch))
async def start_search_menu_handler(
        callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    films: list[dict] = data.get("search_result", None)

    is_first_search_result = False
    if films is None:
        films = search_films_by_filters(data["search_filters"])
        if len(films) == 0:
            await callback.message.answer("Ничего не найдено, извините(")
            return

        await state.update_data(search_result=films)
        is_first_search_result = True

    chosen_film = random.choice(films)
    text = await generate_film_card_text(chosen_film)

    path = "films/" + chosen_film["image"]
    if not os.path.exists(path):
        # todo: исправить все ошибки с ненайденными файлами
        await callback.message.answer("Извините, не удалось отправить картинку")
        print(f"photo_path = {path} не существует")
        return

    photo = FSInputFile(path)
    if is_first_search_result:
        await callback.message.answer_photo(
            photo=photo, caption=text,
            reply_markup=keyboards.get_film_card_keyboard(chosen_film)
        )
        await callback.message.delete()
    else:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=photo, caption=text),
            reply_markup=keyboards.get_film_card_keyboard(chosen_film)
        )


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.StartSearch))
async def start_search_menu_handler(
        callback: CallbackQuery, state: FSMContext) -> None:
    pass


async def generate_film_card_text(film):
    max_quality = max(film['availableQuality'])
    links = '\n'.join(film['links'])
    text = (
               "Мы нашли подходящий фильм по вашему запросу, приятного просмотра!\n\n"
               f"{film['rating']} ⭐️\n"
               f"<b>{film['title']}</b>, {film['ageRestriction']}+\n"
               f"{film['description']}\n\n"
               f"Жанры: {', '.join(film['genres'])}\n"
               f"Продолжительность: {film['duration']} мин.\n"
               f"Доступное качество: {max_quality}p\n"
               f"Актёры: {', '.join(film['actors'])}\n"
               f"Где посмотреть:\n"
               f"{links}"
           )[:1024]  # todo: сделать что-то с выходом за лимит количества символов
    return text
