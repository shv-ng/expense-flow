from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db import get_session
from app.deps import get_current_user
from app.models import Category, User
from app.schemas import CategoryRequest

router = APIRouter(prefix="/categories", tags=["categories"])


# list all categories
@router.get("/")
def get_categories(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    stmt = select(Category).where(Category.user_id == current_user.id)
    return session.exec(stmt).all()


# add a category
@router.post("/")
def add_category(
    data: CategoryRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    category = Category(name=data.name, color=data.color, user_id=current_user.id)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category
