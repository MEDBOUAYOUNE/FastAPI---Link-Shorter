from fastapi import APIRouter, Depends, Request

from schemas.user import UserCreate, UserLogin
from app.db import get_db, Session
from services.user import register_service, login_service, refresh_token_service

router = APIRouter(prefix="/user", tags=["users"])

@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    response = await register_service(user, db)
    return response


@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    response = await login_service(user, db)
    return response

# @router.get("/me")
# async def get_user(db: Session = Depends(get_db)):
#     user = await user_service(db)
#     return user

@router.get("/refresh")
async def refresh_token(request: Request):
    response = await refresh_token_service(request)
    return response
