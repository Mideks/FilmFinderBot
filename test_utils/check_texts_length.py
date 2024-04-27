from tinydb import TinyDB

from routers.film_card import generate_film_card_text
db = TinyDB(r'..\films\info.json')

for film in db.all():
    text = generate_film_card_text(film)
    if len(text) > 1024:
        print(f"{film['title']}: текст слишком длинный ({len(text)}/1024)")
