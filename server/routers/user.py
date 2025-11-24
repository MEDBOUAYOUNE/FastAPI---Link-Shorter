from fastapi import APIRouter, Depends

from schemas.user import UserCreate
from app.db import get_db, Session
from services.user import create_user

router = APIRouter(prefix="/user", tags=["users"])

@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    response = await create_user(user, db)
    return response

