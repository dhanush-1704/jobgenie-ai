from sqlalchemy.orm import Session

from src.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from src.crud.user import (
    create_user,
    get_user_by_email,
)
from src.models.user import User
from src.schemas.user import (
    Token,
    UserCreate,
)


def register_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    """
    Register a new user.
    """
    existing_user = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user:
        raise ValueError("Email already registered")

    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(
            user_data.password,
        ),
    )

    return create_user(
        db,
        user,
    )


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    """
    Verify user credentials.
    """
    user = get_user_by_email(
        db,
        email,
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user


def login_user(
    db: Session,
    email: str,
    password: str,
) -> Token:
    """
    Login user and return JWT token.
    """
    user = authenticate_user(
        db,
        email,
        password,
    )

    if not user:
        raise ValueError(
            "Invalid email or password"
        )

    access_token = create_access_token(
        subject=user.id,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )