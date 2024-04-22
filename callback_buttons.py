import enum

from aiogram.filters.callback_data import CallbackData


class ActionButtonAction(enum.Enum):
    pass


class ActionButton(CallbackData, prefix="action"):
    action: ActionButtonAction


class NavigateButtonLocation(enum.Enum):
    ShowMovieLinks = "ShowMovieLinks"
    ShowRelatedMovies = "ShowRelatedMovies"
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


class DataType(enum.Enum):
    FilmTitle = "FilmTitle"
    Duration = "Duration"
    Rating = "Rating"
    Quality = "Quality"
    AgeRestriction = "AgeRestriction"
    Genre = "Genre"


class DataButton(CallbackData, prefix="select_genre", sep=">"):
    type: DataType
    data: str
