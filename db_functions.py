import random
from typing import Any, Optional
from tinydb import TinyDB, Query
from tinydb.table import Document

from search_filters import SearchFilters

db = TinyDB('films/info.json')


def search_films_by_filters(filters: SearchFilters) -> list[Document]:
    Film = Query()
    duration = filters.duration
    if duration == 0:
        duration = 999999

    def has_quality_not_less_than(quality_list: list[int], min_quality: int):
        return any(quality >= min_quality for quality in quality_list)

    result = db.search(
        (Film.rating >= filters.rating)
        & (Film.duration <= duration)
        & (Film.availableQuality.test(has_quality_not_less_than, int(filters.quality)))
        & (Film.ageRestriction <= filters.age_restriction)
    )
    return result


def get_film_by_title(title: str) -> Optional[Document]:
    Film = Query()

    result = db.search(Film.title == title)
    if len(result) == 0:
        return None
    else:
        return result[0]


def get_film_by_id(film_id: int) -> Optional[Document]:
    return db.get(doc_id=film_id)
