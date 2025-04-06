from pydantic import BaseModel


class Rating(BaseModel):
    source: str
    value: str


class RatingGet(Rating):
    id: int

    class Config:
        from_attributes = True


class MovieBase(BaseModel):
    title: str
    year: str
    rated: str
    released: str
    runtime: str
    genre: str
    director: str
    writer: str
    actors: str
    plot: str
    language: str
    country: str
    awards: str
    poster: str
    ratings: list[Rating]
    metascore: str
    imdb_rating: str
    imdb_votes: str
    imdb_id: str
    type: str
    dvd: str
    box_office: str
    production: str
    website: str


class MovieCreate(MovieBase):
    pass


class MovieGet(MovieBase):
    id: int
    ratings: list[RatingGet]

    class Config:
        from_attributes = True
