from aiogram.fsm.state import StatesGroup, State


class SelectingFilm(StatesGroup):
    main_menu = State()
    waiting_for_rating = State()
