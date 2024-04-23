from typing import Optional, Set


class SearchFilters:
    genres: Set[str] = set()
    rating: float = 0.0
    age_restriction: int = 12
    duration: int = 0
    quality: str = "720"
