from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"user": "me"}
