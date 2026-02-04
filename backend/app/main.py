from fastapi import FastAPI
from .auth import routes as auth
from .users import routes as users
from .categories import routes as categories
from .expenses import routes as expenses
from .analytics import routes as analytics

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(expenses.router)
app.include_router(analytics.router)


@app.get("/health")
def health():
    return
