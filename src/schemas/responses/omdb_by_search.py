from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str = Field(alias="Title")
    year: str = Field(alias="Year")
    imdb_id: str = Field(alias="imdbID")
    type: str = Field(alias="Type")
    poster: str = Field(alias="Poster")

class MovieSearchResponse(BaseModel):
    movies: list[Movie] = Field(alias="Search")
    total_results: str = Field(alias="totalResults")
    response: str = Field(alias="Response")