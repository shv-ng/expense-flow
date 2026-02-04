from datetime import date, datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.auth.dependencies import get_current_user
from app.database import get_session
from app.models import Category, Expense, User

router = APIRouter(prefix="/expenses", tags=["expenses"])


# create expenses
@router.post("/")
def create_expense(
    amount: float,
    category_id: uuid.UUID,
    date: datetime = date.today(),
    description: str | None = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    # check if category exists
    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    expense = Expense(
        amount=amount,
        description=description,
        date=date,
        category_id=category_id,
        user_id=current_user.id,
    )

    session.add(expense)
    session.commit()
    session.refresh(expense)

    return expense


# get expenses with filters like date range and/or category
@router.get("/")
def get_expenses(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    category_id: uuid.UUID | None = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    stmt = select(Expense).where(Expense.user_id == current_user.id)
    if date_from:
        stmt = stmt.where(Expense.date >= date_from)
    if date_to:
        stmt = stmt.where(Expense.date <= date_to)
    if category_id:
        stmt = stmt.where(Expense.category_id == category_id)
    return session.exec(stmt).all()


# get one expenses
@router.get("/{id}")
def get_expense(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return session.exec(
        select(Expense).where(Expense.id == id, User.id == current_user.id)
    ).first()


# update expenses
@router.put("/{id}")
def update_expense(
    id: uuid.UUID,
    amount: float | None = None,
    description: str | None = None,
    date: date | None = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    expense = session.exec(
        select(Expense).where(Expense.id == id, User.id == current_user.id)
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if amount:
        expense.amount = amount
    if description:
        expense.description = description
    if date:
        expense.date = date

    session.add(expense)
    session.commit()
    session.refresh(expense)
    return


# delete expenses
@router.delete("/{id}")
def delete_expense(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    expense = session.exec(
        select(Expense).where(Expense.id == id, User.id == current_user.id)
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    session.delete(expense)
    session.commit()
    return
