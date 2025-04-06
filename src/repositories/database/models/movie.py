from sqlalchemy import Integer, String, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from repositories.database.models.base import Base
from repositories.database.models.rating import Rating


class Movie(Base):
    """Movie entity"""

    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    year: Mapped[str] = mapped_column(String)
    rated: Mapped[str] = mapped_column(String)
    released: Mapped[str] = mapped_column(String)
    runtime: Mapped[str] = mapped_column(String)
    genre: Mapped[str] = mapped_column(String)
    director: Mapped[str] = mapped_column(String)
    writer: Mapped[str] = mapped_column(String)
    actors: Mapped[str] = mapped_column(String)
    plot: Mapped[str] = mapped_column(String)
    language: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    awards: Mapped[str] = mapped_column(String)
    poster: Mapped[str] = mapped_column(String)
    metascore: Mapped[str] = mapped_column(String)
    imdb_rating: Mapped[str] = mapped_column(String)
    imdb_votes: Mapped[str] = mapped_column(String)
    imdb_id: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    dvd: Mapped[str] = mapped_column(String)
    box_office: Mapped[str] = mapped_column(String)
    production: Mapped[str] = mapped_column(String)
    website: Mapped[str] = mapped_column(String)

    ratings: Mapped[list["Rating"]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("imdb_id", name="imdb_id_unique"),
        Index("ix_movie_id", "id"),
        Index("ix_movie_imdb_id", "imdb_id"),
    )
