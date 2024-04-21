from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

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
    max_quality = max(film['availableQuality'])
    links = '\n'.join(film['links'])
    text = (
        "Мы нашли подходящий фильм по вашему запросу:\n\n"
        f"{film['rating']} ⭐️\n"
        f"<b>{film['title']}</b>, {film['ageRestriction']}+\n"
        f"{film['description']}\n\n"
        f"Жанры: {', '.join(film['genres'])}\n"
        f"Продолжительность: {film['duration']} мин.\n"
        f"Доступное качество: {max_quality}p\n"
        f"Актёры: {', '.join(film['actors'])}\n"
        f"Где посмотреть:\n"
        f"{links}"
    )

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=film["image"],
        caption=text, reply_markup=keyboards.get_film_card_keyboard(film))

