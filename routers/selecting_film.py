from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import keyboards
from callback_buttons import NavigateButton, NavigateButtonLocation, DataButton, DataType
from search_filters import SearchFilters

router = Router()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.Search))
async def search_film_filters_menu_handler(
        callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        "Введите фильм, который хотите найти, или выберите по критериям ниже",
        reply_markup=keyboards.get_search_film_filters_menu_keyboard()
    )
    await state.update_data(search_filters=SearchFilters())
    await callback.answer()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SelectGenre))
async def select_genre_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    await callback.message.edit_text(
        "Выберите желаемые жанры",
        reply_markup=keyboards.get_select_genre_keyboard(search_filters.genres)
    )

    await callback.answer()


@router.callback_query(DataButton.filter(F.type == DataType.Genre))
async def select_genre_handler(
        callback: CallbackQuery, callback_data: DataButton, state: FSMContext) -> None:

    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]
    genre = callback_data.data
    if genre not in search_filters.genres:
        search_filters.genres.add(genre)
    else:
        search_filters.genres.remove(genre)

    await state.update_data(search_filters=search_filters)
    await callback.message.edit_text(
        f"Выберите желаемые жанры",
        reply_markup=keyboards.get_select_genre_keyboard(search_filters.genres))
    await callback.answer()
