from aiogram.fsm.state import StatesGroup, State


class SelectingFilm(StatesGroup):
    waiting_for_film_title = State()
    waiting_for_duration = State()
    waiting_for_rating = State()

