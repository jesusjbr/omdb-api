from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from repositories.database.models.base import Base


class MovieRating(Base):
    """Rating entity from a specific source for a movie"""

    __tablename__ = "movie_rating"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id", ondelete="CASCADE"))
    source: Mapped[str] = mapped_column(String)
    value: Mapped[str] = mapped_column(String)

    movie: Mapped["Movie"] = relationship(back_populates="ratings")
