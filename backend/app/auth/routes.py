from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.auth.security import create_access_token, hash_password, verify_password
from app.database import get_session
from app.models.users import User


router = APIRouter(prefix="/auth", tags=["auth"])


# create user
@router.post("/register")
def register(
    username: str, email: str, password: str, session: Session = Depends(get_session)
):
    existing = session.exec(
        select(User).where((User.username == username) | (User.email == email))
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"id": user.id, "username": user.username}


# login
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}
