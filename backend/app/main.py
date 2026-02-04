from fastapi import FastAPI
from .auth import routes as auth

app = FastAPI()

app.include_router( auth.router)


@app.get("/health")
def health():
    return {"status": "ok"}
