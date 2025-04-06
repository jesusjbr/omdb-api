from sqlalchemy import Integer, String, UniqueConstraint, Index, Date, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import IMDB_ID_UNIQUE_CONSTRAINT
from repositories.database.models.base import Base
from repositories.database.models.rating import Rating


class Movie(Base):
    """Movie entity"""

    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer)
    rated: Mapped[str | None] = mapped_column(String, nullable=True)
    released: Mapped[Date | None] = mapped_column(Date, nullable=True)
    runtime: Mapped[str | None] = mapped_column(String, nullable=True)
    genre: Mapped[str | None] = mapped_column(String, nullable=True)
    director: Mapped[str | None] = mapped_column(String, nullable=True)
    writer: Mapped[str | None] = mapped_column(String, nullable=True)
    actors: Mapped[str | None] = mapped_column(String, nullable=True)
    plot: Mapped[str | None] = mapped_column(String, nullable=True)
    language: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    awards: Mapped[str | None] = mapped_column(String, nullable=True)
    poster: Mapped[str | None] = mapped_column(String, nullable=True)
    metascore: Mapped[int | None] = mapped_column(Integer, nullable=True)
    imdb_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    imdb_votes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    imdb_id: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    dvd: Mapped[str | None] = mapped_column(String, nullable=True)
    box_office: Mapped[str | None] = mapped_column(String, nullable=True)
    production: Mapped[str | None] = mapped_column(String, nullable=True)
    website: Mapped[str | None] = mapped_column(String, nullable=True)

    ratings: Mapped[list["Rating"]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("imdb_id", name=IMDB_ID_UNIQUE_CONSTRAINT),
        Index("ix_movie_id", "id"),
        Index("ix_movie_imdb_id", "imdb_id"),
    )
