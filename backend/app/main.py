from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import analytics, auth, categories, expenses,users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)
app.include_router(analytics.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return
