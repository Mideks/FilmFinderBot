import random
import re
from collections import defaultdict, Counter
from typing import Any, Optional
from tinydb import TinyDB, Query
from tinydb.table import Document

from search_filters import SearchFilters

db = TinyDB('films/info.json')


def search_films_by_filters(filters: SearchFilters) -> list[Document]:
    Film = Query()

    def has_quality_not_less_than(quality_list: list[int], min_quality: int):
        return any(quality >= min_quality for quality in quality_list)

    query = (
            (Film.rating >= filters.rating)
            & (Film.availableQuality.test(has_quality_not_less_than, int(filters.quality)))
            & (Film.ageRestriction <= filters.age_restriction)
    )

    if len(filters.genres) != 0:
        query &= (Film.genres.any(filters.genres))

    if len(filters.actors) != 0:
        query &= (Film.actors.any(filters.actors))

    if filters.duration != 0:
        query &= (Film.duration <= filters.duration)

    result = db.search(query)

    return result


def get_film_by_title(title: str) -> Optional[Document]:
    Film = Query()

    result = db.search(Film.title == title)
    if len(result) == 0:
        return None
    else:
        return result[0]


def search_film_by_party_title(party_title: str) -> list[Document]:
    Film = Query()
    result = db.search(Film.title.matches(party_title, flags=re.IGNORECASE))
    return result


def get_film_by_id(film_id: int) -> Optional[Document]:
    return db.get(doc_id=film_id)


def get_films_genres() -> Counter[str]:
    # Retrieve all genres from all films
    all_genres = [genre.lower() for film in db.all() for genre in film['genres']]

    # Use Counter to count the occurrences of each genre
    genres: Counter[str] = Counter(all_genres)

    return genres


def get_films_actors() -> Counter[str]:
    # Retrieve all actors from all films
    all_actors = [actor for film in db.all() for actor in film['actors']]

    # Use Counter to count the occurrences of each actor
    actors: Counter[str] = Counter(all_actors)

    return actors
