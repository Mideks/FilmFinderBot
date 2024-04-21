from typing import Optional, Set


class SearchFilters:
    genres: Set[str] = set()
    rating: float = 0.0
    age_restriction: int = 0
    duration: int = 0
    quality: str = "720"
