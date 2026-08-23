from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserPublic
from app.core import get_current_user
from app.services.user_service import search_user

router = APIRouter(prefix="/users", tags=["users"])


# searches the users from logged in user
@router.get("/search", response_model=list[UserPublic])
def search_users(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[int, Depends(get_current_user)],
    q: str = Query(min_length=2, max_length=50),
):
    return search_user(db=db, query=q, current_user_id=current_user.id)
