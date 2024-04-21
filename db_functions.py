from typing import Any
from tinydb import TinyDB, Query
from tinydb.table import Document

from search_filters import SearchFilters

film_test = {
    "type": "movie",
    "title": "Movie Title",
    "description": "A brief description of the movie, up to 1024 characters.",
    "image": "https://w.forfun.com/fetch/fc/fc829663851296fef905684909404baf.jpeg",
    "duration": 120,
    "rating": 4.1,
    "genres": [
       "Genre1",
       "Genre2",
       "Genre3",
       "Genre4",
       "Genre5"
    ],
    "ageRestriction": 16,
    "availableQuality": [2160, 1440, 1080, 720, 480, 360, 240, 144],
    "links": [
       "https://example.com/link1",
       "https://example.com/link2",
       "https://example.com/link3",
       "https://example.com/link4",
       "https://example.com/link5"
    ],
    "relatedMovies": [
       "Related Movie 1",
       "Related Movie 2"
    ],
    "actors": [
       "Actor1",
       "Actor2",
       "Actor3",
       "Actor4",
       "Actor5",
       "Actor6",
       "Actor7",
       "Actor8",
       "Actor9",
       "Actor10",
       "Actor11"
    ],
   }

db = TinyDB('films/info.json')


def search_film_by_filters(filters: SearchFilters) -> dict[str, Any]:
    Film = Query()

    return db.all()[0]
