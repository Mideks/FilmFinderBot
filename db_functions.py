from typing import Any, Optional
from tinydb import TinyDB, Query
from tinydb.table import Document

from search_filters import SearchFilters

db = TinyDB('films/info.json')


def search_film_by_filters(filters: SearchFilters) -> Optional[dict]:
    Film = Query()

    result = db.search(
        (Film.rating >= filters.rating)
        & (Film.duration <= filters.duration)
        # & (Film.availableQuality.any([filters.quality]))
    )
    if len(result) > 0:
        return result[0]
    else:
        return None
