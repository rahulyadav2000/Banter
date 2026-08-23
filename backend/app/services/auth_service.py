from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core import hash_password, verify_password
from app.models import User
from app.schemas import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email.lower())

    return db.scalar(statement)


def get_user_by_name(db: Session, name: str) -> User | None:
    statement = select(User).where(User.name == name)
    return db.scalar(statement)


def create_user(db: Session, data: UserCreate) -> User | None:
    user = User(
        name=data.name.strip(),
        email=data.email.lower(),
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)

    if user is None:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user


# implement password reset later
