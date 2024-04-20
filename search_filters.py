from typing import Optional, Set


class SearchFilters:
    genres: Set[str] = set()
    age_restriction: int = 0
    quality: str = "720"
    rating: float = 0.0
