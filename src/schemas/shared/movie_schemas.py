from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    title: str
    year: str
    imdb_id: str
    type: str
    poster: str


class MovieCreate(MovieBase):
    title: str = Field(alias="Title")
    year: str = Field(alias="Year")
    imdb_id: str = Field(alias="imdbID")
    type: str = Field(alias="Type")
    poster: str = Field(alias="Poster")


class MovieGet(MovieBase):
    id: int

    class Config:
        from_attributes = True
