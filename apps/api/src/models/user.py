from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    resumes: Mapped[list["Resume"]] = relationship(
        "Resume",
        back_populates="user",
        cascade="all, delete-orphan",
    )