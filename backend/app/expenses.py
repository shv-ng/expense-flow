import uuid
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.db import get_session
from app.deps import get_current_user
from app.models import Category, Expense, User
from app.schemas import CreateExpense, ExpenseRead

router = APIRouter(prefix="/expenses", tags=["expenses"])


# create expenses
@router.post("/")
def create_expense(
    data: CreateExpense,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    # check if category exists
    category = session.exec(
        select(Category).where(Category.id == data.category_id)
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    expense = Expense(
        amount=data.amount,
        description=data.description,
        date=data.date,
        category_id=data.category_id,
        user_id=current_user.id,
    )

    session.add(expense)
    session.commit()
    session.refresh(expense)

    return expense


# get expenses with filters like date range and/or category
@router.get("/", response_model=list[ExpenseRead])
def get_expenses(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    category_id: uuid.UUID | None = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    stmt = (
        select(Expense)
        .where(Expense.user_id == current_user.id)
        .options(selectinload(Expense.category))
    )
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
        select(Expense).where(Expense.id == id, Expense.user_id == current_user.id)
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
        select(Expense).where(Expense.id == id, Expense.user_id == current_user.id)
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
    return expense


# delete expenses
@router.delete("/{id}")
def delete_expense(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    expense = session.exec(
        select(Expense).where(Expense.id == id, Expense.user_id == current_user.id)
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    session.delete(expense)
    session.commit()
    return
