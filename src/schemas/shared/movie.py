from datetime import date

from pydantic import BaseModel


class Rating(BaseModel):
    source: str
    value: str

    class Config:
        from_attributes = True


"""
class RatingGet(Rating):
    class Config:
        from_attributes = True
"""


class MovieBase(BaseModel):
    title: str
    year: int
    rated: str | None
    released: date | None
    runtime: str | None
    genre: str | None
    director: str | None
    writer: str | None
    actors: str | None
    plot: str | None
    language: str | None
    country: str | None
    awards: str | None
    poster: str | None
    ratings: list[Rating]
    metascore: int | None
    imdb_rating: float | None
    imdb_votes: int | None
    imdb_id: str
    type: str
    dvd: str | None
    box_office: str | None
    production: str | None
    website: str | None


class MovieCreate(MovieBase):
    pass


class MovieGet(MovieBase):
    id: int

    class Config:
        from_attributes = True
