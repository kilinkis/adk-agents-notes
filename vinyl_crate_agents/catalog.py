"""A tiny sample catalog so the example runs with no database or API."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Album:
    id: str
    title: str
    artist: str
    genre: str
    year: int


CATALOG: tuple[Album, ...] = (
    Album("kind-of-blue", "Kind of Blue", "Miles Davis", "jazz", 1959),
    Album("a-love-supreme", "A Love Supreme", "John Coltrane", "jazz", 1965),
    Album("time-out", "Time Out", "The Dave Brubeck Quartet", "jazz", 1959),
    Album("blue-train", "Blue Train", "John Coltrane", "jazz", 1958),
    Album("rumours", "Rumours", "Fleetwood Mac", "rock", 1977),
    Album("dark-side", "The Dark Side of the Moon", "Pink Floyd", "rock", 1973),
    Album("led-zeppelin-iv", "Led Zeppelin IV", "Led Zeppelin", "rock", 1971),
    Album("computer-world", "Computer World", "Kraftwerk", "electronic", 1981),
    Album("selected-ambient", "Selected Ambient Works 85-92", "Aphex Twin", "electronic", 1992),
    Album("homework", "Homework", "Daft Punk", "electronic", 1997),
)

_BY_ID = {album.id: album for album in CATALOG}


def get_album(album_id: str) -> Album | None:
    return _BY_ID.get(album_id)


def albums_in_genre(genre: str) -> list[dict]:
    wanted = genre.strip().lower()
    return [asdict(a) for a in CATALOG if a.genre == wanted]
