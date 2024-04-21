from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import keyboards
import states
from callback_buttons import NavigateButton, NavigateButtonLocation, DataButton, DataType
from search_filters import SearchFilters

router = Router()


film_test = {
    "type": "movie",
    "title": "Movie Title",
    "description": "A brief description of the movie, up to 1024 characters.",
    "image": "https://w.forfun.com/fetch/fc/fc829663851296fef905684909404baf.jpeg",
    "duration": 120,
    "rating": 4.1,
    "genres": [
       "Genre1",
       "Genre2",
       "Genre3",
       "Genre4",
       "Genre5"
    ],
    "ageRestriction": 16,
    "availableQuality": [2160, 1440, 1080, 720, 480, 360, 240, 144],
    "links": [
       "https://example.com/link1",
       "https://example.com/link2",
       "https://example.com/link3",
       "https://example.com/link4",
       "https://example.com/link5"
    ],
    "relatedMovies": [
       "Related Movie 1",
       "Related Movie 2"
    ],
    "actors": [
       "Actor1",
       "Actor2",
       "Actor3",
       "Actor4",
       "Actor5",
       "Actor6",
       "Actor7",
       "Actor8",
       "Actor9",
       "Actor10",
       "Actor11"
    ],
   }


@router.callback_query(NavigateButton.filter(F.location == NavigateButtonLocation.StartSearch))
async def start_search_menu_handler(
        callback: CallbackQuery, state: FSMContext) -> None:
    film: dict = film_test
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

