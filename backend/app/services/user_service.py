from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import User


def search_user(
    db: Session, query: str, current_user_id: int, limit: int = 10
) -> list[User]:
    q = query.strip()

    if not q:
        return []

    statement = (
        select(User)
        .where(
            User.id != current_user_id,
            User.name.ilike(f"%{q}%"),
        )
        .order_by(User.name)
        .limit(limit)
    )

    return list(db.scalars(statement).all())
