from fastapi import APIRouter, Depends
from sqlmodel import Session, extract, func, select

from app.db import get_session
from app.deps import get_current_user
from app.models import Category, Expense, User

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/spending-by-date")
def get_analytics(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    stmt = (
        select(
            Expense.date,
            func.sum(Expense.amount).label("total"),
        )
        .where(Expense.user_id == current_user.id)
        .group_by(Expense.date)
        .order_by(Expense.date)
    )

    rows = session.exec(stmt).all()

    return {
        "labels": [str(date) for date, _ in rows],
        "data": [total for _, total in rows],
    }


@router.get("/spending-by-category")
def spending_by_category(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(
            Category.name,
            func.sum(Expense.amount).label("total"),
        )
        .join(Expense, Expense.category_id == Category.id)
        .where(Expense.user_id == current_user.id)
        .group_by(Category.name)
    )

    rows = session.exec(stmt).all()

    return {
        "labels": [name for name, _ in rows],
        "data": [total for _, total in rows],
    }


@router.get("/spending-by-month")
def spending_by_month(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(
            extract("month", Expense.date).label("month"),
            func.sum(Expense.amount).label("total"),
        )
        .where(Expense.user_id == current_user.id)
        .group_by("month")
        .order_by("month")
    )

    rows = session.exec(stmt).all()

    return {
        "labels": [int(month) for month, _ in rows],
        "data": [total for _, total in rows],
    }
