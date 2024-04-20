import enum

from aiogram.filters.callback_data import CallbackData


class ActionButtonAction(enum.Enum):
    pass


class ActionButton(CallbackData, prefix="action"):
    action: ActionButtonAction


class NavigateButtonLocation(enum.Enum):
    Search = "Search"


class NavigateButton(CallbackData, prefix="navigate"):
    location: NavigateButtonLocation

