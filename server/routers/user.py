from fastapi import APIRouter, Depends, Request

from schemas.user import UserCreate, UserLogin
from app.db import get_db, Session
import utils.dependencies as is_authenticated_user
from services.user import register_service, login_service, user_service, refresh_token_service

router = APIRouter(prefix="/user", tags=["users"])

@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    response = await register_service(user, db)
    return response


@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    response = await login_service(user, db)
    return response

@router.get("/me")
async def get_user(user_id : str = Depends(is_authenticated_user), db: Session = Depends(get_db)):
    response = await user_service(user_id, db)
    return response

@router.get("/refresh")
async def refresh_token(request: Request):
    response = await refresh_token_service(request)
    return response
