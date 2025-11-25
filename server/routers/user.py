from fastapi import APIRouter, Depends

from schemas.user import UserCreate, UserLogin
from app.db import get_db, Session
from services.user import create_user, login

router = APIRouter(prefix="/user", tags=["users"])

@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    response = await create_user(user, db)
    return response


@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    response = await login(user, db)
    return response

# @router.get("/me")
# async def get_current_user(db: Session = Depends(get_db)):
#     user = await get_current_user(db)
#     return user
