from pydantic import BaseModel, Field

from schemas.shared.movie_schemas import MovieCreate


class MovieSearchResponse(BaseModel):
    movies: list[MovieCreate] = Field(alias="Search")
    total_results: str = Field(alias="totalResults")
    response: str = Field(alias="Response")


class Rating(BaseModel):
    source: str = Field(alias="Source")
    value: str = Field(alias="Value")


class MovieImdbResponse(BaseModel):
    title: str = Field(alias="Title")
    year: str = Field(alias="Year")
    rated: str = Field(alias="Rated")
    released: str = Field(alias="Released")
    runtime: str = Field(alias="Runtime")
    genre: str = Field(alias="Genre")
    director: str = Field(alias="Director")
    writer: str = Field(alias="Writer")
    actors: str = Field(alias="Actors")
    plot: str = Field(alias="Plot")
    language: str = Field(alias="Language")
    country: str = Field(alias="Country")
    awards: str = Field(alias="Awards")
    poster: str = Field(alias="Poster")
    ratings: list[Rating] = Field(alias="Ratings")
    metascore: str = Field(alias="Metascore")
    imdb_rating: str = Field(alias="imdbRating")
    imdb_votes: str = Field(alias="imdbVotes")
    imdb_id: str = Field(alias="imdbID")
    type: str = Field(alias="Type")
    dvd: str = Field(alias="DVD")
    box_office: str = Field(alias="BoxOffice")
    production: str = Field(alias="Production")
    website: str = Field(alias="Website")
