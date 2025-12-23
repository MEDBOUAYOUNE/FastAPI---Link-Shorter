from fastapi import APIRouter, Depends, Request
from app.db import get_db, Session
from models.user import User
from utils.dependencies import is_authenticated_user
from services.link import create_link_service, get_link_by_short_code_service, delete_link_service, get_link_stats_service, get_link_by_short_code_service

router = APIRouter(prefix="/link", tags=["links"])

@router.post("/add")
async def create_link(request: Request, db: Session = Depends(get_db), user: User = Depends(is_authenticated_user)):
    data = await request.json()
    original_url = data.get("original_url")
    response = await create_link_service(original_url, user, db)
    return response

@router.get("/{short_code}")
async def get_link_by_short_code(short_code: str, request: Request, db: Session = Depends(get_db)):
    response = await get_link_by_short_code_service(short_code, request, db)
    return response

@router.delete("/{short_code}")
async def delete_link(short_code: str, db: Session = Depends(get_db), user: User = Depends(is_authenticated_user)):
    response = await delete_link_service(short_code, user, db)
    return response

@router.get("/stats/{short_code}")
async def get_link_stats(short_code: str, db: Session = Depends(get_db), user: User = Depends(is_authenticated_user)):
    response = await get_link_stats_service(short_code, user, db)
    return response
