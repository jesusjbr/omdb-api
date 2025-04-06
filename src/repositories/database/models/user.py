from sqlalchemy import Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from repositories.database.models.base import Base


class User(Base):
    """User entity"""

    __tablename__ = "member"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean)

    __table_args__ = (UniqueConstraint("username", name="username_unique"),)
