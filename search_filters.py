from typing import Optional, Set


class SearchFilters:
    genres: list[str]
    rating: float
    age_restriction: int
    duration: int
    quality: str

    def __init__(self, genres=None, rating: float = 0.0, age_restriction: int = 12,
                 duration: int = 0, quality: str = "720"):
        if genres is None:
            genres = list()
        self.genres = genres
        self.rating = rating
        self.age_restriction = age_restriction
        self.duration = duration
        self.quality = quality

    def __eq__(self, other):
        if isinstance(other, SearchFilters):
            return (self.genres == other.genres and
                    self.rating == other.rating and
                    self.age_restriction == other.age_restriction and
                    self.duration == other.duration and
                    self.quality == other.quality)
        return False
