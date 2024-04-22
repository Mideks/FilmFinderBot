import random
from typing import Any, Optional
from tinydb import TinyDB, Query
from tinydb.table import Document

from search_filters import SearchFilters

db = TinyDB('films/info.json')


def search_films_by_filters(filters: SearchFilters) -> list[dict]:
    Film = Query()

    result = db.search(
        (Film.rating >= filters.rating)
        & (Film.duration <= filters.duration)
        # & (Film.availableQuality.any([filters.quality]))
    )
    return result
