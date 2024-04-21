from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import keyboards
import states
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
    await state.set_state(states.SelectingFilm.main_menu)
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
    await callback.message.edit_reply_markup(
        reply_markup=keyboards.get_select_genre_keyboard(search_filters.genres)
    )

    await callback.answer()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SelectAgeRestriction))
async def select_age_restriction_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    await callback.message.edit_text(
        "Выберите возрастное ограничение",
        reply_markup=keyboards.get_age_restriction_keyboard(str(search_filters.age_restriction))
    )

    await callback.answer()


@router.callback_query(DataButton.filter(F.type == DataType.AgeRestriction))
async def select_age_restriction_handler(
        callback: CallbackQuery, callback_data: DataButton, state: FSMContext) -> None:

    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]
    search_filters.age_restriction = int(callback_data.data)
    await state.update_data(search_filters=search_filters)

    await callback.message.edit_reply_markup(
        reply_markup=keyboards.get_age_restriction_keyboard(str(search_filters.age_restriction))
    )
    await callback.answer()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SelectQuality))
async def select_quality_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    await callback.message.edit_text(
        "Выберите желаемое качество. Будут показаны фильмы не ниже выбранного качества",
        reply_markup=keyboards.get_quality_keyboard(search_filters.quality)
    )

    await callback.answer()


@router.callback_query(DataButton.filter(F.type == DataType.Quality))
async def select_quality_handler(
        callback: CallbackQuery, callback_data: DataButton, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]
    search_filters.quality = callback_data.data
    await state.update_data(search_filters=search_filters)

    await callback.message.edit_reply_markup(
        reply_markup=keyboards.get_quality_keyboard(search_filters.quality)
    )
    await callback.answer()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SelectRating))
async def select_quality_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    await callback.message.edit_text(
        "Выберите желаемый рейтинг фильма. Либо вы можете ввести своё значение.\n"
        "Пример: 4.1",
        reply_markup=keyboards.get_rating_keyboard(str(search_filters.rating))
    )

    await state.set_state(states.SelectingFilm.waiting_for_rating)
    await state.update_data(bot_message=callback.message)

    await callback.answer()


@router.callback_query(DataButton.filter(F.type == DataType.Rating))
async def select_quality_handler(
        callback: CallbackQuery, callback_data: DataButton, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]
    search_filters.rating = float(callback_data.data)
    await state.update_data(search_filters=search_filters)

    await callback.message.edit_reply_markup(
        reply_markup=keyboards.get_rating_keyboard(str(search_filters.rating))
    )
    await callback.answer()


@router.message(states.SelectingFilm.waiting_for_rating)
async def enter_rating_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    try:
        value = float(message.text)
    except ValueError:
        await message.delete()
        return

    if value < 0 or value > 5:
        await message.delete()
        return

    search_filters.rating = value

    await state.update_data(search_filters=search_filters)

    bot_message: Message = data["bot_message"]
    await bot_message.edit_reply_markup(
        reply_markup=keyboards.get_rating_keyboard(str(search_filters.rating))
    )

    await message.delete()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SelectDuration))
async def select_duration_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    await callback.message.edit_text(
        "Выберите желаемую продолжительность фильма. Либо вы можете ввести своё значение.\n"
        "Пример: 25\n"
        "Будут показаны фильмы не более выбранной продолжительности.",
        reply_markup=keyboards.get_duration_keyboard(str(search_filters.duration))
    )

    await state.set_state(states.SelectingFilm.waiting_for_duration)
    await state.update_data(bot_message=callback.message)

    await callback.answer()


@router.callback_query(DataButton.filter(F.type == DataType.Duration))
async def select_quality_handler(
        callback: CallbackQuery, callback_data: DataButton, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]
    search_filters.duration = int(callback_data.data)
    await state.update_data(search_filters=search_filters)

    await callback.message.edit_reply_markup(
        reply_markup=keyboards.get_duration_keyboard(str(search_filters.duration))
    )
    await callback.answer()


@router.message(states.SelectingFilm.waiting_for_duration)
async def enter_duration_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    try:
        value = int(message.text)
    except ValueError:
        await message.delete()
        return

    if value < 0 or value > 1000:
        await message.delete()
        return

    search_filters.duration = value

    await state.update_data(search_filters=search_filters)

    bot_message: Message = data["bot_message"]
    await bot_message.edit_reply_markup(
        reply_markup=keyboards.get_duration_keyboard(str(search_filters.duration))
    )

    await message.delete()

# todo: add check if value is not modified
