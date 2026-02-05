
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db import get_session
from app.deps import get_current_user
from app.models import User


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users(current_user: User = Depends(get_current_user),session:Session = Depends(get_session)):
    users = session.exec(select(User).where(current_user.id == User.id)).first()
    result = {
        "username": users.username,
        "full_name": users.full_name,
        "email": users.email,
    }
    return result
