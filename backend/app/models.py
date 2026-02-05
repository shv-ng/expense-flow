import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models import Category, Expense


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    amount: float
    description: str | None

    category_id: uuid.UUID = Field(foreign_key="categories.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)

    date: date
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    category: Optional["Category"] = Relationship(back_populates="expenses")


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")

    name: str
    color: str

    expenses: List["Expense"] = Relationship(back_populates="category")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)

    hashed_password: str
    full_name: str | None = None

    disabled: bool = False
