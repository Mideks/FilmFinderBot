import enum

from aiogram.filters.callback_data import CallbackData


class ActionButtonAction(enum.Enum):
    pass


class ActionButton(CallbackData, prefix="action"):
    action: ActionButtonAction


class NavigateButtonLocation(enum.Enum):
    StartSearch = "StartSearch"
    SelectQuality = "SelectQuality"
    SelectDuration = "SelectDuration"
    SelectActor = "SelectActor"
    SelectAgeRestriction = "SelectAgeRestriction"
    SelectRating = "SelectRating"
    SelectGenre = "SelectGenre"
    SearchByFrame = "SearchByFrame"
    Search = "Search"


class NavigateButton(CallbackData, prefix="navigate"):
    location: NavigateButtonLocation

