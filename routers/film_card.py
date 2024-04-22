import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

import keyboards
import states
from callback_buttons import NavigateButton, NavigateButtonLocation, DataButton, DataType
from db_functions import search_film_by_filters
from search_filters import SearchFilters

router = Router()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.StartSearch))
async def start_search_menu_handler(
        callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    film: dict = search_film_by_filters(data["search_filters"])
    if film is None:
        await callback.message.answer("Ничего не найдено, извините(")
        return

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

    path = "films/" + film["image"]
    if not os.path.exists(path):
        # todo: исправить все ошибки с ненайденными файлами
        await callback.message.answer("Извините, не удалось отправить картинку")
        print(f"photo_path = {path} не существует")
        return

    photo = FSInputFile(path)
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        caption=text, reply_markup=keyboards.get_film_card_keyboard(film))

