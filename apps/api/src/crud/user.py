from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get a user by email."""
    return db.scalar(
        select(User).where(User.email == email)
    )


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Get a user by ID."""
    return db.scalar(
        select(User).where(User.id == user_id)
    )


def create_user(db: Session, user: User) -> User:
    """Persist a user."""

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_all_users(db: Session) -> list[User]:
    """Get all users."""

    return list(
        db.scalars(
            select(User)
        ).all()
    )


def delete_user(db: Session, user: User) -> None:
    """Delete a user."""

    db.delete(user)
    db.commit()