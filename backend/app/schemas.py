import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel


class CategoryRequest(BaseModel):
    name: str
    color: str


class CreateExpense(BaseModel):
    amount: float
    category_id: uuid.UUID
    date: datetime = date.today()
    description: str | None = None


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class CategoryRead(SQLModel):
    id: uuid.UUID
    name: str
    color: str


class ExpenseRead(SQLModel):
    id: uuid.UUID
    amount: float
    description: str | None
    date: date
    created_at: datetime

    category: Optional[CategoryRead]
