from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from repositories.database.models.base import Base


class Rating(Base):
    """Rating entity from a specific source for a movie"""

    __tablename__ = "rating"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id", ondelete="CASCADE"))
    source: Mapped[str] = mapped_column(String)
    value: Mapped[str] = mapped_column(String)

    movie: Mapped["Movie"] = relationship(lazy="noload")

    __table_args__ = (
        UniqueConstraint("movie_id", "source", "value", name="movie_source_value_unique"),
    )
