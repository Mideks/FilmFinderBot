from aiogram.fsm.state import StatesGroup, State


class SelectingFilm(StatesGroup):
    waiting_for_duration = State()
    main_menu = State()
    waiting_for_rating = State()

