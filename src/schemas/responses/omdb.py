from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator


class MovieSearch(BaseModel):
    title: str = Field(alias="Title")
    year: str = Field(alias="Year")
    imdb_id: str = Field(alias="imdbID")
    type: str = Field(alias="Type")
    poster: str = Field(alias="Poster")


class MovieSearchResponse(BaseModel):
    movies: list[MovieSearch] = Field(alias="Search")
    total_results: str = Field(alias="totalResults")
    response: str = Field(alias="Response")


class RatingImdbResponse(BaseModel):
    source: str = Field(alias="Source")
    value: str = Field(alias="Value")


class MovieImdbResponse(BaseModel):
    title: str = Field(alias="Title")
    year: int = Field(alias="Year")
    rated: str | None = Field(alias="Rated")
    released: date | None = Field(alias="Released")
    runtime: str | None = Field(alias="Runtime")
    genre: str | None = Field(alias="Genre")
    director: str | None = Field(alias="Director")
    writer: str | None = Field(alias="Writer")
    actors: str | None = Field(alias="Actors")
    plot: str | None = Field(alias="Plot")
    language: str | None = Field(alias="Language")
    country: str | None = Field(alias="Country")
    awards: str | None = Field(alias="Awards")
    poster: str | None = Field(alias="Poster")
    ratings: list[RatingImdbResponse] = Field(alias="Ratings")
    metascore: int | None = Field(alias="Metascore")
    imdb_rating: float | None = Field(alias="imdbRating")
    imdb_votes: int | None = Field(alias="imdbVotes")
    imdb_id: str = Field(alias="imdbID")
    type: str = Field(alias="Type")
    dvd: str | None = Field(alias="DVD")
    box_office: str | None = Field(alias="BoxOffice")
    production: str | None = Field(alias="Production")
    website: str | None = Field(alias="Website")

    @field_validator("released", mode="before")
    def validate_released(v: str | None):
        v = none_if_na(v)
        return datetime.strptime(v, "%d %b %Y").date() if v else None

    @field_validator("year", "metascore", "imdb_votes", mode="before")
    def validate_ints(v: str | None):
        v = none_if_na(v)
        return int(v.replace(",", "")) if v else None

    @field_validator("imdb_rating", mode="before")
    def validate_floats(v: str | None):
        v = none_if_na(v)
        return float(v) if v else None

    @field_validator(
        "rated",
        "plot",
        "awards",
        "poster",
        "dvd",
        "box_office",
        "production",
        "website",
        "genre",
        "director",
        "writer",
        "actors",
        "language",
        "country",
        "runtime",
        mode="before",
    )
    def validate_optional_na(v: str | None):
        return none_if_na(v)


def none_if_na(value: str | None) -> str | None:
    return None if value in (None, "N/A") else value
