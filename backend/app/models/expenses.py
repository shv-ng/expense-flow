from datetime import datetime, date
import uuid
from sqlmodel import Field, SQLModel


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    amount: float
    description: str | None

    category_id: uuid.UUID = Field(foreign_key="categories.id",index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)

    date: date
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
