from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import keyboards
import states
from callback_buttons import NavigateButton, NavigateButtonLocation, DataButton, DataType
from search_filters import SearchFilters

router = Router()


async def send_search_film_filters_menu_message(
        message: Message, state: FSMContext, send_as_new: bool = False):
    data = await state.get_data()
    filters: SearchFilters = data["search_filters"]

    text = (
        f"✍️ Введите название фильма, который вы хотели бы посмотреть"
        f"или найдите себе фильм по критериям ниже.\n\n"
        f"Ваш выбор\n"
        f"<b>Рейтинг:</b> {'любой' if filters.rating == 0 else f'от {filters.rating} ⭐️'}\n"
        f"<b>Возрастное ограничение:</b> {filters.age_restriction}+\n"
        f"<b>Жанры:</b> {'любые' if len(filters.genres) == 0 else ', '.join(filters.genres)}\n"
        f"<b>Актеры:</b>{'любые' if len(filters.actors) == 0 else ', '.join(filters.actors)}\n"
        f"<b>Длительность:</b> {'любая' if filters.duration == 0 else f'до {filters.duration} мин.'}\n"
        f"<b>Качество:</b> от {filters.quality}p\n"
    )

    if send_as_new:
        bot_message = await message.answer(
            text, reply_markup=keyboards.get_search_film_filters_menu_keyboard()
        )
        await state.update_data(bot_message=bot_message)
        await message.delete()
    else:
        await message.edit_text(
            text, reply_markup=keyboards.get_search_film_filters_menu_keyboard()
        )
        await state.update_data(bot_message=message)
    await state.update_data(selected_film=None, search_result=None)
    await state.set_state(states.SelectingFilm.waiting_for_film_title)


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SearchMenu))
async def search_film_filters_menu_handler(
        callback: CallbackQuery, state: FSMContext) -> None:
    await send_search_film_filters_menu_message(callback.message, state)
    await callback.answer()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.BackToSearch))
async def search_film_filters_menu_handler(
        callback: CallbackQuery, state: FSMContext) -> None:
    await send_search_film_filters_menu_message(callback.message, state, True)
    await callback.answer()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.NewSearch))
async def search_film_filters_menu_handler(
        callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    filters: SearchFilters = data.get('search_filters')
    if filters != SearchFilters():
        await state.update_data(search_filters=SearchFilters())
        await send_search_film_filters_menu_message(callback.message, state)
    await callback.answer("Фильтры сброшены")


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SelectGenre))
async def select_genre_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    await callback.message.edit_text(
        "🎭 Выберите желаемые жанры. \n"
        "Мы постараемся для вас найти фильм, в котором совпадает хотя бы один жанр",
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
        search_filters.genres.append(genre)
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
        "🔞 Выберите возрастное ограничение.\n"
        "Будут найдены фильмы не выше выбранного возрастного ограничения.",
        reply_markup=keyboards.get_age_restriction_keyboard(str(search_filters.age_restriction))
    )

    await callback.answer()


@router.callback_query(DataButton.filter(F.type == DataType.AgeRestriction))
async def select_age_restriction_handler(
        callback: CallbackQuery, callback_data: DataButton, state: FSMContext) -> None:

    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    age_restriction = int(callback_data.data)
    if age_restriction == search_filters.age_restriction:
        await callback.answer()
        return

    search_filters.age_restriction = age_restriction
    await state.update_data(search_filters=search_filters)

    await callback.message.edit_reply_markup(
        reply_markup=keyboards.get_age_restriction_keyboard(str(search_filters.age_restriction))
    )
    await callback.answer()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SelectActor))
async def select_actors_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    await callback.message.edit_text(
        "🙎 Выберите желаемых актёров. \n"
        "Мы постараемся для вас найти фильм, в котором присутствует хотя бы один актёр",
        reply_markup=keyboards.get_actors_keyboard(search_filters.actors)
    )

    await callback.answer()


@router.callback_query(DataButton.filter(F.type == DataType.Actors))
async def select_actors_handler(
        callback: CallbackQuery, callback_data: DataButton, state: FSMContext) -> None:

    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]
    actors = callback_data.data
    if actors not in search_filters.actors:
        search_filters.actors.append(actors)
    else:
        search_filters.actors.remove(actors)

    await state.update_data(search_filters=search_filters)
    await callback.message.edit_reply_markup(
        reply_markup=keyboards.get_actors_keyboard(search_filters.actors)
    )

    await callback.answer()


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.SelectQuality))
async def select_quality_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    await callback.message.edit_text(
        "🖼 Выберите желаемое качество.\n"
        "Будут найдены фильмы с качеством не ниже выбранного.",
        reply_markup=keyboards.get_quality_keyboard(search_filters.quality)
    )

    await callback.answer()


@router.callback_query(DataButton.filter(F.type == DataType.Quality))
async def select_quality_handler(
        callback: CallbackQuery, callback_data: DataButton, state: FSMContext) -> None:
    data = await state.get_data()
    search_filters: SearchFilters = data["search_filters"]

    quality = callback_data.data
    if quality == search_filters.quality:
        await callback.answer()
        return

    search_filters.quality = quality
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
        "⭐️ Выберите желаемый рейтинг фильма или введите своё значение.\n"
        "Пример: <i>4.1</i>\n",
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

    rating = float(callback_data.data)
    if rating == search_filters.rating:
        await callback.answer()
        return

    search_filters.rating = rating
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

    if value < 0 or value > 5 or value == search_filters.rating:
        await message.delete()
        return

    search_filters.rating = round(value, 2)

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
        "⏳ Выберите максимальную продолжительность фильма или и введите своё значение\n"
        "Пример: <i>25</>\n",
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

    duration = int(callback_data.data)
    if duration == search_filters.duration:
        await callback.answer()
        return

    search_filters.duration = duration
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

    if value < 0 or value > 1000 or value == search_filters.duration:
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
