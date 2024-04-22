from collections import defaultdict

from tinydb import TinyDB

db = TinyDB('../films/info.json')

films_genres = [d['genres'] for d in db.all()]
genres = defaultdict(int)
for film_genres in films_genres:
    for genre in film_genres:
        genres[genre.lower()] += 1

print(genres)
