import random
from typing import Any, Optional
from tinydb import TinyDB, Query
from tinydb.table import Document

from search_filters import SearchFilters

db = TinyDB('films/info.json')


def search_films_by_filters(filters: SearchFilters) -> list[Document]:
    Film = Query()

    result = db.search(
        (Film.rating >= filters.rating)
        & (Film.duration <= filters.duration)
        # & (Film.availableQuality.any([filters.quality]))
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
